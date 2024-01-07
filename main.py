from flask import Flask, request, jsonify
import functions  # Import your functions module

app = Flask(__name__)

@app.route('/solar_panel_calculations', methods=['POST'])
def solar_panel_calculations_api():
    data = request.json
    address = data.get('address')
    if not address:
        return jsonify({"error": "Address is required"}), 400
    result = functions.solar_panel_calculations(address)
    return jsonify(result)

@app.route('/process_solar_data', methods=['POST'])
def process_solar_data_api():
    data = request.json
    address = data.get('address')
    if not address:
        return jsonify({"error": "Address is required"}), 400
    result = functions.process_solar_data(address)
    return jsonify(result)

@app.route('/find_best_solar_installers', methods=['POST'])
def find_best_solar_installers_api():
    data = request.json
    address = data.get('address')
    if not address:
        return jsonify({"error": "Address is required"}), 400
    result = functions.find_best_solar_installers(address)
    return jsonify(result)

@app.route('/create_lead', methods=['POST'])
def create_lead_api():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    address = data.get('address')
    if not all([name, phone, address]):
        return jsonify({"error": "Name, phone, and address are required"}), 400
    result = functions.create_lead(name, phone, address)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)