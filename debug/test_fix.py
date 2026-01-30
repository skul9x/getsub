from core.crypto_utils import CryptoUtils
import json

def test_fix():
    video_id = "hAXrzWSRgYY"
    print(f"Encrypting ID: {video_id}")
    
    # Encrypt
    payload = CryptoUtils.encrypt(video_id)
    print(f"Generated Payload: {payload}")
    
    # Decrypt and check format
    decrypted = CryptoUtils.decrypt(payload)
    print(f"Decrypted: {decrypted}")
    
    # Expectation: "hAXrzWSRgYY" (with quotes inside the string, because it's a JSON string representation)
    # Wait, CryptoUtils.decrypt returns unpad(...).decode(). 
    # If we encrypted '"hAXrzWSRgYY"', decrypted should be '"hAXrzWSRgYY"'.
    
    if decrypted == f'"{video_id}"':
        print("✅ SUCCESS: Decrypted payload contains quotes.")
    else:
        print(f"❌ FAIL: Decrypted payload is '{decrypted}'")

if __name__ == "__main__":
    test_fix()
