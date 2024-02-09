from flask import Flask, request, jsonify
import functions  # Import your functions module
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {str(e)}")
    return jsonify({"error": "An internal error occurred"}), 500

# Your existing endpoints with minor modifications
@app.route('/solar_panel_calculations', methods=['POST'])
def solar_panel_calculations_api():
    data = request.json
    address = data.get('address')
    if not address:
        return jsonify({"error": "Address is required"}), 400
    try:
        result = functions.solar_panel_calculations(address)
        return jsonify(result)
    except Exception as e:
        handle_exception(e)

@app.route('/process_solar_data', methods=['POST'])
def process_solar_data_api():
    data = request.json
    address = data.get('address')
    monthly_electrical_bill = data.get('monthly_electrical_bill')
    if not address:
        return jsonify({"error": "Address is required"}), 400
    if not monthly_electrical_bill:
        return jsonify({"error": "monthly_electrical_bill is required"}), 400
    try:
        result = functions.process_solar_data(address, monthly_electrical_bill)
        return jsonify(result)
    except Exception as e:
        handle_exception(e)


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)