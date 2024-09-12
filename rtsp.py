import numpy as np
import cv2
import threading
import queue

class RTSPStream:
    def __init__(self, source, width=320, height=240, fps=30):
        self.source = source
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = cv2.VideoCapture(self.source)
        self.queue = queue.Queue(maxsize=2)
        self.stopped = False
        self.lock = threading.Lock()
        if not self.cap.isOpened():
            raise ValueError(f"Error: Cannot open video source {self.source}")
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        threading.Thread(target=self.update, args=(), daemon=True).start()

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                frame_resized = cv2.resize(frame, (self.width, self.height))
                if not self.queue.full():
                    self.queue.put(frame_resized)
            else:
                self.reconnect()

    def read(self):
        with self.lock:
            if not self.queue.empty():
                return self.queue.get()
            return None

    def stop(self):
        self.stopped = True
        self.cap.release()

    def reconnect(self):
        with self.lock:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.source)
            if not self.cap.isOpened():
                print(f"Error: Reconnection to {self.source} failed.")

def process_frame(frame1, frame2):
    images = [frame1, frame2]
    image_stitcher = cv2.Stitcher_create()
    status, stitched_img = image_stitcher.stitch(images)
    if status == cv2.Stitcher_OK and stitched_img is not None:
        return stitched_img
    return None

def main():
    source1 = "rtsp://<your_ip>:<port>/ch01.264" 
    source2 = "rtsp://<your_ip>:<port>/ch01.264"

    try:
        stream1 = RTSPStream(source1, width=320, height=240, fps=30)
        stream2 = RTSPStream(source2, width=320, height=240, fps=30)
    except ValueError as e:
        print(e)
        return

    print("Starting video capture and stitching. Press 'q' to exit.")

    while True:
        frame1 = stream1.read()
        frame2 = stream2.read()

        if frame1 is None or frame2 is None:
            if frame1 is not None:
                cv2.imshow("RTSP Stream 1", frame1)
            if frame2 is not None:
                cv2.imshow("RTSP Stream 2", frame2)
            continue

        cv2.imshow("RTSP Stream 1", frame1)
        cv2.imshow("RTSP Stream 2", frame2)

        stitched_img = process_frame(frame1, frame2)

        if stitched_img is not None:
            cv2.imshow("Stitched Image", stitched_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stream1.stop()
    stream2.stop()
    cv2.destroyAllWindows()
    print("All resources released. Program terminated gracefully.")

if __name__ == "__main__":
    main()
