from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)


def create_connection():
    connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="root",
        host="192.168.20.97",
        port="5432"
    )
    return connection


@app.route('/api/upload', methods=['POST'])
def upload_video():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        video_data = request.json.get('video_data')

        if video_data:
            insert_query = "INSERT INTO videos (video_data) VALUES (%s) RETURNING id"
            cursor.execute(insert_query, (psycopg2.Binary(video_data),))
            connection.commit()

            new_video_id = cursor.fetchone()[0]
            return jsonify({"message": "Video uploaded successfully", "video_id": new_video_id})

        return "Video data not found in request", 400

    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
