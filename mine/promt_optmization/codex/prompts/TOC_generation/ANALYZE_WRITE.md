<!-- filename: ANALYZE_WRITE.md -->
 # analyze + write

 goal: produce one comprehensive document that backend developers can implement from. no iterations.

 process:
 - use loaded context first.
 - if missing business/flow/rules details, call `process()` to fetch the minimal required analysis files (batch when possible).
 - do not infer requirements from filenames; do not guess.

 tool usage:
 - for preliminary: `process({ thinking, request: { type: "getAnalysisFiles", fileNames } })`.
 - for final: `process({ thinking, request: { type: "complete", plan, content } })`.
 - never call `complete` together with preliminary requests.

 thinking:
 - preliminary: state what is missing and why it blocks writing.
 - completion: state what you wrote and why inputs are sufficient.
