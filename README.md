# 🏛️ Fondation École Ké Bien (EKBF) & JSB 2027

> **« L'école est bien, l'école paye — School is Good, School pays »**  
> *Portail officiel de la Fondation et de la 3e Journée des Sciences Biologiques (JSB 2027), en partenariat avec l'ANVRI.*

---

## 📌 Présentation

L'**École Ké Bien Fondation (EKBF)** a été initiée par le **Professeur Titulaire Aimé Christian KAYATH** (Professeur Titulaire des Universités - CAMES, Université Marien Ngouabi, République du Congo).

La fondation a pour mission de :
- Promouvoir les **bonnes mœurs**, l'éthique intellectuelle et le civisme.
- Valoriser l'**excellence académique** et la recherche scientifique appliquée.
- Stimuler et accompagner les **jeunes inventeurs et chercheurs**.
- Organiser la **Journée des Sciences Biologiques (JSB)** en partenariat avec les institutions nationales.

---

## 🤝 Partenaire Institutionnel Officiel

- **ANVRI** : *Agence Nationale de Valorisation des Résultats de la Recherche et de l'Innovation*  
  Partenaire institutionnel pour l'évaluation, l'accompagnement pratique et la valorisation des inventions primées au Grand Prix de l'Innovation JSB.

---

## 🌐 Architecture du Site Web

Le site est conçu en **HTML5 / CSS3 moderne / JavaScript natif** sans dépendance lourde, garantissant une rapidité de chargement maximale et une compatibilité responsive complète (Mobile-First) :

- **index.html** : Portail institutionnel de la Fondation École Ké Bien (Vision, 5 Valeurs Cardinales, 4 Piliers, Mot du Fondateur, Partenariats).
- **jsb2027.html** : Portail dédié à la **3e Journée des Sciences Biologiques (JSB 2027)** (Compte à rebours dynamique, Grand Prix de l'Innovation, 3 Profils de Candidature, FAQ interactive).
- **ssets/css/style.css** : Charte graphique officielle (*Bleu Nuit #163b5c*, *Or #d97706*, *Orange #f97316*, *Vert ANVRI #15803d*), menu mobile drawer, sticky bar d'action mobile et animations au scroll.
- **ssets/js/main.js** : Moteur JavaScript léger (IntersectionObserver pour scroll reveal, compte à rebours, menu mobile, accordéon FAQ).

---

## ⚙️ Automatisations & Outils

Le dossier scripts/ et les fichiers associés contiennent les modules d'automatisation pour la gestion de l'événement JSB 2027 :

1. **google_apps_script_official_final.js** : Script Google Apps Script pour l'envoi automatisé des confirmations et des badges PDF dès la soumission du Google Form.
2. **scripts/sync_form_to_sheet.py** : Synchronisation Google Forms vers Google Sheets.
3. **scripts/send_badges_with_real_pdf.py** : Moteur Python de génération et d'expédition des badges PDF.
4. **scripts/refresh_token.py** : Gestionnaire automatique de rafraîchissement OAuth2 Google API.

---

## 🚀 Déploiement

Le site est hébergé et déployé automatiquement via **GitHub Pages** sur la branche main.

---

## 📄 Licence & Droits

© 2026-2027 **Fondation École Ké Bien (EKBF)**. Tous droits réservés.
