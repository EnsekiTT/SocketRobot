# -*- coding: utf-8 -*-


import os
import cv2
import threading
import pyaudio
import numpy as np
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver


class SocketRobotNetwork:
    def __init__(self):
        print 'Booting Server'
        self.PORT = 8884

    def set_server(self):
        camera = SocketRobotCamera()
        audio = SocketRobotAudio()
        selfpath = os.path.dirname(__file__)
        settings = {
            "contents_path": os.path.join(selfpath, "contents"),
        }
        contdict = dict(path=settings['contents_path'])
        self.app = tornado.web.Application([
            (r"/camview", HttpCamViewHandler),
            (r"/audlisten", HttpAudListenHandler),
            (r"/camera", CWSHandler, dict(camera=camera)),
            (r"/audio", AWSHandler, dict(audio=audio)),
            (r"/(.*)", tornado.web.StaticFileHandler, contdict),
            ], **settings)

    def listen_start(self):
        print 'Start Listener'
        self.http_server = tornado.httpserver.HTTPServer(self.app)
        self.http_server.listen(self.PORT)
        tornado.ioloop.IOLoop.instance().start()

    def listen_stop(self):
        print 'Stop Listener'
        tornado.ioloop.IOLoop.instance().stop()


class HttpCamViewHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render('contents/camera.html')


class HttpAudListenHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def get(self):
        self.render('contents/audio.html')


class CWSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, camera):
        self.camera = camera
        self.state = True

    def open(self):
        print(self.request.remote_ip, ": connection opened")
        t = threading.Thread(target=self.loop)
        t.setDaemon(True)
        t.start()

    def loop(self):
        while 1:
            jpegFrame = self.camera.get_frame()
            self.write_message(jpegFrame, binary=True)
            if not self.state:
                break

    def on_close(self):
        self.state = False
        self.close()
        print(self.request.remote_ip, ": connection closed")


class AWSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, audio):
        self.audio = audio
        self.state = True

    def open(self):
        print(self.request.remote_ip, ": connection opened")
        t = threading.Thread(target=self.loop)
        t.setDaemon(True)
        t.start()

    def loop(self):
        self.audio.set_stream()
        while 1:
            audioFrame = self.audio.get_frame()
            self.write_message(audioFrame, binary=True)
            if not self.state:
                break

    def on_close(self):
        self.state = False
        self.close()
        print(self.request.remote_ip, ": connection closed")


class SocketRobotAudio:
    def __init__(self):
        print 'Booting Audio'
        self.chunk = 1024
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 1

        self.p = pyaudio.PyAudio()

    def set_stream(self):
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.chunk)

    def get_frame(self):
        data = self.stream.read(self.chunk)
        return data

    def close_stream(self):
        self.stream.close()


class SocketRobotCamera:
    def __init__(self):
        print 'Booting Camera'
        self.cap = cv2.VideoCapture(0)
        self.fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
        self.old_frame = np.zeros((480, 360), np.uint8)

    def get_frame(self):
        frame = self.old_frame
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret is not False:
                self.old_frame = frame

        frame = cv2.resize(frame, (480, 360))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
        frame = frame.reshape(frame.size)
        lineframe = np.uint8(frame).tostring()
        return lineframe

    def quick_show(self):
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret is False:
                break

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    hn = SocketRobotNetwork()
    hn.set_server()
    hn.listen_start()
