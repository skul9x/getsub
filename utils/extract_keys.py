import re

JS_FILE = r"c:\Users\Admin\Desktop\Test_code\GetSub\js_analysis\main.8729c32e14153e3d9d63.js"

def main():
    try:
        with open(JS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("File not found.")
        return

    # Find $encode function
    # t.prototype.$encode=function(t,e){if(!t)return!1;var n=Dt.AES.encrypt(JSON.stringify(t),e||Bt,{format:Mt}).toString();return Pt(n).trim()}
    
    # We need to find 'Bt' and 'Mt'.
    # Since it's minified 'Bt' variable name might change in different builds but here it is 'Bt'.
    # We look for definition: var Bt="..."; or const Bt="..."; or Bt="..."; or ,Bt="...";
    
    # Heuristic: Find the $encode definition first to confirm variable names
    encode_match = re.search(r'\$encode\s*=\s*function\([a-zA-Z0-9,]+\)\{.*AES\.encrypt\([^,]+,([a-zA-Z0-9]+)\|\|([a-zA-Z0-9]+),\{format:([a-zA-Z0-9]+)\}\)', content)
    
    if encode_match:
        print("Found $encode pattern!")
        # e || Bt
        # 1st group: var e (context arg)
        # 2nd group: default key var name (Bt)
        # 3rd group: format var name (Mt)
        
        arg_name = encode_match.group(1)
        key_var_name = encode_match.group(2)
        fmt_var_name = encode_match.group(3)
        
        print(f"Key Variable: {key_var_name}")
        print(f"Format Variable: {fmt_var_name}")
        
        # Now find the values
        # Regex for 'var Bt="sometext"' or ',Bt="sometext"'
        
        # Search for string definition
        key_pattern = r'[,\s]' + re.escape(key_var_name) + r'\s*=\s*(["\'])(.*?)\1'
        key_match = re.search(key_pattern, content)
        
        if key_match:
            print(f"KEY FOUND: {key_match.group(2)}")
        else:
            print(f"Key definition for {key_var_name} not found.")

        # Search for Pt (Post process)
        # return Pt(n).trim()
        pt_match = re.search(r'return\s+([a-zA-Z0-9]+)\(n\)\.trim\(\)', content)
        if pt_match:
            pt_func_name = pt_match.group(1)
            print(f"PostProcess Function: {pt_func_name}")
            # Try to find what it does. Likely replace + /
            pt_def_match = re.search(r'function\s+' + re.escape(pt_func_name) + r'\([a-zA-Z0-9]+\)\{return.*\}', content)
            if pt_def_match:
                 print(f"PostProcess Def: {pt_def_match.group(0)}")
    
    else:
        print("Strict $encode pattern not found. Trying loose search for 'Bt' if hardcoded.")
        # Fallback: Just look for 'Bt="..."' if we trust the previous grep
        # Based on previous grep: e||Bt
        # Let's assume key var is 'Bt' from previous output logs (if that was consistent)
        # Previous log: ...n=Dt.AES.encrypt(JSON.stringify(t),e||Bt,{format:Mt})...
        
        print("Searching for definitions of 'Bt'...")
        # Since it is minified, it could be `...,Bt="wg8234...",...`
        # Try to find any string assignment to Bt
        matches = re.findall(r'Bt=(["\'])(.*?)\1', content)
        for m in matches:
            print(f"Possible Key: {m[1]}")

if __name__ == "__main__":
    main()
