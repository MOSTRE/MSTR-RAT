#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSTR Ghost Cryptor Module - SIMPLE XOR VERSION
No external cryptography dependencies
"""

import os
import base64
import json
import hashlib


class PayloadCryptor:
    def __init__(self, build_key):
        self.build_key = build_key
        
    def _xor_encrypt(self, data, key):
        """Simple XOR encryption"""
        result = bytearray()
        key_bytes = key.encode() if isinstance(key, str) else key
        data_bytes = data.encode() if isinstance(data, str) else data
        for i, byte in enumerate(data_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        return bytes(result)
    
    def _xor_decrypt(self, data, key):
        """Simple XOR decryption (same as encrypt)"""
        result = bytearray()
        key_bytes = key.encode() if isinstance(key, str) else key
        for i, byte in enumerate(data):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        return bytes(result)
    
    def encrypt_payload(self, token, server_id):
        """Encrypt token and server ID using XOR"""
        try:
            # Create machine-specific key
            machine_key = hashlib.md5(os.getenv('COMPUTERNAME', 'unknown').encode()).hexdigest()[:16]
            
            payload = {
                "token": token,
                "server": server_id
            }
            
            payload_json = json.dumps(payload)
            encrypted = self._xor_encrypt(payload_json, machine_key)
            encrypted_b64 = base64.b64encode(encrypted).decode()
            
            return encrypted_b64
            
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt_payload(self, encrypted_data):
        """Decrypt payload"""
        try:
            machine_key = hashlib.md5(os.getenv('COMPUTERNAME', 'unknown').encode()).hexdigest()[:16]
            encrypted = base64.b64decode(encrypted_data)
            decrypted = self._xor_decrypt(encrypted, machine_key)
            payload = json.loads(decrypted.decode())
            return payload.get("token"), payload.get("server")
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")