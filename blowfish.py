from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class BlowfishEncryption:
    def __init__(self, key):
        self.key = key
        self.backend = default_backend()

    def encrypt(self, plaintext):
        iv = os.urandom(8)  # Blowfish uses an 8-byte IV
        cipher = Cipher(algorithms.Blowfish(self.key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return iv + ciphertext

    def decrypt(self, ciphertext):
        iv = ciphertext[:8]  # Blowfish uses an 8-byte IV
        cipher = Cipher(algorithms.Blowfish(self.key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext[8:]) + decryptor.finalize()
        return plaintext