# Budget categories choices

class ModelChoices:
    APP_TYPE_KROON = "KROON"
    APP_TYPE_KIOSK = "KIOSK"
    APP_TYPE_ALL = "GENERAL"
    
    APP_TYPES = (
        (APP_TYPE_KROON, APP_TYPE_KROON),
        (APP_TYPE_KIOSK, APP_TYPE_KIOSK),
        (APP_TYPE_ALL, APP_TYPE_ALL)   
    )
