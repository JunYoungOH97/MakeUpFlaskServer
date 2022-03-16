from pickletools import uint8
import dlib


class Detection:
    def __init__(self):
        dlib.DLIB_USE_CUDA=True
        
        self.detector = dlib.cnn_face_detection_model_v1("./model/model_state/mmod_human_face_detector.dat")
        # self.detector = detector = dlib.get_frontal_face_detector()

        self.sp = dlib.shape_predictor("./model/model_state/shape_predictor_5_face_landmarks.dat")
        # self.sp = dlib.shape_predictor("./model_state/shape_predictor_68_face_landmarks_GTX.dat")
    
    def get_image(self, img):
        # img = dlib.load_rgb_image(img)
        img = self.align_faces(img)
        return img

    def align_faces(self, img):
        dets = self.detector(img,1)

        if len(dets) == 0:
            print('cannot find faces!')

        objs = dlib.full_object_detections()

        # for detection in dets:
        #     s = self.sp(img, detection.rect)
        #     objs.append(s)

        # objs.append(self.sp(img, dets[0]))
        objs.append(self.sp(img, dets[0].rect))
        faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)

        return faces