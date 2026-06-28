import cv2

class Camera:
    def __init__(self, cam_index=0, width=1280, height=720):
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(3, width)
        self.cap.set(4, height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)
        return frame
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()