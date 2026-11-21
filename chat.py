import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

api_key = os.environ.get("HEX_API_KEY")
if not api_key:
    sys.exit("Set HEX_API_KEY before running this example.")

model = sys.argv[1] if len(sys.argv) > 1 else "glm-5.3-abliterated"
payload = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Explain why a development server uses a local port."}
    ],
    "max_tokens": 256,
}
request = Request(
    "https://api.hexapi.io/v1/chat/completions",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    method="POST",
)
try:
    with urlopen(request, timeout=90) as response:
        completion = json.load(response)
except HTTPError as error:
    sys.exit(f"HEX returned HTTP {error.code}. See https://hexapi.io/docs for help.")
except (URLError, TimeoutError):
    sys.exit("Could not complete the request to HEX.")

print(completion["choices"][0]["message"].get("content") or "(No text returned)")
