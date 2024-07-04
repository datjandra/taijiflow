import cv2 as cv 
import numpy as np 
import streamlit as st
import mediapipe as mp

## initialize pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def detect_pose():
    pass

def main():
    st.title("Posture Feedback")
    st.write()
    detect_pose()

if __name__=='__main__':
    main()
