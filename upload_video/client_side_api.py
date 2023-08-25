from flask import Flask, request, jsonify, send_file
import os
import psycopg2
import requests

app = Flask(__name__)
UPLOAD_FOLDER = '/home/ayushisoni/PycharmProjects/video_api/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database configuration
DB_NAME = "postgres",
DB_USER = "postgres",
DB_PASSWORD = "root",
DB_HOST = "192.168.20.97",
DB_PORT = "5432"

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="root",
    host="192.168.20.97",
    port="5432"
)
cursor = connection.cursor()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'title' not in request.form:
        return jsonify({'error': 'Missing file or title'}), 400

    file = request.files['file']
    title = request.form['title']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Insert file name and title into the database
        try:
            cursor.execute("INSERT INTO public.videos (file_name, title) VALUES (%s, %s)", (filename, title))
            connection.commit()
            return jsonify({'message': 'File uploaded successfully'}), 200
        except psycopg2.Error as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {e}'}), 500


@app.route('/videos/<int:video_id>', methods=['GET'])
def get_video(video_id):
    print(f"Received request for video_id: {video_id}")

    try:
        cursor.execute("SELECT file_name FROM public.videos WHERE id = %s", (video_id,))
        result = cursor.fetchone()

        if result:
            video_filename = result[0]
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)

            if os.path.exists(video_path):
                return send_file(video_path, as_attachment=True)
            else:
                return jsonify({'error': 'Video file not found'}), 404
        else:
            return jsonify({'error': 'Video not found'}), 404

    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

