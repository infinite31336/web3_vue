import time

from flask import Flask, jsonify
from web3 import Web3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

infura_api_key = "63747f7bebcf40f39f95559ebcc5fbdf"
infura_url = f"https://sepolia.infura.io/v3/{infura_api_key}"
web3_provider = Web3(Web3.HTTPProvider(infura_url))


@app.route('/balance/<address>')
def get_balance(address):
    try:
        checksum_address = web3_provider.to_checksum_address(address)
        balance_wei = web3_provider.eth.get_balance(checksum_address)
        balance_eth = web3_provider.from_wei(balance_wei, 'ether')
        print(f"Infura address {address} balance: {balance_eth} ETH")
        return jsonify({'balance': str(balance_eth), 'unit': 'ETH'})
    except Exception as e:
        print(f"Failed to get balance: {e}")
        return jsonify({'balance_error': str(e)}), 400

@app.route('/transactions/<address>')
def get_transactions(address):
    try:
        if not web3_provider.is_address(address):
            return jsonify({"error": "Invalid Ethereum Address"}), 400

        import requests
        api_key = 'YOUR_ETHERSCAN_API_KEY'
        url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        if data['status'] == '1':
            transactions = [
                {
                    "hash": tx['hash'],
                    "value": str(int(tx['value']) / 1e18),  # 轉換為 ETH
                    "time": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(tx['timeStamp'])))
                }
                for tx in data['result'][:5]  # 取前 5 筆
            ]
            print(f"Infura address {address}\ntransactions: {transactions}")
            return jsonify({"transactions": transactions})
        else:
            return jsonify({"transactions": 'No transactions found'})
    except Exception as e:
        print(f"Get address {address} transactions failed\n error: {str(e)}")
        return jsonify({"tx_error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
