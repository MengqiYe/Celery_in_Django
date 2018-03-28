# camera.py

import os

import cv2
import face_recognition
import imutils
from celery import Celery

from .fn_timer import fn_timer

from hls.config import __RTSP_URL__, COMPRESSION_RATIO, PROCESS_EVERYOTHER_FRAME, NAME_UNKNOWN, __BASE_DIR__
import concurrent.futures


class VideoCamera(object):
    @fn_timer
    def find_jpg(self):
        os.chdir(__BASE_DIR__)
        names_raw = [x.split('.')[0] for x in os.listdir('hls/pic')]
        names = [x.split('_')[0] for x in names_raw]

        for n in names_raw:
            pic = face_recognition.load_image_file('hls/pic/' + n + ".jpg")
            self.add_pic_to_library(n, pic)

        print(f"Find {names_raw.__len__()} pictures.")

    def add_pic_to_library(self, name, pic):
        encodings = face_recognition.face_encodings(pic)
        if encodings.__len__() > 0:
            self.known_face_names.append(name)
            self.known_images.append(pic)
            self.known_face_encodings.append(encodings[0])

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(__RTSP_URL__)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        self.current_user = NAME_UNKNOWN
        self.stopEvent = None
        self.known_face_names = []
        self.known_images = []
        self.known_face_encodings = []

        self.find_jpg()

    def __del__(self):
        self.video.release()

    # @fn_timer
    def get_frame(self, frame):

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        frame_small = imutils.resize(frame, width=int(frame.shape[1] / COMPRESSION_RATIO))

        face_locations = face_recognition.face_locations(frame_small, model='cnn')
        face_encodings = face_recognition.face_encodings(frame_small, face_locations)
        face_names = []
        head_shot = None

        for face_encoding in face_encodings:
            distances = list(face_recognition.face_distance(self.known_face_encodings, face_encoding))
            if min(distances) < 0.35:
                first_match_index = distances.index(min(distances))
                self.current_user = self.known_face_names[first_match_index]
            else:
                self.current_user = NAME_UNKNOWN

            face_names.append(self.current_user)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # top *= COMPRESSION_RATIO
            # right *= COMPRESSION_RATIO
            # bottom *= COMPRESSION_RATIO
            # left *= COMPRESSION_RATIO
            self.face_location = (top, right, bottom, left)

            color = (0, 255, 0)
            if name == NAME_UNKNOWN:
                color = (0, 0, 255)

            cv2.rectangle(frame_small, (left, top), (right, bottom), color, 2)

            cv2.rectangle(frame_small, (left, bottom), (right, bottom + 25), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame_small, name, (left + 6, bottom + 15), font, .5, (255, 255, 255), 1)

        ret, frame_jpeg = cv2.imencode('.jpg', frame_small)

        head_bytes = None
        if head_shot:
            ret, head_shot_jpeg = cv2.imencode('.jpg', head_shot)
            head_bytes = head_shot_jpeg.tobytes()

        return frame_jpeg.tobytes(), head_bytes

    def make_celery(app):
        celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                        broker=app.config['CELERY_BROKER_URL'])
        celery.conf.update(app.config)
        TaskBase = celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask
        return celery
