import os
import json
import httpx
import uvicorn
from datetime import datetime
from fastapi import FastAPI, Request, Response
from starlette.background import BackgroundTask
from pathlib import Path

app = FastAPI()

# Configuration
TARGET_URL = os.getenv("TARGET_URL", "https://api.openai.com/v1").rstrip("/")
PORT = int(os.getenv("PORT", "8000"))
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)

async def log_payload(payload: dict):
    """Logs the payload to a file with the current timestamp."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")
        filename = LOGS_DIR / f"{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception as e:
        print(f"Failed to log payload: {e}")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy(request: Request, path: str):
    target_url = f"{TARGET_URL}/{path}"
    
    # Capture body for logging and forwarding
    body = await request.body()
    
    json_payload = None
    if request.method == "POST":
        try:
            # Attempt to parse JSON for logging purposes
            if body:
                json_payload = await request.json()
        except Exception:
            pass

    # Prepare headers for the upstream request
    # Filter out headers that might cause issues (like Host)
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length")}
    
    # Log if it looks like a chat completion (or log all JSON POSTs if preferred, sticking to prompt's implication)
    background_task = None
    if json_payload:
        # You might want to filter stricter for "chat/completions" in path if needed
        # For now, logging all JSON payloads captured by the shim as requested "logs the chat completion payload"
        background_task = BackgroundTask(log_payload, json_payload)

    async with httpx.AsyncClient() as client:
        try:
            proxy_res = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=60.0,
                follow_redirects=True
            )
        except httpx.RequestError as exc:
            return Response(content=f"Proxy Error: {exc}", status_code=502)

    # Log the request info to console
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {request.method} {path} -> {proxy_res.status_code}")

    # Forward the response back to the client
    return Response(
        content=proxy_res.content,
        status_code=proxy_res.status_code,
        headers=dict(proxy_res.headers),
        background=background_task
    )

if __name__ == "__main__":
    print(f"Starting shim on port {PORT}, forwarding to {TARGET_URL}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
