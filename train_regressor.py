from sklearn.model_selection import train_test_split
import xgboost as xgb
import pandas as pd

df = pd.read_csv('csv_files/clustered_hotel.csv')

FEATURES = ['availability', 'roomleft', 'dis_from_des', 'latitude', 'longitude',
            'free_cancel', 'pay_later', 'discount_percent', 'review_score',
            'review_count', 'vip', 'have_hot_tub', 'have_pool', 'have_free_breakfast']
target = 'price'
train = df.dropna()
test = df[df['price_display'].isna()]
trainX, trainY = train[FEATURES], train[target]
X_test = test[FEATURES]
X_train, X_valid, y_train, y_valid = train_test_split(trainX,
                                                    trainY,
                                                    test_size=.2,
                                                    random_state=42)
dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_valid, label=y_valid)
dtest = xgb.DMatrix(X_test)
params = {
    'eta': 0.01,
    'gamma': 1,
    'max_depth':4,
    'min_child_weight': 1,
    'subsample': 1,
    'colsample_bytree': 1,
    'colsample_bylevel': 1,
    'colsample_bynode': 1,
    'lambda': 1,
    'alpha': 0,
    'tree_method': 'exact',
    'objective': 'reg:squarederror',
    'eval_metric':'rmse',
    'seed': 42
}
model = xgb.train(
    params,
    dtrain,
    num_boost_round=10000,
    evals = [(dtrain, 'train'), (dvalid, 'val')],
    early_stopping_rounds=100,
    verbose_eval=100
)
xgb.plot_importance(model)
y_preds = model.predict(dtest)
df['price_regressor'] = df['price']
for i, index in enumerate(df[df['price_regressor'].isna()].index):
    df.loc[index, 'price_test'] = y_preds[i]
df.to_csv('csv_files/clustered_hotel_regressor_filled.csv')
