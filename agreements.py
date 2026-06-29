# Contract signing simulation for desktop-to-cloud workflow
import hashlib
import json
import time
from datetime import datetime

class Contract:
    def __init__(self, client, provider, details):
        self.client = client
        self.provider = provider
        self.details = details
        self.created = time.time()
        self.audit_trail = []

    def to_json(self):
        return json.dumps({
            "client": self.client,
            "provider": self.provider,
            "details": self.details,
            "created": self.created
        }, sort_keys=True)

    def compute_hash(self):
        return hashlib.sha256(self.to_json().encode()).hexdigest()

    def sign(self, secret):
        base = self.compute_hash()
        return hashlib.sha256(f"{base}:{secret}".encode()).hexdigest()

    def verify(self, signature, secret):
        expected = self.sign(secret)
        return expected == signature

    def log_event(self, event):
        self.audit_trail.append({
            "event": event,
            "time": datetime.utcnow().isoformat()
        })

def run_demo():
    contract = Contract("UserA", "ServiceB", "Cloud migration agreement")
    contract.log_event("created")

    hash_value = contract.compute_hash()
    signature = contract.sign("secure_key_1")

    contract.log_event("signed")

    print("Contract Hash:", hash_value)
    print("Signature:", signature)
    print("Valid:", contract.verify(signature, "secure_key_1"))

    contract.log_event("verified")
    print("Audit trail length:", len(contract.audit_trail))
    return contract

def print_audit(contract):
    print("Audit Log:")
    for entry in contract.audit_trail:
        print(entry)

def summary(contract):
    print("Summary:")
    print("Client:", contract.client)
    print("Provider:", contract.provider)

def main():
    c = run_demo()
    print_audit(c)
    summary(c)
    print("Process finished")

if __name__ == "__main__":
    main()
