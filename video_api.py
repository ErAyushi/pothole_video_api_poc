from flask import Flask, request, jsonify, send_file
import psycopg2
from flask_cors import CORS
import io
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


@app.route('/api/videos/<int:video_id>', methods=['GET'])
def get_video_by_id(video_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Query to retrieve video data by video_id
        select_query = "SELECT video_data FROM videos WHERE id = %s"
        cursor.execute(select_query, (video_id,))
        record = cursor.fetchone()

        if record:
            video_data = record[0]
            video_file = io.BytesIO(video_data.tobytes())
            return send_file(video_file, mimetype='video/mp4')
        else:
            return "Video not found", 404

    except Exception as e:
        return str(e), 500


# http://127.0.0.1:5000/api/videos/1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

