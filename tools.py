import requests
from urllib.parse import quote_plus

def check_if_user_exists(username: str) -> bool:
    # Encode the username for a URL (spaces, etc.)
    encoded_name = quote_plus(username)
    url = f"https://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player={encoded_name}"

    response = requests.get(url)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise RuntimeError(
            f"Unexpected status {response.status_code} from hiscores API for {username!r}"
        )