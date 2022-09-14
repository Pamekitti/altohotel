
# Hotel Dash

Visualize hotel business performance with interactive dashboard and unsupervised clustering machine learning integration.

## Link 
hoteldash.atfbbtb9d5a7acc5.southeastasia.azurecontainer.io


## Installation

Install my-project with npm

```bash
  pip install -r requirements.txt
```

To run DASH on your local computer, in file main.py, change

```python
app_port = os.environ['APP_PORT']
```

To

```python
app_port = '80
```


## Deployment

To deploy this project run

```bash
  docker build --tag name .
```

On mac Apple Silicon
```bash
docker buildx build --platform=linux/amd64 -t name .
```

Then
```bash
  docker push name
```
Deploy using Azure Container Instance Services

