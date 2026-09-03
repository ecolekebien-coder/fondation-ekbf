import json
import urllib.request
import urllib.parse

def sync():
    token = json.load(open("google_token.json", encoding="utf-8"))["access_token"]
    sheet_id = "1pCu_M1vUBYjKhiS3GwjG0l6fwYiRQDsDcPxuNYVT_hk"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Row for Auditeurs simples
    aud_row = [
        "31/08/2026 13:00",
        "2_ABaOnudIqodYwI_QKhZzH66pFvFQzz8LQRd4WBDQLRQxkAgNNWuuR2rSFRZbmT175vrCI2M",
        "JSB27-AUD-1484",
        "Okouakoua Yannick Frédéric ",
        "fryokouakoua@gmail.com",
        "242066077680",
        "Professionnel",
        "National institute of natural and exact sciences ",
        "Oui",
        "Badge envoyé (PDF joint)",
        "31/08/2026 13:00"
    ]

    u_aud = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote('👥 Auditeurs simples')}!A:K:append?valueInputOption=USER_ENTERED"
    req_aud = urllib.request.Request(u_aud, data=json.dumps({"values": [aud_row]}).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req_aud) as resp:
            print("Succès ajout dans 👥 Auditeurs simples")
    except Exception as e:
        print("Erreur Auditeurs:", e)

    # 2. Row for Candidats Prix Innovation
    can_row = [
        "31/08/2026 13:09",
        "2_ABaOnucr5MinkOngIlJSW14fBCA31Asf4S5N5QL4KoG1PzAU3HJZ2-NFgpwpmo11VNhiXPw",
        "JSB27-CAN-7602",
        "Okouakoua Yannick Frédéric ",
        "fryokouakoua@gmail.com",
        "242066077680",
        "Enseignant-Chercheur",
        "IRA",
        "Agronomy ",
        "PGPF for growth plant and biofertilizer",
        "Help for durable agriculture use biofertilizer for promoting biological lutte against phytopathogen ",
        "https://drive.google.com/open?id=1JY7di-AFV_BckXlKmIgobtkZkHIUGYUY",
        "https://drive.google.com/open?id=1rX3b-I9zausviOYFwsebpAxZQbuXhTj7",
        "Badge envoyé (PDF joint)"
    ]

    u_can = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote('💡 Candidats Prix Innovation')}!A:N:append?valueInputOption=USER_ENTERED"
    req_can = urllib.request.Request(u_can, data=json.dumps({"values": [can_row]}).encode('utf-8'), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req_can) as resp:
            print("Succès ajout dans 💡 Candidats Prix Innovation")
    except Exception as e:
        print("Erreur Candidats:", e)

if __name__ == "__main__":
    sync()
