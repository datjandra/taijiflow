import cv2 as cv 
import numpy as np 
import streamlit as st
import mediapipe as mp
import time
import tempfile
import os

## initialize pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def detect_pose():
    video_file = st.file_uploader('Upload Video')
    if video_file is not None:
        tmpfile = tempfile.NamedTemporaryFile(delete=False)
        tmpfile.write(video_file.read())

        cap = cv.VideoCapture(tmpfile.name)
        canvas = st.empty()

        start_time = time.time()
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break
    
            try:
                img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                pose_results = pose.process(img_rgb)
                mp_drawing.draw_landmarks(img_rgh, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                canvas.image(img_rgb)
            except:
                break

            if cv.waitKey(5) & 0xFF == ord('q'):
                break
    
        cap.release()
        tmpfile.close()
        os.remove(tmpfile.name)
        # cv.destroyAllWindows()

def main():
    st.title("Posture Feedback")
    st.write()
    detect_pose()

if __name__=='__main__':
    main()
