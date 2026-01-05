import json
import hashlib
import time
import secrets
from datetime import datetime
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError


class ReceiptSigner:
    """Handles cryptographic signing and verification of AOAPI action receipts."""

    def __init__(self, private_key_hex: str):
        self.signing_key = SigningKey(private_key_hex, encoder=HexEncoder)
        self.verify_key = self.signing_key.verify_key

    def sign(self, results: list, ui_digest: str = None) -> dict:
        """Generate signed receipt for action results."""
        # Stable JSON serialization (sorted keys, no whitespace)
        state_hash = hashlib.sha256(
            json.dumps(results, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

        receipt = {
            "state_hash": f"sha256:{state_hash}",
            "ui_hash": ui_digest or "sha256:none",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "nonce": secrets.token_hex(16)
        }

        # Sign the receipt payload
        message = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode("utf-8")
        signature = self.signing_key.sign(message).signature
        receipt["signature"] = signature.hex()

        return receipt

    def verify_receipt(self, receipt: dict, max_age_seconds: int = 60) -> bool:
        """Verify receipt signature and freshness."""
        try:
            sig = bytes.fromhex(receipt["signature"])
            payload = {k: v for k, v in receipt.items() if k != "signature"}
            message = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

            self.verify_key.verify(message, sig)

            ts = datetime.strptime(receipt["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            if (datetime.utcnow() - ts).total_seconds() > max_age_seconds:
                return False

            return True
        except (BadSignatureError, KeyError, ValueError):
            return False
