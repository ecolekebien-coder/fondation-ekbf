import json
import urllib.request
import urllib.parse
import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from reportlab.lib.pagesizes import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.barcode import qr
from reportlab.pdfgen import canvas

# Dimensions Carte Badge standard : 95mm x 145mm
BADGE_WIDTH = 95 * mm
BADGE_HEIGHT = 145 * mm

def generate_pdf_badge(filepath, role_type, code_badge, nom, affil_text="", project_text=""):
    c = canvas.Canvas(filepath, pagesize=(BADGE_WIDTH, BADGE_HEIGHT))
    
    # Couleurs de la charte officielle
    c_dark = colors.HexColor("#0C2338")
    c_ekbf_blue = colors.HexColor("#163B5C")
    
    if role_type == "CANDIDAT":
        c_primary = colors.HexColor("#C2410C")
        c_accent = colors.HexColor("#F97316")
        c_pill_bg = colors.HexColor("#FFF7ED")
        role_label = "CANDIDAT AU PRIX INNOVATION"
        role_sub = "COMPÉTITION & PITCH DEVANT LE JURY"
        sec_tag = "PRIX INNOVATION 2027"
        sec_bg = colors.HexColor("#F97316")
        sec_txt = colors.white
    elif role_type == "PARTENAIRE":
        c_primary = colors.HexColor("#065F46")
        c_accent = colors.HexColor("#D97706")
        c_pill_bg = colors.HexColor("#F0FDF4")
        role_label = "PARTENAIRE & SPONSORING"
        role_sub = "ACCÈS VIP & ESPACE PARTENAIRES"
        sec_tag = "ACCÈS VIP OFFICIEL"
        sec_bg = colors.HexColor("#F59E0B")
        sec_txt = colors.HexColor("#0C2338")
    else: # AUDITEUR
        c_primary = colors.HexColor("#163B5C")
        c_accent = colors.HexColor("#0284C7")
        c_pill_bg = colors.HexColor("#F0F9FF")
        role_label = "PARTICIPANT / AUDITEUR"
        role_sub = "ACCÈS CONFÉRENCES, ATELIERS & POSTERS"
        sec_tag = "ACCRÉDITATION OFFICIELLE"
        sec_bg = colors.HexColor("#38BDF8")
        sec_txt = colors.HexColor("#0C2338")

    # 1. Fond blanc et bordure officielle
    c.setStrokeColor(c_primary)
    c.setLineWidth(3)
    c.setFillColor(colors.white)
    c.roundRect(2*mm, 2*mm, BADGE_WIDTH - 4*mm, BADGE_HEIGHT - 4*mm, 5*mm, fill=1, stroke=1)

    # 2. Bandeau supérieur (Header dégradé sombre)
    c.setFillColor(c_dark)
    c.roundRect(2*mm, BADGE_HEIGHT - 26*mm, BADGE_WIDTH - 4*mm, 24*mm, 4*mm, fill=1, stroke=0)
    c.rect(2*mm, BADGE_HEIGHT - 26*mm, BADGE_WIDTH - 4*mm, 8*mm, fill=1, stroke=0)

    # Liseré couleur sous le header
    c.setFillColor(c_accent)
    c.rect(2*mm, BADGE_HEIGHT - 27*mm, BADGE_WIDTH - 4*mm, 1.2*mm, fill=1, stroke=0)

    # Pastille de sécurité
    c.setFillColor(sec_bg)
    c.roundRect(BADGE_WIDTH/2 - 22*mm, BADGE_HEIGHT - 9*mm, 44*mm, 4.5*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(sec_txt)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(BADGE_WIDTH/2, BADGE_HEIGHT - 8*mm, sec_tag)

    # Titres événement
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(BADGE_WIDTH/2, BADGE_HEIGHT - 17*mm, "JSB 2027")
    c.setFont("Helvetica-Bold", 6.5)
    c.setFillColor(colors.HexColor("#BAE6FD"))
    c.drawCentredString(BADGE_WIDTH/2, BADGE_HEIGHT - 22*mm, "3E JOURNÉE DES SCIENCES BIOLOGIQUES")

    # 3. Logos Partenaires Grands Formats (hauteur 14mm / ~55px)
    y_logo = BADGE_HEIGHT - 44*mm
    logo_ekbf_path = "assets/images/logo.jpg"
    logo_anvri_path = "assets/images/anvri.png"

    if os.path.exists(logo_ekbf_path):
        c.drawImage(logo_ekbf_path, 6*mm, y_logo, width=28*mm, height=14*mm, preserveAspectRatio=True, mask='auto')
    if os.path.exists(logo_anvri_path):
        c.drawImage(logo_anvri_path, BADGE_WIDTH - 34*mm, y_logo, width=28*mm, height=14*mm, preserveAspectRatio=True, mask='auto')

    # Texte partenariat central
    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(BADGE_WIDTH/2, y_logo + 8*mm, "• PARTENARIAT •")
    c.setFillColor(c_accent)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawCentredString(BADGE_WIDTH/2, y_logo + 5*mm, "OFFICIEL")

    # Ligne de séparation logos
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.setLineWidth(0.8)
    c.line(4*mm, y_logo - 2*mm, BADGE_WIDTH - 4*mm, y_logo - 2*mm)

    # 4. Boîte de Rôle Stylisée
    y_role = y_logo - 14*mm
    c.setFillColor(c_pill_bg)
    c.setStrokeColor(c_accent)
    c.setLineWidth(1)
    c.roundRect(6*mm, y_role, BADGE_WIDTH - 12*mm, 10*mm, 3*mm, fill=1, stroke=1)

    c.setFillColor(c_primary)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(BADGE_WIDTH/2, y_role + 5.5*mm, role_label)
    c.setFillColor(c_accent)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawCentredString(BADGE_WIDTH/2, y_role + 2*mm, role_sub)

    # 5. Nom & Affiliation
    y_name = y_role - 7*mm
    c.setFillColor(colors.HexColor("#0F172A"))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(BADGE_WIDTH/2, y_name, nom.upper())

    c.setFillColor(colors.HexColor("#475569"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(BADGE_WIDTH/2, y_name - 4.5*mm, affil_text)

    if project_text:
        c.setFillColor(colors.HexColor("#C2410C"))
        c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(BADGE_WIDTH/2, y_name - 8.5*mm, f"Projet : « {project_text} »")

    # 6. QR Code avec réticules de visée
    y_qr = 24*mm
    qr_size = 26*mm
    qr_x = BADGE_WIDTH/2 - qr_size/2

    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.roundRect(qr_x - 2*mm, y_qr - 2*mm, qr_size + 4*mm, qr_size + 4*mm, 3*mm, fill=1, stroke=1)

    qr_data = f"JSB2027|{code_badge}|{nom}|{role_type}"
    qr_code = qr.QrCodeWidget(qr_data)
    qr_code.barWidth = qr_size
    qr_code.barHeight = qr_size
    qr_code.qrVersion = 1
    d = Drawing(qr_size, qr_size)
    d.add(qr_code)
    d.drawOn(c, qr_x, y_qr)

    # Code Série en dessous
    c.setFillColor(c_primary)
    c.setFont("Courier-Bold", 9.5)
    c.drawCentredString(BADGE_WIDTH/2, y_qr - 6*mm, code_badge)

    # 7. Footer
    c.setFillColor(c_dark)
    c.roundRect(2*mm, 2*mm, BADGE_WIDTH - 4*mm, 13*mm, 3*mm, fill=1, stroke=0)
    c.rect(2*mm, 10*mm, BADGE_WIDTH - 4*mm, 5*mm, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#38BDF8"))
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(BADGE_WIDTH/2, 9*mm, "📍 Amphithéâtre FST — Brazzaville • Mars 2027")

    c.setFillColor(colors.HexColor("#E2E8F0"))
    c.setFont("Helvetica", 5.5)
    c.drawCentredString(BADGE_WIDTH/2, 5*mm, "École Ké Bien Fondation • Partenaire Officiel ANVRI")

    c.save()
    print(f"Badge PDF généré : {filepath}")

def send_all_tests():
    with open("google_token.json", "r", encoding="utf-8") as f:
        tokens = json.load(f)
    token = tokens["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    recipient = "dieuvitk@gmail.com"
    os.makedirs("generated_badges", exist_ok=True)

    items = [
        {
            "type": "AUDITEUR",
            "code": "JSB27-AUD-8421",
            "nom": "Dr. Christian KIBAMBA",
            "affil": "Enseignant-Chercheur • FST / UMNG",
            "proj": "",
            "pdf": "generated_badges/Badge_JSB27_Auditeur_KIBAMBA.pdf",
            "subject": "🎟️ [TEST JSB 2027 AVEC BADGE PDF] Votre Badge Auditeur Officiel",
            "body": "<p>Bonjour <strong>Dr. Christian KIBAMBA</strong>,</p><p>Votre inscription en tant que <strong>Participant (Auditeur)</strong> à la <strong>JSB 2027</strong> a été validée avec succès.</p><p>🪪 <strong>Votre Badge d'Accès Officiel PDF est joint à cet e-mail</strong>, muni de votre QR Code de contrôle.</p><p>Code d'accès : <strong>JSB27-AUD-8421</strong></p><p>Bien cordialement,<br><strong>École Ké Bien Fondation & ANVRI</strong></p>"
        },
        {
            "type": "CANDIDAT",
            "code": "JSB27-CAN-3914",
            "nom": "Sarah MAMPASSI",
            "affil": "Étudiante Master 2 • Bio-Ressources",
            "proj": "Valorisation des Bio-Ressources Locales",
            "pdf": "generated_badges/Badge_JSB27_Candidat_MAMPASSI.pdf",
            "subject": "🏆 [TEST JSB 2027 AVEC BADGE PDF] Votre Badge Candidat Officiel",
            "body": "<p>Bonjour <strong>Sarah MAMPASSI</strong>,</p><p>Votre candidature au <strong>Grand Prix de l'Innovation JSB 2027</strong> est bien enregistrée.</p><p>🪪 <strong>Votre Badge Candidat Officiel PDF est joint à cet e-mail</strong> pour votre passage devant le jury.</p><p>Code Candidat : <strong>JSB27-CAN-3914</strong></p><p>Scientifiquement vôtre,<br><strong>Comité Scientifique JSB 2027 & ANVRI</strong></p>"
        },
        {
            "type": "PARTENAIRE",
            "code": "JSB27-SPO-9052",
            "nom": "TotalEnergies Congo",
            "affil": "Délégation Officielle • Partenaire Or",
            "proj": "",
            "pdf": "generated_badges/Badge_JSB27_Partenaire_TotalEnergies.pdf",
            "subject": "🤝 [TEST JSB 2027 AVEC BADGE PDF] Votre Badge Partenaire VIP Officiel",
            "body": "<p>Bonjour <strong>TotalEnergies Congo</strong>,</p><p>Nous vous remercions pour votre précieux soutien à la <strong>JSB 2027</strong>.</p><p>🪪 <strong>Votre Badge Partenaire & Accès VIP PDF est joint à cet e-mail</strong>.</p><p>Code Partenaire : <strong>JSB27-SPO-9052</strong></p><p>Avec nos salutations distinguées,<br><strong>Pr Aimé Christian KAYATH • Président Fondateur</strong></p>"
        }
    ]

    for item in items:
        # 1. Génération du PDF
        generate_pdf_badge(item["pdf"], item["type"], item["code"], item["nom"], item["affil"], item["proj"])
        
        # 2. Préparation du mail avec PJ
        msg = MIMEMultipart()
        msg["To"] = recipient
        msg["From"] = "ecolekebien@gmail.com"
        msg["Subject"] = item["subject"]

        msg.attach(MIMEText(item["body"], "html", "utf-8"))

        with open(item["pdf"], "rb") as f:
            pdf_data = f.read()
        
        attachment = MIMEApplication(pdf_data, _subtype="pdf")
        filename = os.path.basename(item["pdf"])
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

        # 3. Envoi via Gmail API
        raw_msg = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        send_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
        req = urllib.request.Request(
            send_url,
            data=json.dumps({"raw": raw_msg}).encode('utf-8'),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print(f"SUCCÈS : Mail avec Badge PDF envoyé pour {item['type']} -> Message ID: {res.get('id')}")

if __name__ == "__main__":
    send_all_tests()