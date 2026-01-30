import base64
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class CryptoUtils:
    DEFAULT_KEY = "zthxw34cdp6wfyxmpad38v52t3hsz6c5"

    @staticmethod
    def evp_bytes_to_key(password: str, salt: bytes, key_len: int, iv_len: int):
        """
        Derive Key and IV using OpenSSL EVP_BytesToKey (MD5) strategy, matching CryptoJS.
        """
        dtot = b""
        d = b""
        password_bytes = password.encode('utf-8')
        
        while len(dtot) < (key_len + iv_len):
            s = d + password_bytes + salt
            d = hashlib.md5(s).digest()
            dtot += d
            
        return dtot[:key_len], dtot[key_len:key_len+iv_len]

    @staticmethod
    def encrypt(data_obj, password: str = None) -> str:
        """
        Encrypts a data object (dict or string) into the DownSub payload format.
        Format: Base64( JSONString({ "ct": "...", "iv": "...", "s": "..." }) )
        """
        if password is None:
            password = CryptoUtils.DEFAULT_KEY

        # 1. Prepare Data
        # API expects JSON.stringify(t) as input to encrypt.
        # JSON.stringify("abc") -> "abc" (with quotes)
        # JSON.stringify({"a": 1}) -> {"a":1}
        
        plaintext = json.dumps(data_obj, separators=(',', ':'))

        # 2. Generate Salt
        salt = get_random_bytes(8)

        # 3. Derive Key/IV
        key, iv = CryptoUtils.evp_bytes_to_key(password, salt, 32, 16)

        # 4. Encrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))

        # 5. Format to JSON object components
        ct_b64 = base64.b64encode(ciphertext).decode('utf-8')
        iv_hex = iv.hex()
        s_hex = salt.hex()

        json_payload = json.dumps({
            "ct": ct_b64,
            "iv": iv_hex,
            "s": s_hex
        }, separators=(',', ':'))

        # 6. Final Base64 Encode
        # Downsub uses standard Base64 but maybe URL safe?
        # cURL 2 payload: "eyJjdCI6ImJidytNMXrqUVk2ZUNjTjJUdnp..." using + and / ?
        # cURL 2 payload has '+'. "bbt+M1tj..."
        # So it is standard Base64.
        # However, it is appearing in a URL, so Requests usually handles encoding,
        # or we might need to verify if distinct characters are used.
        # The payload in cURL 2 is simply the path? 
        # https://get-info.downsub.com/eyJjdCI6...
        # Base64 string is directly in the path. Standard Base64 uses '/' which breaks paths.
        # So it MUST be URL-safe Base64 (replace + with -, / with _).
        # WAIT. cURL 2 output shows: "ImJidytNMXRqUVk2ZUNj...". That has a '+'.
        # If it's in the PATH, typically '+' is allowed but '/' is not.
        # Let's check cURL 2 content carefully.
        
        final_b64 = base64.b64encode(json_payload.encode('utf-8')).decode('utf-8')
        return final_b64

    @staticmethod
    def decrypt(payload_b64: str, password: str = None):
        """
        Decrypts a payload to verify correctness.
        """
        if password is None:
            password = CryptoUtils.DEFAULT_KEY

        # 1. Base64 Decode
        # Fix padding if needed
        missing_padding = len(payload_b64) % 4
        if missing_padding:
            payload_b64 += '=' * (4 - missing_padding)
            
        json_str = base64.b64decode(payload_b64).decode('utf-8')
        data = json.loads(json_str)

        ct = base64.b64decode(data['ct'])
        iv = bytes.fromhex(data['iv'])
        salt = bytes.fromhex(data['s'])

        # 2. Derive Key
        key, _ = CryptoUtils.evp_bytes_to_key(password, salt, 32, 16)

        # 3. Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')

        return plaintext
