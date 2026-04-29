from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from app.services.analyzer import analyze_athlete
from app.services.card_generator import generate_card
from app.services.report_generator import generate_report

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "hub-podium-backend"})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json or {}
    result = analyze_athlete(data)
    return jsonify(result)

@app.route('/generate-card', methods=['POST'])
def card():
    data = request.json or {}
    path = generate_card(data)
    return send_file(path, mimetype='image/png')

@app.route('/generate-report', methods=['POST'])
def report():
    data = request.json or {}
    path = generate_report(data)
    return send_file(path, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
