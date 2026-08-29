import json
import urllib.request
import urllib.parse

def push_code_to_apps_script():
    with open("google_token.json", "r", encoding="utf-8") as f:
        tokens = json.load(f)
    token = tokens["access_token"]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Search for script project in Drive
    q = "mimeType = 'application/vnd.google-apps.script' and trashed = false"
    url = f"https://www.googleapis.com/drive/v3/files?q={urllib.parse.quote(q)}&fields=files(id,name)"
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req) as resp:
        files = json.loads(resp.read().decode('utf-8')).get("files", [])
    
    print("Projets Apps Script trouvés dans Google Drive :")
    for f in files:
        print(f" - Nom: {f.get('name')}, ID: {f.get('id')}")

    if not files:
        print("Aucun fichier script autonome trouvé. Recherche des scripts liés au formulaire...")
        # If bound to form or spreadsheet, we check
        return

    target_script_id = files[0]["id"]
    for f in files:
        if "BADGE" in f.get("name", "").upper():
            target_script_id = f["id"]
            break

    print(f"\nMise à jour du projet : {target_script_id}...")

    # 2. Get existing content to preserve manifest (appsscript.json)
    get_url = f"https://script.googleapis.com/v1/projects/{target_script_id}/content"
    req_get = urllib.request.Request(get_url, headers=headers)
    
    manifest_file = None
    try:
        with urllib.request.urlopen(req_get) as resp:
            content = json.loads(resp.read().decode('utf-8'))
            for item in content.get("files", []):
                if item.get("type") == "JSON" and item.get("name") == "appsscript":
                    manifest_file = item
    except Exception as e:
        print("Erreur lecture projet:", e)

    if not manifest_file:
        manifest_file = {
            "name": "appsscript",
            "type": "JSON",
            "source": json.dumps({
                "timeZone": "Africa/Brazzaville",
                "dependencies": {},
                "exceptionLogging": "STACKDRIVER",
                "runtimeVersion": "V8"
            }, indent=2)
        }

    # 3. Read our new code
    with open("google_apps_script_official_final.js", "r", encoding="utf-8") as f:
        code_source = f.read()

    new_files = [
        manifest_file,
        {
            "name": "Code",
            "type": "SERVER_JS",
            "source": code_source
        }
    ]

    put_url = f"https://script.googleapis.com/v1/projects/{target_script_id}/content"
    req_put = urllib.request.Request(
        put_url,
        data=json.dumps({"files": new_files}).encode("utf-8"),
        headers=headers,
        method="PUT"
    )

    with urllib.request.urlopen(req_put) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("\nSUCCÈS : Code mis à jour directement dans votre Google Apps Script !")
        print(f"URL du projet : https://script.google.com/d/{target_script_id}/edit")

if __name__ == "__main__":
    push_code_to_apps_script()
