import requests
import json

def get_photovoltaic_device_data(session: requests, loginUrl: str) -> json:
    """
    Args: 
        requests: the login session 
        str(loginUrl): the login url
    Returns:
        json: the api response with the storage energy day chart 
    """
    url = 'https://server.growatt.com/panel/getDevicesByPlantList'

    payload = {"currPage":"1",
                "plantId":"2613959"}

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
        "Referer": loginUrl,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = session.post(
        url,
        data=payload,
        headers=headers
    )

    if (response.status_code == 200 ):
        try:
            return json.loads(response.text)
        except ValueError as e:
            print(f"Deserealization - ERROR on photovoltaic device data [ERROR : {e}]")
    else:
        print(f"RESPONSE ERROR on photovoltaic device data request [RESPONSE CODE : {response.status_code}]")