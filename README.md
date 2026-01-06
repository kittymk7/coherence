# Coherence Protocol

Coherence Protocol is an infrastructure company focused on **execution admissibility for agentic systems**.

As AI systems move from reasoning to action, the failure mode is no longer “incorrect output” but **irreversible execution** — legal filings, financial operations, regulated workflows, and other real-world state changes where probabilistic success is unacceptable.

Coherence Protocol addresses this gap by defining the primitives required to make agent actions **deterministic, verifiable, and auditable**.

---

## What This Repository Is

This is the **public reference repository** for Coherence Protocol.

It exists to publish:

- protocol specifications
- minimal reference implementations
- technical artifacts relevant to execution verification

It is **not** the primary development repository.

Active development, internal tooling, and production systems are maintained in private repositories.

Note: This repository contains a public reference implementation and demo for the AOAPI protocol. It is intended to illustrate protocol behavior, integration patterns, and deployment flow.

Core production systems, internal orchestration, and proprietary components are intentionally not included here.

---

## What We Work On

Coherence Protocol focuses on the **execution layer**, not model intelligence.

Specifically:

- replacing perception-based execution (DOM parsing, vision inference) with protocol-declared actions
- establishing cryptographic or state-based proofs of execution
- defining admissibility standards for high-compliance environments

One example of this work is **AOAPI (Agent-Oriented API)**, a protocol for exposing web-based actions as deterministic, verifiable endpoints for agents.

---
## Quick Start

Install required dependencies
```bash
cd reference-server
pip install -r requirements.txt
```

Generate/set keypair and start server
```bash
export AOAPI_PRIVATE_KEY="$(python -c "from nacl.signing import SigningKey; from nacl.encoding import HexEncoder; print(SigningKey.generate().encode(encoder=HexEncoder).decode())")"
python main.py
```

Sample output
```
🚀 AOAPI Reference Server
📍 Discovery: http://localhost:8000/.well-known/aoapi.json
🔍 Search: POST http://localhost:8000/aoapi/actions/search_patent
✅ Verify: http://localhost:8000/verify
INFO:     Started server process [22504]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Server test
```bash
curl http://localhost:8000/verify
```

Sample output
```
StatusCode        : 200
StatusDescription : OK
Content           : {"demo":"receipt_verification","receipt":{"state_hash":"sha256:405e727 
                    1bcac3a6765dbf81e8696c949ddfcc9d30843173aba1f9b55ad7b40a6","ui_hash":" 
                    sha256:none","timestamp":"2026-01-06T01:52:14Z","nonce":"c55...        
RawContent        : HTTP/1.1 200 OK
                    Content-Length: 402
                    Content-Type: application/json
                    Date: Tue, 06 Jan 2026 01:52:13 GMT
                    Server: uvicorn

                    {"demo":"receipt_verification","receipt":{"state_hash":"sha256:405e727 
                    1bca...
Forms             : {}
Headers           : {[Content-Length, 402], [Content-Type, application/json], [Date, Tue,  
                    06 Jan 2026 01:52:13 GMT], [Server, uvicorn]}                          Images            : {}                                                                     InputFields       : {}                                                                     Links             : {}                                                                     
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 402
```
---

## Design Principles

- **Determinism over inference**
    
    Prefer declared contracts to guessed behavior.
    
- **Admissibility over accuracy**
    
    An action must be provably correct, not merely likely correct.
    
- **Verification over retries**
    
    Execution success is established through proofs, not heuristics.
    
- **Protocols before platforms**
    
    Coherence defines interfaces and invariants; it does not operate hosted services.
    

---

## What This Is Not

Coherence Protocol is not:

- a browser automation framework
- a scraping or RPA product
- a hosted agent platform
- a model training company
- a consumer-facing application

---

## Publication Policy

Artifacts in this repository are published **selectively and intentionally**.

There is no public roadmap, no announcement cadence, and no solicitation for contributions at this time.

---

## License

Unless otherwise specified, materials in this repository are released under the MIT License.

---

## Contact

**Monica King, J.D.**
Founder, Coherence Protocol

www.linkedin.com/in/monicaking | monica@coherenceprotocol.co