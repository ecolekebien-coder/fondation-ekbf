import json
import urllib.request
import urllib.parse

token = json.load(open("google_token.json", encoding="utf-8"))["access_token"]
headers = {"Authorization": f"Bearer {token}"}

def query(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

# 1. Folders in Drive
print("=== DOSSIERS DRIVE ===")
folders = query("https://www.googleapis.com/drive/v3/files?q=" + urllib.parse.quote("mimeType = 'application/vnd.google-apps.folder' and trashed = false") + "&fields=" + urllib.parse.quote("files(id,name,createdTime)"))
for f in folders.get("files", []):
    print(f"Folder: {f['name']} (ID: {f['id']})")

# 2. PDF Files in Drive
print("\n=== FICHIERS PDF RECENTS ===")
pdfs = query("https://www.googleapis.com/drive/v3/files?q=" + urllib.parse.quote("mimeType = 'application/pdf' and trashed = false") + "&fields=" + urllib.parse.quote("files(id,name,createdTime,size,webViewLink)"))
for f in pdfs.get("files", []):
    print(f"PDF: {f['name']} (ID: {f['id']}, Créé le: {f.get('createdTime')})")

# 3. Form ID & Details
print("\n=== GOOGLE FORM ===")
form_data = query("https://forms.googleapis.com/v1/forms/1-dRLV-vJ-VyzFOmFh5ASz8bpxiYvI0Uez3Qy_Xal-l0")
print("Titre du Formulaire :", form_data.get("info", {}).get("title"))
print("Description :", form_data.get("info", {}).get("description")[:100] if form_data.get("info", {}).get("description") else "Pas de description")
