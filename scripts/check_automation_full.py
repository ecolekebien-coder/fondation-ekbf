import json
import urllib.request
import urllib.parse
import sys

def get_token():
    with open("google_token.json", "r", encoding="utf-8") as f:
        return json.load(f)["access_token"]

def make_request(url, headers, method="GET", data=None):
    try:
        req = urllib.request.Request(url, headers=headers, method=method, data=data)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return {"error": e.code, "message": body}
    except Exception as e:
        return {"error": str(e)}

def main():
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    report = {}

    # 1. Check Apps Script projects
    q = "mimeType = 'application/vnd.google-apps.script' and trashed = false"
    url = f"https://www.googleapis.com/drive/v3/files?q={urllib.parse.quote(q)}&fields=files(id,name,modifiedTime)"
    scripts = make_request(url, headers)
    report["script_projects"] = scripts

    # Inspect each script project's content
    script_details = []
    for s in scripts.get("files", []):
        sid = s["id"]
        content_url = f"https://script.googleapis.com/v1/projects/{sid}/content"
        c = make_request(content_url, headers)
        script_details.append({
            "id": sid,
            "name": s.get("name"),
            "modified": s.get("modifiedTime"),
            "files": [f.get("name") for f in c.get("files", [])] if "files" in c else c
        })
    report["script_details"] = script_details

    # 2. Check Form details & responses
    form_id = "1-dRLV-vJ-VyzFOmFh5ASz8bpxiYvI0Uez3Qy_Xal-l0"
    form_info = make_request(f"https://forms.googleapis.com/v1/forms/{form_id}", headers)
    report["form_title"] = form_info.get("info", {}).get("title") if "info" in form_info else form_info
    
    # Form responses
    form_resp = make_request(f"https://forms.googleapis.com/v1/forms/{form_id}/responses", headers)
    if "responses" in form_resp:
        report["total_form_responses"] = len(form_resp["responses"])
        report["recent_form_responses"] = form_resp["responses"][-3:]
    else:
        report["form_responses_error"] = form_resp

    # 3. Check Spreadsheet
    sheet_id = "1pCu_M1vUBYjKhiS3GwjG0l6fwYiRQDsDcPxuNYVT_hk"
    sheet_meta = make_request(f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?fields=sheets.properties", headers)
    if "sheets" in sheet_meta:
        report["sheets_tabs"] = [sh["properties"]["title"] for sh in sheet_meta["sheets"]]
        first_sheet = sheet_meta["sheets"][0]["properties"]["title"]
        rows = make_request(f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{urllib.parse.quote(first_sheet)}!A1:Z10", headers)
        report["sheet_sample_rows"] = rows.get("values", [])
    else:
        report["sheet_error"] = sheet_meta

    # 4. Check Badges Folder in Drive
    q_folder = "name = 'JSB 2027 — Badges Officiels' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    folders = make_request(f"https://www.googleapis.com/drive/v3/files?q={urllib.parse.quote(q_folder)}", headers)
    report["badge_folders"] = folders
    if folders.get("files"):
        folder_id = folders["files"][0]["id"]
        files_in_folder = make_request(f"https://www.googleapis.com/drive/v3/files?q='{folder_id}'+in+parents+and+trashed=false&fields=files(id,name,createdTime)&pageSize=10", headers)
        report["files_in_badge_folder"] = files_in_folder

    # 5. Check Gmail recent sent & inbox messages
    sent_list = make_request("https://gmail.googleapis.com/gmail/v1/users/me/messages?q=in:sent&maxResults=5", headers)
    sent_msgs = []
    for m in sent_list.get("messages", []):
        msg = make_request(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{m['id']}?format=metadata&metadataHeaders=Subject&metadataHeaders=To&metadataHeaders=Date", headers)
        headers_dict = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        sent_msgs.append(headers_dict)
    report["recent_sent_emails"] = sent_msgs

    inbox_list = make_request("https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=5", headers)
    inbox_msgs = []
    for m in inbox_list.get("messages", []):
        msg = make_request(f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{m['id']}?format=metadata&metadataHeaders=Subject&metadataHeaders=From&metadataHeaders=Date", headers)
        headers_dict = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        inbox_msgs.append(headers_dict)
    report["recent_inbox_emails"] = inbox_msgs

    with open("scripts/diagnostic_output.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("Diagnostic completed! Results written to scripts/diagnostic_output.json")

if __name__ == "__main__":
    main()
