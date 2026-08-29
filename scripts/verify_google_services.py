import json
import urllib.request
import urllib.parse

def test_google_access():
    with open("google_token.json", "r", encoding="utf-8") as f:
        tokens = json.load(f)
        
    access_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    results = {}
    
    # 1. Test Gmail Profile
    try:
        req = urllib.request.Request("https://gmail.googleapis.com/gmail/v1/users/me/profile", headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results["Gmail"] = f"OK - Email: {data.get('emailAddress')} (Total Messages: {data.get('messagesTotal')})"
    except Exception as e:
        results["Gmail"] = f"Error: {e}"

    # 2. Test Google Drive
    try:
        req = urllib.request.Request("https://www.googleapis.com/drive/v3/files?pageSize=5&fields=files(id,name)", headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            file_count = len(data.get("files", []))
            results["Google Drive"] = f"OK - {file_count} recent files found"
    except Exception as e:
        results["Google Drive"] = f"Error: {e}"

    # 3. Test Calendar
    try:
        req = urllib.request.Request("https://www.googleapis.com/calendar/v3/users/me/calendarList", headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            cal_count = len(data.get("items", []))
            results["Google Calendar"] = f"OK - {cal_count} calendars accessible"
    except Exception as e:
        results["Google Calendar"] = f"Error: {e}"

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_google_access()
