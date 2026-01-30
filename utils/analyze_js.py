import re
import requests
import os
import glob
import time

RESPONSE_FILE = r"c:\Users\Admin\Desktop\Test_code\GetSub\cURL+Response\Response_1.txt"
BASE_URL = "https://downsub.com"
OUTPUT_DIR = "js_analysis"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find /js/*.js (quoted or unquoted)
    # Match /js/....js until space, >, ", or '
    matches = re.findall(r'(/js/[a-zA-Z0-9\.\-_]+\.js)', content)
    
    unique_js = set(matches)
    print(f"Found {len(unique_js)} JS files: {unique_js}")

    found_files = []

    for js_path in unique_js:
        url = BASE_URL + js_path
        filename = js_path.split("/")[-1]
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Don't download if exists to save time
        if not os.path.exists(filepath):
            print(f"Downloading {url}...")
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(r.content)
                    found_files.append(filepath)
                else:
                    print(f"Failed to download {url}: {r.status_code}")
                time.sleep(0.5) # Be nice
            except Exception as e:
                print(f"Error downloading {url}: {e}")
        else:
            print(f"Skipping {filename} (already exists)")
            found_files.append(filepath)

    # Analyze
    keywords = ["get-info", "encrypt", "AES", "downsub.com", "CryptoJS", "secret", "password", "KEY", "IV"]
    
    print("\n--- ANALYSIS ---")
    for filepath in found_files:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # print(f"Scanning {filepath}...")
        for kw in keywords:
            if kw in content:
                # If it's a very common word like 'password' appearing in UI text, skip or be careful
                # But we want to find code
                idx = content.find(kw)
                # Check if it looks like code?
                start = max(0, idx - 150)
                end = min(len(content), idx + 150)
                snippet = content[start:end].replace('\n', ' ')
                
                # Filter out likely false positives (e.g. text)
                if "AES" in kw or "get-info" in kw or ("encrypt" in kw and "function" in snippet):
                     print(f"\n[MATCH] File: {os.path.basename(filepath)} | Keyword: '{kw}'")
                     print(f"    Context: ...{snippet}...")

if __name__ == "__main__":
    main()
