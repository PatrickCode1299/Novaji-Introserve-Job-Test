import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import binascii


def encrypt_aes_256_cbc_pkcs7(text, key, iv):
  
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()
    
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
   
    hex_encrypted = binascii.hexlify(encrypted_data).decode('utf-8')
    base64_encrypted = base64.b64encode(encrypted_data).decode('utf-8')
    
    return hex_encrypted, base64_encrypted


def decrypt_aes_256_cbc_pkcs7(ciphertext, key, iv, input_format='hex'):
    
    if input_format == 'hex':
        encrypted_data = binascii.unhexlify(ciphertext)
    elif input_format == 'base64':
        encrypted_data = base64.b64decode(ciphertext)
    else:
        raise ValueError("Unsupported format. Use 'hex' or 'base64'.")
   
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    
    return decrypted_data.decode('utf-8')


if __name__ == "__main__":
  
    key = os.urandom(32)  
    iv = os.urandom(16)   
    
    plaintext = "Welcome to Lagos"
    
   
    hex_encrypted, base64_encrypted = encrypt_aes_256_cbc_pkcs7(plaintext, key, iv)
    
    print(f"Original text: {plaintext}")
    print(f"Encrypted (HEX): {hex_encrypted}")
    print(f"Encrypted (Base64): {base64_encrypted}")
    
    
    decrypted_from_hex = decrypt_aes_256_cbc_pkcs7(hex_encrypted, key, iv, input_format='hex')
    print(f"Decrypted from HEX: {decrypted_from_hex}")
    
    
    decrypted_from_base64 = decrypt_aes_256_cbc_pkcs7(base64_encrypted, key, iv, input_format='base64')
    print(f"Decrypted from Base64: {decrypted_from_base64}")
