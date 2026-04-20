from flask import Flask, render_template, request, jsonify, Response
from blockchain_service import service

app = Flask(__name__)

@app.route('/')
def index():
    state = service.get_state()
    return render_template('index.html', chain=state['chain'], valid=state['valid'], difficulty=state['difficulty'], history=state['history'])

@app.route('/api/chain')
def get_chain():
    return jsonify(service.get_state())

@app.route('/api/mine', methods=['POST'])
def mine_block():
    data = request.json.get('data') if request.is_json else request.form.get('data')
    if not data:
        return jsonify({'error': 'data is required'}), 400
    result = service.add_block(data)
    return jsonify({'success': True, 'mine_result': result})

@app.route('/api/validate')
def validate_chain():
    return jsonify({'valid': service.validate()})

@app.route('/api/tamper', methods=['POST'])
def tamper_chain():
    payload = request.json if request.is_json else request.form
    index = int(payload.get('index', -1))
    new_data = payload.get('new_data')
    success = service.tamper_block(index, new_data)
    return jsonify({'success': success})

@app.route('/api/difficulty', methods=['POST'])
def set_difficulty():
    payload = request.json if request.is_json else request.form
    difficulty = int(payload.get('difficulty', 4))
    if service.set_difficulty(difficulty):
        return jsonify({'success': True, 'difficulty': difficulty})
    return jsonify({'success': False, 'error': 'invalid difficulty'}), 400

@app.route('/stream')
def stream():
    def event_stream():
        q = service.attach_listener()
        try:
            while True:
                message = q.get()
                yield f'data: {message}\n\n'
        except GeneratorExit:
            service.detach_listener(q)

    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)