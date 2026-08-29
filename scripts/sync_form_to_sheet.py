import json
import urllib.request
import urllib.parse
from datetime import datetime

FORM_ID = "1-dRLV-vJ-VyzFOmFh5ASz8bpxiYvI0Uez3Qy_Xal-l0"
SPREADSHEET_ID = "1pCu_M1vUBYjKhiS3GwjG0l6fwYiRQDsDcPxuNYVT_hk"

def sync_responses():
    with open("google_token.json", "r", encoding="utf-8") as f:
        tokens = json.load(f)
    token = tokens["access_token"]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Fetch Form Schema to map Question Titles to Question IDs
    form_url = f"https://forms.googleapis.com/v1/forms/{FORM_ID}"
    req = urllib.request.Request(form_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        form = json.loads(resp.read().decode('utf-8'))

    q_map = {} # questionId -> title
    for item in form.get("items", []):
        if "questionItem" in item:
            q = item["questionItem"]["question"]
            qid = q.get("questionId")
            q_map[qid] = item.get("title", "")

    # 2. Fetch all Form Responses
    resp_url = f"https://forms.googleapis.com/v1/forms/{FORM_ID}/responses"
    req_resp = urllib.request.Request(resp_url, headers=headers)
    with urllib.request.urlopen(req_resp) as resp:
        resp_data = json.loads(resp.read().decode('utf-8'))

    responses = resp_data.get("responses", [])
    print(f"Total responses fetched from Google Form: {len(responses)}")

    all_rows = []
    auditeur_rows = []
    candidat_rows = []
    partenaire_rows = []

    for r in responses:
        rid = r.get("responseId")
        created_time = r.get("lastSubmittedTime") or r.get("createTime")
        answers = r.get("answers", {})

        # Extract values by question title lookup
        parsed_ans = {}
        for qid, a_obj in answers.items():
            t = q_map.get(qid, "")
            text_vals = [a.get("value", "") for a in a_obj.get("textAnswers", {}).get("answers", [])]
            parsed_ans[t] = " ; ".join(text_vals)

        # Helper to find answer by key phrase
        def get_val(key_phrase):
            for t, val in parsed_ans.items():
                if key_phrase.lower() in t.lower():
                    return val
            return ""

        profil = get_val("Vous êtes")
        nom = get_val("Nom complet")
        email = get_val("Email")
        tel = get_val("Téléphone")
        statut = get_val("Statut")
        etablissement = get_val("Établissement")
        filiere = get_val("Filière")
        attestation = get_val("attestation")
        
        # Candidat specific
        titre_projet = get_val("Titre")
        resume_projet = get_val("Résumé")
        pdf_projet = get_val("Dossier de présentation") or get_val("document PDF") or get_val("Lien du document")
        cni = get_val("Pièce d'identité") or get_val("carte d'identité") or get_val("CNI")

        # Partenaire specific
        organisation = get_val("Nom de l'organisation")
        secteur = get_val("Secteur")
        contact_partenaire = get_val("Personne à contacter")
        cadre_soutien = get_val("Dans quel cadre")
        detail_proposition = get_val("Décrivez votre proposition")
        attentes_partenaire = get_val("Qu'attendez-vous")

        # Code d'inscription automatique
        index_num = 1000 + len(all_rows) + 1
        if "candidat" in profil.lower() or "prix" in profil.lower() or "innovation" in profil.lower():
            code_badge = f"JSB27-CAN-{index_num}"
        elif "partenaire" in profil.lower() or "sponsoring" in profil.lower():
            code_badge = f"JSB27-SPO-{index_num}"
        else:
            code_badge = f"JSB27-AUD-{index_num}"

        # Build row for "Toutes les réponses" (23 colonnes)
        row_all = [
            created_time, rid, code_badge, profil, nom, email, tel, statut, etablissement, filiere, attestation,
            titre_projet, resume_projet, pdf_projet, cni,
            organisation, secteur, contact_partenaire, cadre_soutien, detail_proposition, attentes_partenaire,
            "Badge prêt", ""
        ]
        all_rows.append(row_all)

        # Dispatch to specific tabs
        if "auditeur" in profil.lower() or "participant" in profil.lower():
            row_auditeur = [
                created_time, rid, code_badge, nom, email, tel, statut, etablissement, attestation, "Badge prêt", ""
            ]
            auditeur_rows.append(row_auditeur)
        elif "candidat" in profil.lower() or "prix" in profil.lower() or "innovation" in profil.lower():
            row_candidat = [
                created_time, rid, code_badge, nom, email, tel, statut, etablissement, filiere,
                titre_projet, resume_projet, pdf_projet, cni,
                "Badge prêt", "", "", "", "", "", "", "Dossier soumis"
            ]
            candidat_rows.append(row_candidat)
        elif "partenaire" in profil.lower() or "sponsoring" in profil.lower():
            row_partenaire = [
                created_time, code_badge, organisation, secteur, contact_partenaire, email or get_val("Email de contact"),
                tel or get_val("Téléphone"), cadre_soutien, detail_proposition, attentes_partenaire, "Badge prêt", "", "À contacter"
            ]
            partenaire_rows.append(row_partenaire)

    # Update Google Sheets tabs
    values_payload = {
        "valueInputOption": "USER_ENTERED",
        "data": []
    }

    if all_rows:
        values_payload["data"].append({
            "range": f"'📋 Toutes les réponses'!A2:W{len(all_rows)+1}",
            "values": all_rows
        })
    if auditeur_rows:
        values_payload["data"].append({
            "range": f"'👥 Auditeurs simples'!A2:K{len(auditeur_rows)+1}",
            "values": auditeur_rows
        })
    if candidat_rows:
        values_payload["data"].append({
            "range": f"'💡 Candidats Prix Innovation'!A2:U{len(candidat_rows)+1}",
            "values": candidat_rows
        })
    if partenaire_rows:
        values_payload["data"].append({
            "range": f"'🤝 Partenaires & Sponsoring'!A2:M{len(partenaire_rows)+1}",
            "values": partenaire_rows
        })

    if values_payload["data"]:
        update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values:batchUpdate"
        req_up = urllib.request.Request(update_url, data=json.dumps(values_payload).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req_up) as resp:
            print("SUCCESS: Google Sheet synchronized with latest Form responses!")
    else:
        print("No new responses to write.")

if __name__ == "__main__":
    sync_responses()
