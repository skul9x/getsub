from core.crypto_utils import CryptoUtils
import json

def test_verify_known_payload():
    print("--- Verifying Known Payload ---")
    # Payload from cURL 2
    # https://get-info.downsub.com/eyJjdCI6ImJidytNMXRqUVk2ZUNjTjJUdnpwQmc9PSIsIml2IjoiNzgwZTJlMzRmZjkzZTZkMmQ5ZDM2YjUxMzQ1YTY5MzAiLCJzIjoiZWI2NzAxODJhNjRmZjVlMCJ9
    
    payload = "eyJjdCI6ImJidytNMXRqUVk2ZUNjTjJUdnpwQmc9PSIsIml2IjoiNzgwZTJlMzRmZjkzZTZkMmQ5ZDM2YjUxMzQ1YTY5MzAiLCJzIjoiZWI2NzAxODJhNjRmZjVlMCJ9"
    
    print(f"Payload: {payload}")
    
    try:
        decrypted = CryptoUtils.decrypt(payload)
        print(f"Decrypted successfully: {decrypted}")
        
        # In cURL 1 input was: https://youtu.be/BS72fMpsGjk?si=GroklTRv-c7SqZfE
        # Check if decrypted matches (it might be JSON stringified)
        
        expected_substr = "BS72fMpsGjk"
        if expected_substr in decrypted:
            print("✅ SUCCESS: Decrypted content matches expected video ID.")
        else:
            print("❌ FAILURE: Decrypted content does not match.")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_verify_known_payload()
