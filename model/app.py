from flask import Flask, jsonify
from web3 import Web3

app = Flask(__name__)

infura_api_key = "your_infura_api_key"
infura_url = f"https://sepolia.infura.io/v3/{infura_api_key}"
web3 = Web3(Web3.HTTPProvider(infura_url))

@app.route('/balance/<address>')
def get_balance(address):
    try:
        checksum_address = web3.to_checksum_address(address)
        balance_wei = web3.eth.get_balance(checksum_address)
        balance_eth = web3.from_wei(balance_wei, 'ether')
        return jsonify({'balance': str(balance_eth), 'unit': 'ETH'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)