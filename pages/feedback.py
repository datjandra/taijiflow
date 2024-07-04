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

            try:
                img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                pose_results = pose.process(img_rgb)
                mp_drawing.draw_landmarks(img, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                cv.imshow('Output', img)
            except:
                break
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= 30:
                break
    
        cap.release()
        # cv.destroyAllWindows()

def main():
    st.title("Posture Feedback")
    st.write()
    detect_pose()

if __name__=='__main__':
    main()
