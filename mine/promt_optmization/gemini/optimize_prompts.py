import json
import re
import os
import sys

INPUT_FILE = "2025-12-25T18-12-09-207307.json"
OUTPUT_FILE = "gemini/optimized.json"

def optimize_text(text):
    if not isinstance(text, str):
        return text
    
    # Simple regex first to test
    # 1. Remove Emojis
    # Using a simplified safe regex for now to avoid potential encoding crash
    text = re.sub(r'[^\x00-\x7F]+', '', text) # Aggressive removal of non-ascii for debugging
    # Only if I want to strip ALL non-ascii. The prompt had emojis.
    # But wait, earlier I used sophisticated regex.
    # Let's try the sophisticated one again but print before/after if needed.
    # Actually, let's stick to the sophisticated one but catch errors.
    
    # 2. Fix All-Caps words
    whitelist = {
        "API", "JSON", "HTTP", "HTTPS", "URL", "URI", "UUID", "ID", "DTO", 
        "GET", "POST", "PUT", "PATCH", "DELETE", "CRUD", "SQL", "NOSQL", 
        "REST", "SDK", "CLI", "UI", "UX", "HTML", "CSS", "JS", "TS", "JWT",
        "ISO", "UTC", "PRISMA", "NESTJS", "NODE", "COMMON", "NOT", "OR", "AND",
        "NULL", "TRUE", "FALSE", "UNDEFINED", "VOID", "STRING", "NUMBER", "BOOLEAN"
    }
    
    def capitalization_replacer(match):
        word = match.group(0)
        if word in whitelist:
            return word
        return word.capitalize()

    text = re.sub(r'\b[A-Z]{4,}\b', capitalization_replacer, text)
    
    # 3. Text Compression
    replacements = [
        (r'\bIn order to\b', 'To'),
        (r'\bmake sure to\b', 'ensure'),
        (r'\bMake sure to\b', 'Ensure'),
        (r'\bPlease note that\b', 'Note that'),
        (r'\bis required to\b', 'must'),
        (r'\bare required to\b', 'must'),
        (r'\bIt is recommended to\b', 'Recommend:'),
        (r'\bIt is important to\b', 'Must'),
        (r'\bYou are\b', "You're"),
        (r'\bDo not\b', "Don't"),
        (r'\bdo not\b', "don't"),
        (r'\bdoes not\b', "doesn't"),
        (r'\bcan not\b', "can't"),
        (r'\bcannot\b', "can't"),
        (r'\bis going to\b', "will"),
        (r'\n{3,}', '\n\n'),
    ]
    
    for old, new in replacements:
        text = re.sub(old, new, text, flags=re.IGNORECASE)

    return text.strip()

def recursive_optimize(data):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k in ['content', 'description'] and isinstance(v, str):
                new_dict[k] = optimize_text(v)
            else:
                new_dict[k] = recursive_optimize(v)
        return new_dict
    elif isinstance(data, list):
        return [recursive_optimize(item) for item in data]
    else:
        return data

print("Step 1: Start", flush=True)
try:
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Step 2: Loaded JSON. Keys: {list(data.keys())}", flush=True)
    
    optimized_data = recursive_optimize(data)
    print("Step 3: Optimized", flush=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(optimized_data, f, indent=2, ensure_ascii=False)
        
    print(f"Step 4: Saved to {OUTPUT_FILE}", flush=True)
    
except Exception as e:
    print(f"Error: {e}", flush=True)