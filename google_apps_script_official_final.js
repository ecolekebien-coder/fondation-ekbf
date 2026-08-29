/**
 * =======================================================================
 * DÉCLENCHEUR OFFICIEL JSB 2027 — ÉCOLE KÉ BIEN FONDATION & ANVRI
 * Version Garantie 100% PDF & Pièce Jointe Attachée
 * =======================================================================
 */

var FORM_ID = "1-dRLV-vJ-VyzFOmFh5ASz8bpxiYvI0Uez3Qy_Xal-l0";
var SPREADSHEET_ID = "1pCu_M1vUBYjKhiS3GwjG0l6fwYiRQDsDcPxuNYVT_hk";

var LOGO_EKBF_URL = "https://raw.githubusercontent.com/ecolekebien-coder/fondation-ekbf/main/assets/images/logo.jpg";
var LOGO_ANVRI_URL = "https://raw.githubusercontent.com/ecolekebien-coder/fondation-ekbf/main/assets/images/anvri.png";

/**
 * Exécutez cette fonction UNE SEULE FOIS pour installer le déclencheur
 */
function installerDeclencheurFormulaire() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    ScriptApp.deleteTrigger(triggers[i]);
  }
  
  var form = FormApp.openById(FORM_ID);
  ScriptApp.newTrigger("onFormSubmit")
           .forForm(form)
           .onFormSubmit()
           .create();
           
  Logger.log("SUCCÈS : Déclencheur Formulaire installé et actif pour JSB 2027 !");
}

function onFormSubmit(e) {
  var itemResponses = e.response.getItemResponses();
  var answers = {};
  
  for (var i = 0; i < itemResponses.length; i++) {
    var title = itemResponses[i].getItem().getTitle();
    var val = itemResponses[i].getResponse();
    answers[title] = Array.isArray(val) ? val.join(" ; ") : val;
  }

  function get(key) {
    for (var k in answers) {
      if (k.toLowerCase().indexOf(key.toLowerCase()) !== -1) return answers[k];
    }
    return "";
  }

  var profil = get("Vous êtes") || "Participant (auditeur simple)";
  var nom = get("Nom complet") || get("Personne à contacter") || "Participant";
  
  var email = "";
  try {
    if (e.response && typeof e.response.getRespondentEmail === "function") {
      email = e.response.getRespondentEmail();
    }
  } catch(err) {}
  if (!email) {
    email = get("Email") || get("Email de contact") || get("Courriel");
  }

  var tel = get("Téléphone");
  var statut = get("Statut");
  var etablissement = get("Établissement") || get("Faculté") || get("Institut");
  var filiere = get("Filière") || get("Département");
  var titreProjet = get("Titre");
  var resumeProjet = get("Résumé");
  var organisation = get("Nom de l'organisation");
  var secteur = get("Secteur d'activité");
  var attestation = get("Attestation") || "Oui";

  if (!email || email.indexOf("@") === -1) {
    Logger.log("Erreur : Email manquant ou invalide (" + email + ")");
    return;
  }

  // 1. Couleurs et Titres selon profil
  var typeKey = "AUDITEUR";
  var codePrefix = "JSB27-AUD-";
  var colorPrimary = "#163B5C"; // Bleu Marine
  var colorAccent = "#0284C7";  // Bleu Ciel
  var colorPillBg = "#EFF6FF";
  var roleTitle = "PARTICIPANT / AUDITEUR";
  var roleSubtitle = "ACCÈS CONFÉRENCES, ATELIERS & POSTERS";
  var securityTag = "ACCRÉDITATION OFFICIELLE";
  var securityBg = "#38BDF8";
  var securityColor = "#0C2338";
  
  if (profil.toLowerCase().indexOf("candidat") !== -1 || profil.toLowerCase().indexOf("prix") !== -1 || profil.toLowerCase().indexOf("innovation") !== -1) {
    typeKey = "CANDIDAT";
    codePrefix = "JSB27-CAN-";
    colorPrimary = "#C2410C"; // Orange Foncé
    colorAccent = "#F97316";  // Orange Vif
    colorPillBg = "#FFF7ED";
    roleTitle = "CANDIDAT AU PRIX INNOVATION";
    roleSubtitle = "COMPÉTITION & PITCH DEVANT LE JURY";
    securityTag = "PRIX INNOVATION 2027";
    securityBg = "#F97316";
    securityColor = "#FFFFFF";
  } else if (profil.toLowerCase().indexOf("partenaire") !== -1 || profil.toLowerCase().indexOf("sponsor") !== -1) {
    typeKey = "PARTENAIRE";
    codePrefix = "JSB27-SPO-";
    colorPrimary = "#065F46"; // Vert Émeraude
    colorAccent = "#D97706";  // Or
    colorPillBg = "#F0FDF4";
    roleTitle = "PARTENAIRE & SPONSORING";
    roleSubtitle = "ACCÈS VIP & ESPACE PARTENAIRES";
    securityTag = "ACCÈS VIP OFFICIEL";
    securityBg = "#F59E0B";
    securityColor = "#0C2338";
  }

  var randomNum = Math.floor(1000 + Math.random() * 9000);
  var codeBadge = codePrefix + randomNum;
  var qrCodeUrl = "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=" + encodeURIComponent("JSB2027|" + codeBadge + "|" + nom + "|" + roleTitle);

  // 2. HTML Compatible Moteur PDF Google Apps Script
  var badgeHtml = `
  <!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <style>
      body { font-family: Arial, sans-serif; margin: 0; padding: 10px; background-color: #ffffff; text-align: center; }
      .badge-table {
        width: 100%; border-collapse: collapse; text-align: center;
        border: 4px solid ${colorPrimary}; background-color: #ffffff;
      }
      .top-banner {
        background-color: #0C2338; color: #ffffff; padding: 14px 10px; text-align: center;
        border-bottom: 3px solid ${colorAccent};
      }
      .security-pill {
        background-color: ${securityBg}; color: ${securityColor}; font-size: 8.5px; font-weight: bold;
        padding: 3px 12px; border-radius: 10px; display: inline-block; text-transform: uppercase; margin-bottom: 5px;
      }
      .title-main { font-size: 22px; font-weight: bold; letter-spacing: 2px; margin: 0; text-transform: uppercase; color: #ffffff; }
      .title-sub { font-size: 9.5px; opacity: 0.95; margin: 3px 0 0 0; text-transform: uppercase; color: #BAE6FD; }
      
      .logos-cell {
        padding: 12px 14px; background-color: #ffffff; border-bottom: 2px solid #e2e8f0;
      }
      .logo-label {
        font-size: 7.5px; font-weight: bold; color: #0f172a; text-transform: uppercase; margin-top: 4px;
      }
      .role-cell {
        padding: 10px 14px 4px 14px; text-align: center;
      }
      .role-box {
        background-color: ${colorPillBg}; border: 2px solid ${colorAccent};
        padding: 8px 14px; border-radius: 8px; display: inline-block; width: 85%;
      }
      .role-label { font-size: 13px; font-weight: bold; color: ${colorPrimary}; text-transform: uppercase; margin: 0; }
      .role-desc { font-size: 8.5px; font-weight: bold; color: ${colorAccent}; margin: 3px 0 0 0; text-transform: uppercase; }

      .name-cell {
        padding: 6px 14px; text-align: center;
      }
      .attendee-name { font-size: 18px; font-weight: bold; color: #0f172a; text-transform: uppercase; margin: 0; }
      .attendee-affil { font-size: 11px; color: #475569; margin: 3px 0 0 0; font-weight: bold; }
      .project-box {
        font-size: 9px; font-weight: bold; color: #c2410c; background-color: #fff7ed;
        padding: 4px 8px; border-radius: 4px; border: 1px dashed #fdba74; display: inline-block; margin-top: 4px;
      }

      .qr-cell {
        padding: 6px 14px; text-align: center;
      }
      .qr-frame {
        background-color: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 10px;
        padding: 6px; display: inline-block;
      }
      .code-text {
        font-family: Courier, monospace; font-size: 14px; font-weight: bold;
        color: ${colorPrimary}; letter-spacing: 2px; margin-top: 5px;
      }

      .footer-cell {
        background-color: #0C2338; color: #ffffff; padding: 12px 10px; text-align: center;
      }
      .footer-loc { font-size: 9.5px; font-weight: bold; color: #38bdf8; margin: 0; }
      .footer-inst { font-size: 8.5px; color: #e2e8f0; margin: 3px 0 0 0; }
    </style>
  </head>
  <body>
    <table class="badge-table" cellpadding="0" cellspacing="0">
      <tr>
        <td class="top-banner">
          <div class="security-pill">${securityTag}</div>
          <div class="title-main">JSB 2027</div>
          <div class="title-sub">3ᵉ Journée des Sciences Biologiques</div>
        </td>
      </tr>
      <tr>
        <td class="logos-cell">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td align="center" width="40%">
                <img src="${LOGO_EKBF_URL}" height="56" style="display:block; margin:0 auto;" />
                <div class="logo-label">ÉCOLE KÉ BIEN FONDATION</div>
              </td>
              <td align="center" width="20%" style="font-size:8px; font-weight:bold; color:#64748b;">
                &bull; PARTENARIAT &bull;<br><span style="color:#d97706;">OFFICIEL</span>
              </td>
              <td align="center" width="40%">
                <img src="${LOGO_ANVRI_URL}" height="56" style="display:block; margin:0 auto;" />
                <div class="logo-label">ANVRI CONGO</div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td class="role-cell">
          <div class="role-box">
            <div class="role-label">${roleTitle}</div>
            <div class="role-desc">${roleSubtitle}</div>
          </div>
        </td>
      </tr>
      <tr>
        <td class="name-cell">
          <div class="attendee-name">${nom}</div>
          <div class="attendee-affil">${statut || organisation || 'Participant Officiel'} ${etablissement ? '• ' + etablissement : ''}</div>
          ${typeKey === 'CANDIDAT' && titreProjet ? '<div class="project-box">Projet : ' + titreProjet + '</div>' : ''}
        </td>
      </tr>
      <tr>
        <td class="qr-cell">
          <div class="qr-frame">
            <img src="${qrCodeUrl}" width="110" height="110" style="display:block; margin:0 auto;" />
            <div class="code-text">${codeBadge}</div>
          </div>
        </td>
      </tr>
      <tr>
        <td class="footer-cell">
          <div class="footer-loc">📍 Amphithéâtre FST — Brazzaville • Mars 2027</div>
          <div class="footer-inst">École Ké Bien Fondation &bull; Partenaire Officiel ANVRI</div>
        </td>
      </tr>
    </table>
  </body>
  </html>
  `;

  // 3. Génération du Blob PDF Officiel
  var htmlBlob = Utilities.newBlob(badgeHtml, 'text/html', 'badge.html');
  var badgeBlob = htmlBlob.getAs('application/pdf');
  badgeBlob.setName('Badge_JSB2027_' + nom.replace(/\s+/g, '_') + '.pdf');

  // 4. Sauvegarde dans Google Drive (Dossier dédié)
  var pdfDriveUrl = "";
  try {
    var folderName = "JSB 2027 — Badges Officiels";
    var folders = DriveApp.getFoldersByName(folderName);
    var targetFolder = folders.hasNext() ? folders.next() : DriveApp.createFolder(folderName);
    var savedFile = targetFolder.createFile(badgeBlob);
    savedFile.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    pdfDriveUrl = savedFile.getUrl();
  } catch (dErr) {
    Logger.log("Erreur sauvegarde Drive: " + dErr);
  }

  // 5. Contenu du Mail selon le rôle
  var subject = "";
  var bodyHtml = "";

  if (typeKey === "AUDITEUR") {
    subject = "🎟️ Confirmation d'inscription & Votre Badge d'accès — JSB 2027";
    bodyHtml = `
      <p>Bonjour <strong>${nom}</strong>,</p>
      <p>Nous vous confirmons votre inscription en tant que <strong>Participant (Auditeur)</strong> à la <strong>3ᵉ Journée des Sciences Biologiques (JSB 2027)</strong>, organisée par l'<strong>École Ké Bien Fondation</strong> en partenariat officiel avec l'<strong>ANVRI</strong>.</p>
      <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; border-left: 4px solid #163b5c; margin: 15px 0;">
        <p style="margin: 0 0 6px 0;"><strong>Votre Code d'accès :</strong> <code style="font-size: 15px; color: #163b5c; font-weight: bold;">${codeBadge}</code></p>
        <p style="margin: 0 0 6px 0;"><strong>Statut :</strong> ${statut} (${etablissement || 'Non spécifié'})</p>
        <p style="margin: 0;"><strong>Lieu :</strong> Amphithéâtre FST, Brazzaville (Mars 2027)</p>
      </div>
      <p>🪪 <strong>Votre Badge d'Accès Officiel PDF est joint à cet e-mail</strong> avec votre QR Code individuel.</p>
      <p>Bien cordialement,<br><strong>École Ké Bien Fondation & ANVRI</strong></p>
    `;
  } else if (typeKey === "CANDIDAT") {
    subject = "🏆 Confirmation de Candidature — Grand Prix de l'Innovation JSB 2027 & Votre Badge";
    bodyHtml = `
      <p>Bonjour <strong>${nom}</strong>,</p>
      <p>Nous accusons réception de votre candidature pour le <strong>Grand Prix de l'Innovation (JSB 2027)</strong>.</p>
      <div style="background: #fff7ed; padding: 15px; border-radius: 8px; border-left: 4px solid #ea580c; margin: 15px 0;">
        <p style="margin: 0 0 6px 0;"><strong>Votre Code Candidat :</strong> <code style="font-size: 15px; color: #ea580c; font-weight: bold;">${codeBadge}</code></p>
        <p style="margin: 0 0 6px 0;"><strong>Titre du Projet :</strong> <em>« ${titreProjet || 'Projet soumis'} »</em></p>
        <p style="margin: 0;"><strong>Filière / Statut :</strong> ${filiere || statut}</p>
      </div>
      <p>🪪 <strong>Veuillez trouver votre Badge Candidat officiel joint à cet e-mail</strong> pour votre passage devant le jury.</p>
      <p>Scientifiquement vôtre,<br><strong>Le Jury & Comité Scientifique JSB 2027</strong></p>
    `;
  } else {
    subject = "🤝 Remerciements & Prise de contact — Partenariat JSB 2027 & Votre Badge VIP";
    bodyHtml = `
      <p>Bonjour <strong>${nom}</strong> (${organisation || 'Partenaire'}),</p>
      <p>Nous vous remercions chaleureusement pour votre soutien à la <strong>JSB 2027</strong>.</p>
      <div style="background: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #059669; margin: 15px 0;">
        <p style="margin: 0 0 6px 0;"><strong>Organisation :</strong> ${organisation || nom}</p>
        <p style="margin: 0;"><strong>Code Partenaire :</strong> <code style="font-size: 15px; color: #059669; font-weight: bold;">${codeBadge}</code></p>
      </div>
      <p>🪪 <strong>Veuillez trouver en pièce jointe votre Badge Partenaire / VIP officiel</strong>.</p>
      <p>Avec nos salutations distinguées,<br><strong>Pr Aimé Christian KAYATH • Président Fondateur</strong></p>
    `;
  }

  // 6. Envoi de l'Email avec la Pièce Jointe Badge PDF
  try {
    MailApp.sendEmail({
      to: email,
      subject: subject,
      htmlBody: bodyHtml,
      name: "JSB 2027 — École Ké Bien & ANVRI",
      attachments: [badgeBlob]
    });
    Logger.log("SUCCÈS : Email avec Badge PDF envoyé à " + email);
  } catch (mErr) {
    Logger.log("Erreur envoi email: " + mErr);
  }

  // 7. Synchronisation Multi-Onglets dans Google Sheet
  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var dateStr = Utilities.formatDate(new Date(), "GMT+1", "dd/MM/yyyy HH:mm");
    var respId = e.response ? e.response.getId() : "MANUAL-" + new Date().getTime();

    // A. Onglet Global : Toutes les réponses
    var allSheet = ss.getSheetByName("📋 Toutes les réponses") || ss.getSheets()[0];
    allSheet.appendRow([
      dateStr, respId, codeBadge, profil, nom, email, tel,
      statut, etablissement, filiere, attestation,
      titreProjet, resumeProjet, "", "",
      organisation, secteur, nom, "",
      "", "", "Badge envoyé (PDF joint)", dateStr, pdfDriveUrl
    ]);

    // B. Onglets Spécifiques
    if (typeKey === "AUDITEUR") {
      var audSheet = ss.getSheetByName("🎟️ Auditeurs simples");
      if (audSheet) {
        audSheet.appendRow([
          dateStr, respId, codeBadge, nom, email, tel,
          statut, etablissement, attestation, "Badge envoyé (PDF joint)", dateStr, pdfDriveUrl
        ]);
      }
    } else if (typeKey === "CANDIDAT") {
      var canSheet = ss.getSheetByName("🏆 Candidats Prix Innovation");
      if (canSheet) {
        canSheet.appendRow([
          dateStr, respId, codeBadge, nom, email, tel,
          statut, etablissement, filiere,
          titreProjet, resumeProjet, "", "",
          "Badge envoyé (PDF joint)", "", "", "", "", "", "", "", pdfDriveUrl
        ]);
      }
    } else if (typeKey === "PARTENAIRE") {
      var partSheet = ss.getSheetByName("🤝 Partenaires & Sponsoring");
      if (partSheet) {
        partSheet.appendRow([
          dateStr, codeBadge, organisation, secteur, nom,
          email, tel, "Accompagnement / Sponsoring", "",
          "", "Badge envoyé (PDF joint)", dateStr, "À contacter", pdfDriveUrl
        ]);
      }
    }
  } catch (sErr) {
    Logger.log("Erreur Sheet: " + sErr);
  }
}