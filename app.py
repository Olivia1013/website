from flask import Flask, render_template, request, jsonify
from blockchain import Blockchain
from block import Block
import time

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', chain=blockchain.chain, valid=blockchain.is_chain_valid())

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.form.get('data')
    if data:
        new_block = Block(len(blockchain.chain), time.time(), data, "")
        blockchain.add_block(new_block)
    return jsonify({'success': True})

@app.route('/validate')
def validate():
    return jsonify({'valid': blockchain.is_chain_valid()})

@app.route('/tamper', methods=['POST'])
def tamper():
    index = int(request.form.get('index'))
    new_data = request.form.get('new_data')
    if 0 < index < len(blockchain.chain):
        blockchain.chain[index].data = new_data
        blockchain.chain[index].hash = blockchain.chain[index].calculate_hash()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)