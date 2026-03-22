#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSTR Ghost Obfuscator Module - SAFE VERSION
No syntax errors, minimal obfuscation for stability
"""

import base64
import zlib
import random
import string


def obfuscate_python(code):
    """
    Safe obfuscation that won't break Python syntax
    Returns original code if anything fails
    """
    try:
        # Simple compression only - most stable
        compressed = zlib.compress(code.encode())
        compressed_b64 = base64.b64encode(compressed).decode()
        
        # Clean wrapper without nested imports
        wrapper = f"""
import zlib, base64
exec(zlib.decompress(base64.b64decode('{compressed_b64}')))
"""
        return wrapper
        
    except Exception as e:
        # Return original code on any error
        print(f"Obfuscation skipped: {e}")
        return code


def light_obfuscate(code):
    """
    Light obfuscation - rename variables only
    """
    try:
        import re
        
        def random_name():
            return ''.join(random.choices(string.ascii_lowercase, k=8))
        
        # Find variable names (simplified)
        var_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        keywords = {'def', 'class', 'import', 'from', 'if', 'else', 'elif', 'for', 
                    'while', 'return', 'try', 'except', 'finally', 'with', 'as',
                    'lambda', 'yield', 'global', 'nonlocal', 'assert', 'pass',
                    'break', 'continue', 'raise', 'del', 'and', 'or', 'not',
                    'in', 'is', 'None', 'True', 'False', 'print', 'exec', 'eval'}
        
        # Find all identifiers
        identifiers = set(re.findall(var_pattern, code))
        mapping = {}
        
        for ident in identifiers:
            if ident not in keywords and not ident.startswith('__'):
                mapping[ident] = random_name()
        
        # Replace with mapped names
        for old, new in mapping.items():
            code = re.sub(r'\b' + old + r'\b', new, code)
        
        return code
        
    except Exception as e:
        return code