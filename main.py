import psycopg2

# Connect to the database
connection = psycopg2.connect(
    database="postgres", user="postgres", password="root", host="192.168.20.97", port="5432")
cursor = connection.cursor()

# Query to retrieve video records
select_query = "SELECT file_name, content_type FROM videos"
cursor.execute(select_query)
records = cursor.fetchall()

# Path of the video file you inserted
inserted_video_path = "/home/ayushisoni/Documents/cv/video_dataset/mixkit-potholes-in-a-rural-road-25208-medium (online-video-cutter.com).mp4"

# Check if the inserted video file path is in the records
if any(record[0] == inserted_video_path for record in records):
    print("Video file has been successfully stored in the database.")
else:
    print("Video file was not found in the database.")

cursor.close()
connection.close()
