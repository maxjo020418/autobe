const fs = require('fs');
const path = require('path');

// 1. Load the file content
// We read it as a string because 'require()' might fail if the file isn't a valid CommonJS module (it has 'const apiSchema = ...')
const filePath = path.join(process.cwd(), 'pve-apidoc.js');
let fileContent = fs.readFileSync(filePath, 'utf8');

// 2. "Hack" it into valid JSON to parse it safely
// Remove "const apiSchema =" and the trailing ";"
fileContent = fileContent.replace(/^const apiSchema\s*=\s*/, '').replace(/;?\s*$/, '');

let schema;
try {
    schema = JSON.parse(fileContent);
} catch (e) {
    console.error("Failed to parse schema. It might not be strict JSON (e.g. trailing commas or unquoted keys).");
    console.error(e.message);
    process.exit(1);
}

// 3. Recursive Search Function
function findNode(nodes, targetPath) {
    if (!nodes) return null;

    for (const node of nodes) {
        // Normalize schema path: replace {name} with regex pattern [^/]+
        // e.g., "/cluster/replication/{id}" -> "^\/cluster\/replication\/[^/]+$"
        const regexPath = '^' + node.path.replace(/\{[^}]+\}/g, '[^/]+') + '$';
        const regex = new RegExp(regexPath);

        // Check if this node matches
        if (regex.test(targetPath)) {
            // Found a match! Return this node.
            return node;
        }

        // If not a direct match, check if it's a parent path (prefix)
        // e.g. target "/cluster/replication/123" starts with "/cluster"
        // We only dive deeper if the current node's path is a prefix of the target
        // (Simple string check isn't perfect for variables, but good heuristic)
        // Better: Just search all children blindly if we haven't found it yet? 
        // Actually, the structure is a tree. We can just search children recursively.
        
        const found = findNode(node.children, targetPath);
        if (found) return found;
    }
    return null;
}

// 4. Run Search
const target = process.argv[2]; // e.g. "/cluster/replication/100-0"

if (!target) {
    console.log("Usage: node search_schema.js <api_path>");
    console.log("Example: node search_schema.js /cluster/replication/100-0");
    process.exit(0);
}

console.log(`Searching for: ${target}...`);
const result = findNode(schema, target);

if (result) {
    console.log("\n✅ Found Definition:");
    console.log(`Path Template: ${result.path}`);
    if (result.info) {
        console.log("Methods:", Object.keys(result.info).join(", "));
        // Print the first method's description as a sample
        const firstMethod = Object.keys(result.info)[0];
        console.log(`Description (${firstMethod}):`, result.info[firstMethod].description);
        console.log("\nFull Node Info (Truncated):");
        console.log(JSON.stringify(result.info, null, 2).slice(0, 500) + "... (truncated)");
    } else {
        console.log("Node has no 'info' block (intermediate path).");
    }
} else {
    console.error("\n❌ Path not found in schema.");
}
