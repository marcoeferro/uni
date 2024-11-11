import requests

def login(loginUrl:str,session:requests) -> requests:
    """
    Args: 
        str: the login url
    Returns:
        requests: the api response to the login  
    """

    #detalles del login
    payload = {
        "account":"absch",
        "password":"Unvime24",
        "validateCode":""
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5,es-MX;q=0.4",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "referer": loginUrl,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = session.post(
        loginUrl,
        data=payload,
        headers=headers
    )

    if (response.status_code == 200 ):
        try:
            return response
        except ValueError as e:
            print(f"Deserealization - ERROR on login data [ERROR : {e}]")
    else:
        print(f"RESPONSE ERROR on login data request [RESPONSE CODE : {response.status_code}]")
