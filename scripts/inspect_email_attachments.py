import json
import urllib.request

token = json.load(open("google_token.json", encoding="utf-8"))["access_token"]
headers = {"Authorization": f"Bearer {token}"}

req = urllib.request.Request('https://gmail.googleapis.com/gmail/v1/users/me/messages?q=in:sent&maxResults=3', headers=headers)
res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
for m in res.get('messages', []):
    m_url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{m['id']}"
    m_detail = json.loads(urllib.request.urlopen(urllib.request.Request(m_url, headers=headers)).read().decode('utf-8'))
    headers_dict = {h['name']: h['value'] for h in m_detail.get('payload', {}).get('headers', [])}
    print(f"\nSubject: {headers_dict.get('Subject')}")
    print(f"To: {headers_dict.get('To')}")
    print(f"Date: {headers_dict.get('Date')}")
    parts = m_detail.get('payload', {}).get('parts', [])
    for p in parts:
        print(f"  Part: mime={p.get('mimeType')}, filename='{p.get('filename')}', size={p.get('body', {}).get('size')} bytes")
