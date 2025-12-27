import os
print("Hello from test script")
try:
    with open("2025-12-25T18-12-09-207307.json", 'r') as f:
        print("File opened successfully")
        content = f.read(100)
        print(f"Read content: {content}")
except Exception as e:
    print(f"Error: {e}")
