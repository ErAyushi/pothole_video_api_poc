from flask import Flask, Response, jsonify, request
import json
import requests

app = Flask(__name__)

# Define a dictionary to store received pothole information
received_pothole_info = {}

@app.route('/send_pothole_info', methods=['POST'])
def send_pothole_info():
    external_api_url = "http://192.168.20.97:5002/test"

    try:
        response = requests.get(external_api_url)

        if response.status_code == 200:
            received_data = response.json()
            print("Received Data from External API:", received_data)

            received_pothole_info['pothole_count'] = received_data.get('pothole_count')
            # received_pothole_info['bounding_boxes'] = received_data.get('bounding_boxes')

            return received_data, 200
        else:
            print("Failed to fetch data from External API")
            print("Response Content:", response.text)  # Print the response content
            return jsonify({"message": "Failed to fetch data from External API"}), 500

    except requests.exceptions.RequestException as e:
        print("Error during API request:", e)
        return jsonify({"message": "Error during API request"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
