import cv2

class Camera:
    def __init__(self, cam_index=0, width=1280, height=720):
        # CAP_DSHOW for faster capture on windows
        self.cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)
        return frame
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()