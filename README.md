# AOAPI v0.1

**Agent-Oriented API Protocol**
Deterministic execution verification layer for LLM-based web agents

---

## Problem

LLM tool-calling works when APIs exist. Most business workflows live in web UIs.

Current approaches fail in production:
- **DOM parsing** → brittle to UI changes
- **Screenshot agents** → expensive, unverifiable
- **Manual adaptation** → doesn't scale

AOAPI makes web UI actions callable as tool functions with verifiable receipts.

---

## Protocol

Sites expose actions at `/.well-known/aoapi.json`

Each action returns a **receipt** containing:
```json
{
  "state_hash": "sha256:a3d8f7c2...",
  "signature": "4f92b1a5...",
  "timestamp": "2026-01-04T10:23:11Z",
  "nonce": "7e8f9a2b...",
  "ui_hash": "sha256:d8e9f1a2..."
}
```

**Note:** `state_hash` is computed over stable JSON serialization (sorted keys, no whitespace) of the action results (excluding receipt metadata). This enables deterministic verification across implementations.

Agents treat results as untrusted until receipt verification passes.

---

## Example: Patent Search

**Descriptor** (`/.well-known/aoapi.json`):
```json
{
  "aoapi_version": "0.1",
  "actions": [{
    "name": "search_patent",
    "method": "POST",
    "path": "/aoapi/actions/search_patent",
    "input_schema": {
      "type": "object",
      "properties": {
        "query": {"type": "string"},
        "assignee": {"type": "string"},
        "limit": {"type": "integer", "default": 10, "maximum": 50}
      },
      "required": ["query"]
    },
    "verification": {
      "mode": "shadow_ui",
      "receipt_sig": {"alg": "ed25519"}
    }
  }]
}
```

**Action response**:
```json
{
  "results": [
    {"publication_number": "US-2026-0001234", "title": "..."}
  ],
  "receipt": {
    "state_hash": "sha256:a3d8f7c2...",
    "signature": "4f92b1a5...",
    "timestamp": "2026-01-04T10:23:11Z",
    "nonce": "7e8f9a2b..."
  }
}
```

---

## Quick Start
```bash
cd reference-server
pip install -r requirements.txt

# Generate and set keypair
export AOAPI_PRIVATE_KEY="$(python -c "from nacl.signing import SigningKey; from nacl.encoding import HexEncoder; print(SigningKey.generate().encode(encoder=HexEncoder).decode())")"
python main.py
```

Visit:

- Discovery: `http://localhost:8000/.well-known/aoapi.json`
- Verification demo: `http://localhost:8000/verify`

Test search:
```bash
curl -X POST http://localhost:8000/aoapi/actions/search_patent \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "limit": 3}'
```

---

## Repository Contents
```
aoapi/
├── spec/
│   ├── minipaper.pdf          # technical spec (emailed)
│   └── aoapi.schema.json      # JSON schema for descriptors (emailed) 
├── examples/
│   └── patent-search/
│       └── aoapi.json         # USPTO reference descriptor
└── reference-server/
    ├── main.py                # FastAPI implementation
    ├── crypto.py              # ED25519 signing & verification
    └── requirements.txt
```
spec/ contains the normative AOAPI specification (minipaper.pdf) and the canonical JSON Schema (aoapi.schema.json).
---

## Integration Patterns

### OpenAI (Tool Calling)

AOAPI actions map 1:1 to function tools. Receipts included in tool results.

### Anthropic (Computer Use)

Protocol-first execution (0 vision tokens), graceful fallback to Computer Use with receipt wrapping.

---

## Validation Scenario

**USPTO patent search** chosen because:

- Complex, brittle UIs
- Multi-step workflows (10-20 actions)
- Legal compliance requirements
- Determinism is non-negotiable

Demonstrates receipt chaining across long-horizon tasks without perception ambiguity.

---

## Status

- **Spec**: v0.1 (stable draft)
- **Reference server**: functional (mock results)
- **Validation**: USPTO descriptor + receipt flow demonstrated

---

## License

MIT License

Protocol specification and reference implementation are open.

Vertical-specific adapters and verification strategies released separately.

---

## Contact

**Monica King, J.D.**
Founder, Coherence Protocol

[LinkedIn] | [email]

---

## Design Principles

This protocol does not:

- Promise autonomous agents
- Claim to solve AGI
- Benchmark against synthetic scenarios
- Market to non-technical audiences

AOAPI is infrastructure. Execution and domain depth still matter.