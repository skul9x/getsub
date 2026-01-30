from core.crypto_utils import CryptoUtils
import json
import base64

def compare_structures():
    # 1. Working Payload from cURL 2 (ID: "BS72fMpsGjk")
    working_payload_b64 = "eyJjdCI6ImJidytNMXRqUVk2ZUNjTjJUdnpwQmc9PSIsIml2IjoiNzgwZTJlMzRmZjkzZTZkMmQ5ZDM2YjUxMzQ1YTY5MzAiLCJzIjoiZWI2NzAxODJhNjRmZjVlMCJ9"
    
    # 2. Failed Payload from User (ID: "hAXrzWSRgYY")
    failed_payload_b64 = "eyJjdCI6IkU0K0xIS0tRdmxoZXpCbVJ1cC93QWc9PSIsIml2IjoiMzM5YzQ3MTlhOGMzY2M2ZTMxOWQ1YmJhYzkwMGNiY2IiLCJzIjoiODc5NTgxZjRmZWQyMjZiMCJ9"
    
    print("\n--- Structural Analysis ---")
    
    def analyze(name, payload):
        print(f"\nAnalyzing {name}:")
        try:
            json_str = base64.b64decode(payload).decode('utf-8')
            print(f"  JSON Raw: {json_str}")
            parsed = json.loads(json_str)
            print(f"  Keys: {list(parsed.keys())}")
            print(f"  IV Length: {len(parsed['iv'])}")
            print(f"  Salt Length: {len(parsed['s'])}")
        except Exception as e:
            print(f"  Error: {e}")

    analyze("Working Payload", working_payload_b64)
    analyze("Failed Payload", failed_payload_b64)
    
compare_structures()
