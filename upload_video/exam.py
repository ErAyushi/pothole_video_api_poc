import numpy as np
import cv2
from flask import Flask, Response, request
import requests
import geocoder
import time
import os
import json
app = Flask(__name__)





def get_video_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        video_data = response.content
        return video_data
    else:
        return None


video_source = "http://192.168.20.97:5000/videos/latest"
model_weights_path = "/home/ayushisoni/PycharmProjects/video_api/video_main/project_files/yolov4_tiny.weights"
model_config_path = "/home/ayushisoni/PycharmProjects/video_api/video_main/project_files/yolov4_tiny.cfg"
output_video_path = "result.avi"

def generate_frames(video_source, model_weights_path, model_config_path, output_video_path):
    cap = cv2.VideoCapture(video_source)

    # Load the model and set up other parameters here
    cap.open(cv2.CAP_ANY)
    net1 = cv2.dnn.readNet('project_files/yolov4_tiny.weights',
                          'project_files/yolov4_tiny.cfg')
    net1.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net1.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
    model1 = cv2.dnn_DetectionModel(net1)
    model1.setInputParams(size=(640, 480), scale=1 / 255, swapRB=True)

    cap = cv2.VideoCapture(video_source)
    width = cap.get(3)
    height = cap.get(4)
    result = cv2.VideoWriter('result.avi',
                            cv2.VideoWriter_fourcc(*'MJPG'),
                            10, (int(width), int(height)))

    g = geocoder.ip('me')
    result_path = "pothole_coordinates"

    starting_time = time.time()
    Conf_threshold = 0.5
    NMS_threshold = 0.4
    frame_counter = 4
    i = 0
    b = 0

    detected_potholes = {}

    pothole_count = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Pothole detection and annotation logic here

        classes, scores, boxes = model1.detect(
            frame, Conf_threshold, NMS_threshold)
        for (classid, score, box) in zip(classes, scores, boxes):
            label = "pothole"
            x, y, w, h = box

            recarea = w * h
            area = width * height
            # print('test1')
            print(scores)
            if (len(scores) != 0 and scores[0] >= 0.7):
                # print('test2')
                print((recarea / area))
                if ((recarea / area) <= 0.1 and box[1] < 600):
                    is_duplicate = False
                    for pothole_id, prev_pothole in detected_potholes.items():
                        prev_x, prev_y, prev_w, prev_h = prev_pothole
                        if abs(x - prev_x) < 50 and abs(y - prev_y) < 50:
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        pothole_id = i
                        # print(pothole_id)
                        detected_potholes[pothole_id] = (x, y, w, h)
                        i += 1

                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                        cv2.putText(frame, "%" + str(round(scores[0] * 100, 2)) + " " + label,
                                   (box[0], box[1] - 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

                        cv2.imwrite(os.path.join(
                            result_path, 'pothole' + str(pothole_id) + '.jpg'), frame)
                        with open(os.path.join(result_path, 'pothole' + str(pothole_id) + '.txt'), 'w') as f:
                            f.write(str(g.latlng))

                        pothole_count += 1
        detected_potholes_converted = {k: tuple(int(value) for value in values) for k, values in
                                       detected_potholes.items()}
        pothole_info = {
            "pothole_count": pothole_count,
            "bounding_boxes": detected_potholes_converted
        }

        with open('pothole_info.json', 'w') as json_file:
            json.dump(pothole_info, json_file)

        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            break

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/test1', methods=['GET'])
def video_feed():
    global video_source, model_weights_path, model_config_path, output_video_path

    video_source = request.args.get('video_source', video_source)
    model_weights_path = request.args.get('yolov4_tiny.weights', model_weights_path)
    model_config_path = request.args.get('yolov4_tiny.cfg', model_config_path)
    output_video_path = request.args.get('result.avi', output_video_path)

    print("run")

    return Response(generate_frames(video_source, model_weights_path, model_config_path, output_video_path), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=False)