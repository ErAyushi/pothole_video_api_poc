import psycopg2

# Connect to the database
connection = psycopg2.connect(
    database="postgres", user="postgres", password="root", host="192.168.20.97", port="5432")
cursor = connection.cursor()

video_path = "/home/ayushisoni/Documents/cv/video_dataset/mixkit-potholes-in-a-rural-road-25208-medium (online-video-cutter.com).mp4"
with open(video_path, "rb") as video_file:
    video_data = video_file.read()

# Insert video data into the database (second video)
insert_query = "INSERT INTO videos (file_name, content_type, video_data) VALUES (%s, %s, %s)"
data = ("/home/ayushisoni/Documents/cv/video_dataset/mixkit-potholes-in-a-rural-road-25208-medium (online-video-cutter.com).mp4", "video/mp4", psycopg2.Binary(video_data))
cursor.execute(insert_query, data)
connection.commit()

cursor.close()
connection.close()

print("Second video stored in the database.")

















# # Create the "videos" table
# create_table_query = '''
#     CREATE TABLE videos (
#         id SERIAL PRIMARY KEY,
#         file_name TEXT NOT NULL,
#         content_type TEXT NOT NULL,
#         video_data BYTEA NOT NULL
#     );
# '''
# cursor.execute(create_table_query)
# connection.commit()
#
# # Read video binary data
# video_path = "/home/ayushisoni/Documents/cv/video_dataset/mixkit-potholes-in-a-rural-road-25208-medium (online-video-cutter.com).mp4"
# with open(video_path, "rb") as video_file:
#     video_data = video_file.read()
#
# # Insert video data into the database
# insert_query = "INSERT INTO videos (file_name, content_type, video_data) VALUES (%s, %s, %s)"
# data = ("/home/ayushisoni/Documents/cv/video_dataset/mixkit-potholes-in-a-rural-road-25208-medium (online-video-cutter.com).mp4", "/home/ayushisoni/Documents/cv/video_dataset", psycopg2.Binary(video_data))
# cursor.execute(insert_query, data)
# connection.commit()
#
# cursor.close()
# connection.close()
#
# print("Video stored in the database.")
