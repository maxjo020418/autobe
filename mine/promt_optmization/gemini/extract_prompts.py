import json
import re
import os

INPUT_FILE = "gemini/optimized.json"
OUTPUT_DIR = "gemini/prompts"

def extract_prompts():
    if not os.path.exists(INPUT_FILE):
        print(f"File not found: {INPUT_FILE}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Process Messages
    if 'messages' in data:
        for i, msg in enumerate(data['messages']):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            text_content = ""
            if isinstance(content, str):
                text_content = content
            elif isinstance(content, list):
                # Concatenate text parts
                for part in content:
                    if isinstance(part, dict) and part.get('type') == 'text':
                        text_content += part.get('text', '') + "\n"
            
            if not text_content.strip():
                continue

            # Try to extract filename from comment
            match = re.search(r'<!--\s*filename:\s*(.*?)\s*-->', text_content, re.IGNORECASE | re.DOTALL)
            if match:
                filename = match.group(1).strip()
            else:
                filename = f"message_{i}_{role}.md"
            
            # Ensure filename ends with .md
            if not filename.endswith('.md'):
                filename += ".md"

            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(text_content)
            print(f"Extracted: {filename}")

    # 2. Process Tools
    if 'tools' in data:
        for tool in data['tools']:
            func = tool.get('function', {})
            name = func.get('name', 'unnamed_tool')
            filename = f"tool_{name}.md"
            
            output_path = os.path.join(OUTPUT_DIR, filename)
            
            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(f"# Tool: {name}\n\n")
                
                desc = func.get('description', '')
                if desc:
                    f_out.write(f"## Description\n{desc}\n\n")
                
                f_out.write("## Parameter Descriptions\n")
                
                # Recursive function to extract descriptions from schema
                def walk_schema(schema, path=""):
                    if not isinstance(schema, dict):
                        return
                    
                    current_desc = schema.get('description')
                    if current_desc:
                        f_out.write(f"### `{path}`\n")
                        f_out.write(f"{current_desc}\n\n")
                    
                    # Handle properties
                    if 'properties' in schema:
                        for prop_name, prop_schema in schema['properties'].items():
                            new_path = f"{path}.{prop_name}" if path else prop_name
                            walk_schema(prop_schema, new_path)
                    
                    # Handle array items
                    if 'items' in schema:
                        walk_schema(schema['items'], f"{path}[]")
                    
                    # Handle definitions / $defs
                    if '$defs' in schema:
                        for def_name, def_schema in schema['$defs'].items():
                            walk_schema(def_schema, f"$defs.{def_name}")
                    
                    # Handle anyOf, oneOf, allOf
                    for key in ['anyOf', 'oneOf', 'allOf']:
                        if key in schema:
                            for idx, sub_schema in enumerate(schema[key]):
                                # Try to find a name if possible, else index
                                # For $ref, we might not have descriptions here, they are in defs.
                                # But if there is an inline description, we grab it.
                                walk_schema(sub_schema, f"{path}({key}[{idx}])")

                if 'parameters' in func:
                    walk_schema(func['parameters'])
            
            print(f"Extracted: {filename}")

if __name__ == "__main__":
    extract_prompts()