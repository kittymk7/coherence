import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from crypto import ReceiptSigner

app = FastAPI(title="AOAPI Reference Server")

# Infrastructure discipline: No hardcoded keys
PRIVATE_KEY = os.getenv("AOAPI_PRIVATE_KEY")
if not PRIVATE_KEY:
    raise RuntimeError(
        "AOAPI_PRIVATE_KEY environment variable must be set. "
        "Generate a key with: python -c 'from nacl.signing import SigningKey; "
        "from nacl.encoding import HexEncoder; print(SigningKey.generate().encode(encoder=HexEncoder).decode())'"
    )

signer = ReceiptSigner(PRIVATE_KEY)


class SearchPatentRequest(BaseModel):
    query: str
    assignee: str | None = None
    inventor: str | None = None
    limit: int = Field(default=10, ge=1, le=50)


@app.get("/.well-known/aoapi.json")
async def aoapi_descriptor():
    """AOAPI discovery endpoint."""
    return {
        "aoapi_version": "0.1",
        "service": {
            "name": "Reference Patent Portal",
            "base_url": "http://localhost:8000"
        },
        "actions": [{
            "name": "search_patent",
            "method": "POST",
            "path": "/aoapi/actions/search_patent",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "assignee": {"type": "string"},
                    "inventor": {"type": "string"},
                    "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50}
                },
                "required": ["query"]
            },
            "verification": {
                "mode": "shadow_ui",
                "receipt_sig": {"alg": "ed25519"}
            }
        }]
    }


@app.post("/aoapi/actions/search_patent")
async def search_patent(req: SearchPatentRequest):
    """Execute patent search and return signed receipt."""

    results = [
        {
            "publication_number": f"US-2026-{i:07d}",
            "title": f"Method and System for {req.query}",
            "assignee": req.assignee or "Example Corp",
            "filing_date": "2026-01-04",
            "abstract": f"A system for implementing {req.query}..."
        }
        for i in range(1, min(req.limit, 3) + 1)
    ]

    receipt = signer.sign(results)

    return {
        "results": results,
        "receipt": receipt
    }


@app.get("/verify")
async def verify_demo():
    """Demo endpoint showing receipt verification."""
    test_results = [{"id": "test"}]
    receipt = signer.sign(test_results)

    is_valid = signer.verify_receipt(receipt)

    return {
        "demo": "receipt_verification",
        "receipt": receipt,
        "verification_passed": is_valid
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 AOAPI Reference Server")
    print("📍 Discovery: http://localhost:8000/.well-known/aoapi.json")
    print("🔍 Search: POST http://localhost:8000/aoapi/actions/search_patent")
    print("✅ Verify: http://localhost:8000/verify")
    uvicorn.run(app, host="0.0.0.0", port=8000)
