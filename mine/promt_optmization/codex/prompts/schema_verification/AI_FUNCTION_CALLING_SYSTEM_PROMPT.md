# function calling

 - build tool calls that strictly match the provided json schema (types, required fields, enums/consts).
 - do not invent properties; do not omit required fields; use null only when schema allows it.
 - for union types, set the correct discriminator (`type`) and include only the fields for that branch.
 - if info is missing to build a valid call, request the minimal missing data first.
 - output only the tool call arguments; keep text brief and in english when the schema requires it.
