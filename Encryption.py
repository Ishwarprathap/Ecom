from Crypto.Cipher import AES
import base64
import os

# AES Encryption and Decryption Setup
key = os.urandom(16)  # 16-byte key for AES-128, 24-byte for AES-192, 32-byte for AES-256
iv = os.urandom(16)   # 16-byte initialization vector

# Function to encrypt data
def encrypt_data(data):
    """Encrypts data using AES encryption."""
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_data = cipher.encrypt(data.encode())  # data must be in bytes, so encode it
    return base64.b64encode(encrypted_data).decode()  # Encode as base64 to store in the DB

# Function to decrypt data
def decrypt_data(encrypted_data):
    """Decrypts data using AES decryption."""
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted_data = cipher.decrypt(base64.b64decode(encrypted_data.encode()))  # Decode from base64 first
    return decrypted_data.decode()  # Decrypted data is a string

# Card
if __name__ == "__main__":
    card_data = "4111-1111-1111-1111"  
    encrypted_card = encrypt_data(card_data)
    print(f"Encrypted: {encrypted_card}")

    # Save encrypted_card into the database...

    decrypted_card = decrypt_data(encrypted_card)
    print(f"Decrypted: {decrypted_card}")
