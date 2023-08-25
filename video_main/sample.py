from flask import Flask, Response, jsonify, request
import cv2 as cv
import time
import geocoder
import os
import requests
import numpy as np
import json

app = Flask(__name__)

# def get_video_from_api(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         video_data = response.content
#         return video_data
#     else:
#         return None



# @app.route('/detect_potholes', methods=['GET'])
# def detect_potholes():
#     # return jsonify({'message': 'File uploaded1 successfully'}), 200
#     class_name = []
#
#     # with open(os.path.join("/home/ayushisoni/PycharmProjects/video_api/video_main/project_files", 'obj.names'), 'r') as f:
#     #     class_name = [cname.strip() for cname in f.readlines()]
#
#     video_api_url = "http://192.168.20.97:5000/videos/71"
#     video_data = get_video_from_api(video_api_url)
#
#     if video_data is None:
#         print("Failed to retrieve video from the API.")
#         # return Response("Video not available.", status=404)
#
#     # Convert video data to a numpy array for OpenCV
#     video_np_array = np.frombuffer(video_data, np.uint8)
#     cap = cv.VideoCapture()
#     cap.open(cv.CAP_ANY)
#     net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights',
#                           'project_files/yolov4_tiny.cfg')
#     net1.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
#     net1.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
#     model1 = cv.dnn_DetectionModel(net1)
#     model1.setInputParams(size=(640, 480), scale=1 / 255, swapRB=True)
#
#     cap = cv.VideoCapture(video_api_url)
#     width = cap.get(3)
#     height = cap.get(4)
#     result = cv.VideoWriter('result.avi',
#                             cv.VideoWriter_fourcc(*'MJPG'),
#                             10, (int(width), int(height)))
#
#     g = geocoder.ip('me')
#     result_path = "pothole_coordinates"
#
#     starting_time = time.time()
#     Conf_threshold = 0.5
#     NMS_threshold = 0.4
#     frame_counter = 4
#     i = 0
#     b = 0
#
#     detected_potholes = {}
#
#     pothole_count = 0
#
#     while True:
#         ret, frame = cap.read()
#         frame_counter += 1
#         if ret == False:
#             break
#
#         classes, scores, boxes = model1.detect(
#             frame, Conf_threshold, NMS_threshold)
#         for (classid, score, box) in zip(classes, scores, boxes):
#             label = "pothole"
#             x, y, w, h = box
#
#             recarea = w * h
#             area = width * height
#
#             if (len(scores) != 0 and scores[0] >= 0.7):
#                 if ((recarea / area) <= 0.1 and box[1] < 600):
#                     is_duplicate = False
#                     for pothole_id, prev_pothole in detected_potholes.items():
#                         prev_x, prev_y, prev_w, prev_h = prev_pothole
#                         if abs(x - prev_x) < 50 and abs(y - prev_y) < 50:
#                             is_duplicate = True
#                             break
#
#                     if not is_duplicate:
#                         pothole_id = i
#                         # print(pothole_id)
#                         detected_potholes[pothole_id] = (x, y, w, h)
#                         i += 1
#
#                         cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
#                         cv.putText(frame, "%" + str(round(scores[0] * 100, 2)) + " " + label,
#                                    (box[0], box[1] - 10), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
#
#                         cv.imwrite(os.path.join(
#                             result_path, 'pothole' + str(pothole_id) + '.jpg'), frame)
#                         with open(os.path.join(result_path, 'pothole' + str(pothole_id) + '.txt'), 'w') as f:
#                             f.write(str(g.latlng))
#
#                         pothole_count += 1
#
#         endingTime = time.time() - starting_time
#         fps = frame_counter / endingTime
#         # print(fps)
#         cv.putText(frame, f'FPS: {fps}', (20, 50),
#                    cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
#
#         cv.imshow('frame', frame)
#         result.write(frame)
#         key = cv.waitKey(1)
#         if key == ord('q'):
#             break
#
#
#
#
#     # detected_potholes_converted = {k: tuple(int(value) for value in values) for k, values in detected_potholes.items()}
#     pothole_info = {
#         # "pothole_count": pothole_count,
#         "pothole_count": 25,
#         # "bounding_boxes": detected_potholes_converted
#         "bounding_boxes": 25
#     }
#     json_data = json.dumps(pothole_info)
#
#     # Define API endpoint URL
#     api_url = "http://192.168.20.97:5003/send_pothole_info"
#
#     # Set headers for JSON content
#     headers = {'Content-Type': 'application/json'}
#
#     # Send the JSON data as a POST request
#     response = requests.post(api_url, data=json_data, headers=headers)
#
#     if response.status_code == 200:
#         print("Pothole information sent successfully.")
#     else:
#         print("Failed to send pothole information.")
#         print("Response status code:", response.status_code)
#         print("Response content:", response.content)
#
#     # Return a response after all processing is done
#     # return jsonify({'message': 'File uploaded successfully'}), 200
#     return jsonify(pothole_info), 200
#
#     _, buffer = cv.imencode('.jpg', frame)
#     frame_data = buffer.tobytes()
#     yield (b'--frame\r\n'
#            b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
#     # print("buffer")
#     # print(buffer)
#
#
#
#     cap.release()
#     result.release()
#     cv.destroyAllWindows()
#



def get_video_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        video_data = response.content
        return video_data
    else:
        return None

@app.route('/test', methods=['GET'])
def upload_file():
    video_api_url = "http://192.168.20.97:5000/videos/54"
    video_data = get_video_from_api(video_api_url)

    if video_data is None:
        print("Failed to retrieve video from the API.")
        # return Response("Video not available.", status=404)

    # Convert video data to a numpy array for OpenCV
    video_np_array = np.frombuffer(video_data, np.uint8)
    cap = cv.VideoCapture()
    cap.open(cv.CAP_ANY)
    net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights',
                          'project_files/yolov4_tiny.cfg')
    net1.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    net1.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
    model1 = cv.dnn_DetectionModel(net1)
    model1.setInputParams(size=(640, 480), scale=1 / 255, swapRB=True)

    cap = cv.VideoCapture(video_api_url)
    width = cap.get(3)
    height = cap.get(4)
    result = cv.VideoWriter('result.avi',
                            cv.VideoWriter_fourcc(*'MJPG'),
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



    while True:
        ret, frame = cap.read()
        frame_counter += 1
        if ret == False:
            break

        classes, scores, boxes = model1.detect(
            frame, Conf_threshold, NMS_threshold)
        for (classid, score, box) in zip(classes, scores, boxes):
            label = "pothole"
            x, y, w, h = box

            recarea = w * h
            area = width * height

            if (len(scores) != 0 and scores[0] >= 0.7):
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

                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                        cv.putText(frame, "%" + str(round(scores[0] * 100, 2)) + " " + label,
                                   (box[0], box[1] - 10), cv.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

                        cv.imwrite(os.path.join(
                            result_path, 'pothole' + str(pothole_id) + '.jpg'), frame)
                        with open(os.path.join(result_path, 'pothole' + str(pothole_id) + '.txt'), 'w') as f:
                            f.write(str(g.latlng))

                        pothole_count += 1

        endingTime = time.time() - starting_time
        fps = frame_counter / endingTime
        # print(fps)
        cv.putText(frame, f'FPS: {fps}', (20, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

        cv.imshow('frame', frame)
        result.write(frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break

    detected_potholes_converted = {k: tuple(int(value) for value in values) for k, values in detected_potholes.items()}
    pothole_info = {
        "pothole_count": pothole_count,
        # "pothole_count": 25,
        "bounding_boxes": detected_potholes_converted
        # "bounding_boxes": 25
    }
    json_data = json.dumps(pothole_info)
    print(json_data)



    # Return a response after all processing is done
    # return jsonify({'message': 'File uploaded successfully'}), 200
    # return jsonify(pothole_info), 200
    return json_data, 200

    _, buffer = cv.imencode('.jpg', frame)
    frame_data = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
    # print("buffer")
    # print(buffer)



    cap.release()
    result.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)





