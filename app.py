from flask import Flask, jsonify, request
from Blockchain.blockchain import Blockchain, Block

app = Flask(__name__)

# Initialize your blockchain - Replace 'your_password' with a real password
blockchain = Blockchain(password="Daju")

@app.route('/add_block', methods=['POST'])
def add_block():
    text = request.json.get('text', '')
    input_password = request.json.get('password', '')
    response = blockchain.add_block(text, input_password)
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.to_json())
    return jsonify(chain_data), 200

# Additional endpoints as needed...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
