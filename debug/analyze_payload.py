from core.crypto_utils import CryptoUtils
import base64
import json

def analyze_payload():
    # Payload from User's error
    # https://get-info.downsub.com/eyJjdCI6IkU0K0xIS0tRdmxoZXpCbVJ1cC93QWc9PSIsIml2IjoiMzM5YzQ3MTlhOGMzY2M2ZTMxOWQ1YmJhYzkwMGNiY2IiLCJzIjoiODc5NTgxZjRmZWQyMjZiMCJ9
    
    encoded_payload = "eyJjdCI6IkU0K0xIS0tRdmxoZXpCbVJ1cC93QWc9PSIsIml2IjoiMzM5YzQ3MTlhOGMzY2M2ZTMxOWQ1YmJhYzkwMGNiY2IiLCJzIjoiODc5NTgxZjRmZWQyMjZiMCJ9"
    
    print(f"Analyzing Payload: {encoded_payload}")
    
    try:
        decrypted = CryptoUtils.decrypt(encoded_payload)
        print(f"✅ Decrypted Content: {decrypted}")
        print(f"Type: {type(decrypted)}")
        
        # Check if it looks like a valid video ID
        # Valid ID: BS72fMpsGjk (11 chars)
        # Or URL
        
    except Exception as e:
        print(f"❌ Decryption Failed: {e}")

if __name__ == "__main__":
    analyze_payload()
