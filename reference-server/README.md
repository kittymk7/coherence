# AOAPI Reference Server

FastAPI implementation of AOAPI v0.1 protocol with ED25519 signed receipts.

## Setup
```bash
pip install -r requirements.txt
```

Generate Ed25519 keypair:
```bash
python -c "from nacl.signing import SigningKey; from nacl.encoding import HexEncoder; k = SigningKey.generate(); print('AOAPI_PRIVATE_KEY=' + k.encode(encoder=HexEncoder).decode()); print('Public:', k.verify_key.encode(encoder=HexEncoder).decode())"
```

Export the private key (32 bytes, 64 hex characters):
```bash
export AOAPI_PRIVATE_KEY="<your_64_char_hex>"
python main.py
```

Quick test with ephemeral key:
```bash
export AOAPI_PRIVATE_KEY="$(python -c "from nacl.signing import SigningKey; from nacl.encoding import HexEncoder; print(SigningKey.generate().encode(encoder=HexEncoder).decode())")"
python main.py
```

## Endpoints

- `GET /.well-known/aoapi.json` - Protocol discovery
- `POST /aoapi/actions/search_patent` - Execute patent search
- `GET /verify` - Verification demo

## Testing
```bash
# Verification demo
curl http://localhost:8000/verify

# Patent search with signed receipt
curl -X POST http://localhost:8000/aoapi/actions/search_patent \
  -H "Content-Type: application/json" \
  -d '{"query":"machine learning","limit":2}'
```