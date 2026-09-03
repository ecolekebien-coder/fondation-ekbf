import os
import re
import json
import urllib.request

def check_html_file(filename):
    print(f"\n--- Analyse de {filename} ---")
    if not os.path.exists(filename):
        print(f"Fichier {filename} manquant !")
        return
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    # Form links
    forms = re.findall(r'https://(?:forms\.gle|docs\.google\.com/forms)[^\s"\'<>]+', html)
    print(f"  Liens Google Forms trouvés ({len(forms)}) :")
    for fl in set(forms):
        print(f"    -> {fl}")

    # Images
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    print(f"  Images référencées ({len(imgs)}) :")
    for img in set(imgs):
        if img.startswith("http"):
            print(f"    -> [Distant] {img}")
        else:
            exists = os.path.exists(img)
            print(f"    -> [Local] {img} (Existe: {'OUI' if exists else 'NON'})")

    # CSS / JS
    css_files = re.findall(r'<link[^>]+href=["\']([^"\']+\.css)["\']', html)
    for c in set(css_files):
        print(f"  CSS: {c} (Existe: {'OUI' if os.path.exists(c) else 'NON'})")
    
    js_files = re.findall(r'<script[^>]+src=["\']([^"\']+\.js)["\']', html)
    for j in set(js_files):
        print(f"  JS: {j} (Existe: {'OUI' if os.path.exists(j) else 'NON'})")

def main():
    print("==================================================")
    print("VÉRIFICATION TECHNIQUE DU CODE GITHUB & DU SITE")
    print("==================================================")

    # 1. Vérification HTML
    check_html_file("index.html")
    check_html_file("jsb2027.html")

    # 2. Vérification GitHub Pages en ligne
    print("\n--- Test des URLs en ligne (GitHub Pages) ---")
    urls = [
        "https://ecolekebien-coder.github.io/fondation-ekbf/",
        "https://ecolekebien-coder.github.io/fondation-ekbf/jsb2027.html",
        "https://ecolekebien-coder.github.io/fondation-ekbf/assets/css/style.css",
        "https://ecolekebien-coder.github.io/fondation-ekbf/assets/js/main.js",
        "https://ecolekebien-coder.github.io/fondation-ekbf/assets/images/logo.jpg",
        "https://ecolekebien-coder.github.io/fondation-ekbf/assets/images/anvri.png"
    ]
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                size = len(resp.read())
                print(f"  [HTTP {status}] {u} ({size} octets)")
        except Exception as e:
            print(f"  [ERREUR] {u} : {e}")

if __name__ == "__main__":
    main()
