""" 
Module for encryption and decryption using Vigenere cipher
"""
class Encryption:
    def __init__(self, key):
        self.key = "".join(filter(str.isalpha, key)).lower()
        if not self.key:
            raise ValueError("Key must contain at least one alphabetic character.")
        
    # Mode = 1 for encryption, -1 for decryption
    def crypt(self, text, mode):
        key_idx = 0
        new_text = ""
        
        for char in text:
            if char.isalpha():
                key_char = self.key[key_idx % len(self.key)]
                key_shift = ord(key_char) - ord('a')
                
                if 'a' <= char <= 'z':
                    base = ord('a')
                else:
                    base = ord('A')
                    
                char_code = ord(char) - base
                new_char_code = (char_code + mode * key_shift) % 26
                new_text += chr(new_char_code + base)
                
                key_idx += 1
            else:
                new_text += char
                
        return new_text
    
    def encrypt(self, text):
        return self.crypt(text, 1)
    
    def decrypt(self, text):
        return self.crypt(text, -1)
    