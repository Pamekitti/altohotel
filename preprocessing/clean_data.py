def clean_hotel_data(ds):
    web_cols = ['imageGallery/images/0/fallbackImage/url', 'imageGallery/images/0/image/url',
                'imageGallery/images/1/image/url',
                'imageGallery/images/2/image/url',
                'imageGallery/images/3/image/url',
                'propertyDetailsLink/uri/value', 'propertyImage/fallbackImage/url', 'propertyImage/image/url']

    shit_cols = ['destinationInfo/distanceFromDestination/unit', 'destinationInfo/distanceFromMessaging', 'destinationInfo/regionId',
                 'imageGallery/images/0/fallbackImage', 'imageGallery/images/0/imageId', 'imageGallery/images/0/subjectId',
                 'imageGallery/images/1/fallbackImage', 'imageGallery/images/1/imageId', 'imageGallery/images/1/subjectId',
                 'imageGallery/images/2/fallbackImage', 'imageGallery/images/2/imageId', 'imageGallery/images/2/subjectId',
                 'imageGallery/images/3/fallbackImage', 'imageGallery/images/3/imageId', 'imageGallery/images/3/subjectId',
                 'legalDisclaimer', 'mapMarker/icon', 'mapMarker/type', 'offerSummary/messages/0/mark', 'offerSummary/messages/1/mark',
                 'price/alignment', 'price/disclaimer', 'price/displayMessages', 'price/marketingFeeDetails', 'price/options/0/disclaimer',
                 'price/options/0/leadingCaption', 'price/options/0/loyaltyPrice', 'price/options/0/strikeOut', 'price/priceMessages/0/value',
                 'price/roomNightMessage', 'price/strikeOut', 'priceMetadata/rateDiscount', 'propertyImage/fallbackImage', 'propertyImage/fallbackImage/description',
                 'reviews/mark', 'reviews/scoreDenominator','star', 'amenities/0/name', 'amenities/1/name', 'amenities/2/name', 'price/strikeOut/formatted',
                 'priceMetadata/rateDiscount/description', 'propertyImage/image/description'
    ]

    df = ds[[col for col in ds.columns if col not in web_cols + shit_cols]]
    df = df.rename(columns={'amenities/0/icon':'amenities_0',
                    'amenities/1/icon':'amenities_1',
                    'amenities/2/icon':'amenities_2',
                    'availability/available':'availability',
                    'availability/minRoomsLeft':'roomleft',
                    'availability/text':'soldout',
                    'destinationInfo/distanceFromDestination/value':'dis_from_des',
                    'imageGallery/images/0/fallbackImage/description':'fallback_image',
                    'imageGallery/images/0/image/description':'image_0',
                    'imageGallery/images/1/image/description':'image_1',
                    'imageGallery/images/2/image/description':'image_2',
                    'imageGallery/images/3/image/description':'image_3',
                    'mapMarker/label':'map_marker_price',
                    'mapMarker/latLong/latitude':'latitude',
                    'mapMarker/latLong/longitude':'longitude',
                    'neighborhood/name':'neighborhood',
                    'offerSummary/messages/0/message':'offer_summary_0',
                    'offerSummary/messages/0/theme':'offer_theme_0',
                    'offerSummary/messages/0/type':'free_cancel',
                    'offerSummary/messages/1/message':'offer_summary_1',
                    'offerSummary/messages/1/theme':'offer_theme_1',
                    'offerSummary/messages/1/type':'pay_later',
                    'price/disclaimer/value':'price_disclaimer',
                    'price/lead/formatted':'price_lead',
                    'price/options/0/disclaimer/value':'price_disclaim',
                    'price/options/0/displayPrice/formatted':'price_display',
                    'price/options/0/strikeOut/formatted':'price_original',
                    'price/strikeOutType':'strikeout_type',
                    'priceMetadata/discountType':'discount_type',
                    'priceMetadata/totalDiscountPercentage':'discount_percent',
                    'reviews/score':'review_score',
                    'reviews/superlative':'review_superlative',
                    'reviews/total':'review_count',
                    'vipMessaging':'vip'
                    })

    df = df.drop(['map_marker_price', 'price_lead', 'soldout', 'fallback_image',
             'offer_theme_0', 'offer_summary_0', 'offer_theme_1', 'offer_summary_1',
             'neighborhood', 'image_0', 'image_1', 'image_2', 'image_3', 'fallback_image',
             'price_disclaimer', 'price_disclaim', 'strikeout_type', 'discount_type'], axis=1)

    for col in ['price_display', 'price_original']:
        df[col] = df[col].str.replace('$', '', regex=True)
        df[col] = df[col].str.replace(',', '', regex=True)
        df[col] = df[col].astype('float')

    col = df.pop("name")
    df.insert(0, col.name, col)
    col = df.pop("id")
    df.insert(0, col.name, col)

    return df