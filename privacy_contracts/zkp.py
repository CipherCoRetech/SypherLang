from Crypto.PublicKey import RSA
from prove import generate_proof
from verify import verify_proof

def zero_knowledge_proof(data, private_key, public_key):
    """
    Perform a zero-knowledge proof by generating and verifying proof.

    Parameters:
        data (str): The input data for which the zero-knowledge proof is required.
        private_key (str): The RSA private key in PEM format for generating the proof.
        public_key (str): The RSA public key in PEM format for verifying the proof.

    Returns:
        str: A message indicating if the zero-knowledge proof is valid or not.
    """
    # Generate the proof using the provided private key
    proof = generate_proof(data, private_key)

    # Verify the generated proof using the provided public key
    if verify_proof(proof, public_key):
        return "Valid Zero-Knowledge Proof"
    else:
        return "Invalid Proof"

# Example usage
if __name__ == "__main__":
    # Generate an RSA key pair (for demonstration)
    key_pair = RSA.generate(2048)
    private_key_pem = key_pair.export_key()
    public_key_pem = key_pair.publickey().export_key()

    # Perform zero-knowledge proof
    data = "Confidential transaction details"
    result = zero_knowledge_proof(data, private_key_pem, public_key_pem)
    print(result)
# Zero-Knowledge Proof (ZKP) based privacy contract functions
