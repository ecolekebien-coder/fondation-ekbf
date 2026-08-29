import json
import urllib.request
import urllib.parse

def get_valid_token():
    with open("google_token.json", "r", encoding="utf-8") as f:
        tokens = json.load(f)

    with open("google_client_secret.json", "r", encoding="utf-8") as f:
        cs = json.load(f)["installed"]

    # Refresh access token
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": cs["client_id"],
        "client_secret": cs["client_secret"],
        "refresh_token": tokens["refresh_token"],
        "grant_type": "refresh_token"
    }

    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(token_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

    try:
        with urllib.request.urlopen(req) as resp:
            new_data = json.loads(resp.read().decode('utf-8'))
            tokens["access_token"] = new_data["access_token"]
            if "refresh_token" in new_data:
                tokens["refresh_token"] = new_data["refresh_token"]
            with open("google_token.json", "w", encoding="utf-8") as out:
                json.dump(tokens, out, indent=2)
            print("Google Access Token successfully refreshed!")
            return tokens["access_token"]
    except Exception as e:
        print("Error refreshing token:", e)
        return tokens.get("access_token")

if __name__ == "__main__":
    get_valid_token()
