import json
import urllib.request
import urllib.parse

token = json.load(open("google_token.json", encoding="utf-8"))["access_token"]
sheet_id = "1pCu_M1vUBYjKhiS3GwjG0l6fwYiRQDsDcPxuNYVT_hk"
headers = {"Authorization": f"Bearer {token}"}

tab_name = "📋 Toutes les réponses"
u = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote(tab_name)}!A1:Z5"
res = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=headers)).read().decode('utf-8'))
headers_row = res.get("values", [])[0]

for i, r in enumerate(res.get("values", [])[1:], start=2):
    print(f"\n--- LIGNE {i} ---")
    for j, val in enumerate(r):
        col_name = headers_row[j] if j < len(headers_row) else f"Col_{j}"
        if val:
            print(f"  {col_name}: {val}")
