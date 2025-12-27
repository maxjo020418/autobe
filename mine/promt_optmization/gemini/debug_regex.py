import re

text = "Critical: This MUST be a SINGLE string value. NOT an array."
whitelist = {"NOT", "ARRAY"}

def capitalization_replacer(match):
    word = match.group(0)
    if word in whitelist:
        return word
    return word.capitalize()

text = re.sub(r'\b[A-Z]{4,}\b', capitalization_replacer, text)
print(text)
