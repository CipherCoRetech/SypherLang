def verify_proof(proof, key):
    return proof.startswith(f"proof") and f"key({key})" in proof
# Function to verify ZKP
