import json
import urllib.request
import urllib.parse

token = json.load(open("google_token.json", encoding="utf-8"))["access_token"]
sheet_id = "1pCu_M1vUBYjKhiS3GwjG0l6fwYiRQDsDcPxuNYVT_hk"
headers = {"Authorization": f"Bearer {token}"}

tabs = [
    "📋 Toutes les réponses",
    "⚙️ Compteur",
    "👥 Auditeurs simples",
    "💡 Candidats Prix Innovation",
    "🤝 Partenaires & Sponsoring"
]

for tab in tabs:
    u = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote(tab)}!A1:H15"
    try:
        req = urllib.request.Request(u, headers=headers)
        res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        vals = res.get("values", [])
        print(f"=== {tab} === (total rows: {len(vals)})")
        for i, row in enumerate(vals[:5]):
            print(f"  Row {i+1}: {row[:4]}")
    except Exception as e:
        print(f"=== {tab} === ERROR: {e}")
