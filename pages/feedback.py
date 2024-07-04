import cv2 as cv 
import numpy as np 
import streamlit as st
import mediapipe as mp
import time

## initialize pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def detect_pose():
    if st.button("Start", key='start_button'):
        use_webcam = True
    else:
        use_webcam = False

    if use_webcam:
        cap = cv.VideoCapture(0)

        start_time = time.time()
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break

            elapsed_time = time.time() - start_time
            if elapsed_time >= 30:
                break
    
        cap.release()
        cv.destroyAllWindows()

def main():
    st.title("Posture Feedback")
    st.write()
    detect_pose()

if __name__=='__main__':
    main()
