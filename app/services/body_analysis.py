import mediapipe as mp
import cv2
import numpy as np
from io import BytesIO
from PIL import Image

mp_pose = mp.solutions.pose

def analyze_body_from_image(image_file):
    """MediaPipe를 사용한 신체 랜드마크 추출"""
    
    # 이미지 로드
    image = Image.open(image_file)
    image_np = np.array(image)
    
    # BGR로 변환 (OpenCV 형식)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    # MediaPipe Pose 초기화
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
        
        if not results.pose_landmarks:
            return None
        
        # 주요 랜드마크 추출
        landmarks = results.pose_landmarks.landmark
        
        # 어깨 너비 계산 (픽셀 기준, 실제 cm로 변환 필요)
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_width = abs(left_shoulder.x - right_shoulder.x) * image_np.shape[1]
        
        # 허리 위치
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        waist_width = abs(left_hip.x - right_hip.x) * image_np.shape[1]
        
        measurements = {
            "shoulder_width_px": shoulder_width,
            "waist_width_px": waist_width,
            "body_height_px": image_np.shape[0],
            "landmarks": [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in landmarks]
        }
        
