from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Blockchain RPC URL
BLOCKCHAIN_RPC_URL = "http://localhost:8545"

@app.route('/faucet', methods=['POST'])
def faucet():
    address = request.json.get('address')
    if not address:
        return jsonify({"error": "Address is required"}), 400
    
    # Define the faucet amount (test tokens)
    faucet_amount = 100

    # Make a request to transfer tokens to the address
    transfer_data = {
        "sender": "faucet_address",  # Replace with faucet wallet address
        "receiver": address,
        "amount": faucet_amount
    }

    response = requests.post(f"{BLOCKCHAIN_RPC_URL}/transfer", json=transfer_data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
