# Budget categories choices

class ModelChoices:
    # APP TYPE 
    APP_TYPE_KROON = "KROON"
    APP_TYPE_KIOSK = "KIOSK"
    APP_TYPE_ALL = "GENERAL"

    # GENDER TYPE
    GENDER_ONE = "MALE"
    GENDER_TWO = "FEMALE"
    
    APP_TYPES = (
        (APP_TYPE_KROON, APP_TYPE_KROON),
        (APP_TYPE_KIOSK, APP_TYPE_KIOSK),
        (APP_TYPE_ALL, APP_TYPE_ALL)   
    )

    GENDER_TYPE = (
        (GENDER_ONE, GENDER_ONE),
        (GENDER_TWO, GENDER_TWO),
    )



