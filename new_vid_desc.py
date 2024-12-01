
import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Function to upload video file
def upload_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    return file_path

# Function to analyze video
def analyze_video(file_path):
    cap = cv2.VideoCapture(file_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / frame_rate
    
    frames = []
    success, frame = cap.read()
    while success:
        frames.append(frame)
        success, frame = cap.read()
    
    cap.release()
    
    return frames, duration

# Function to generate description
def generate_description(frames):
    sampled_frames = frames[::len(frames)//10]
    descriptions = []
    
    for frame in sampled_frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        _, thresholded = cv2.threshold(edges, 128, 255, cv2.THRESH_BINARY)
        
        descriptions.append("scene with varying edges and light")

    # Summarize descriptions
    description_words = " ".join(descriptions).split()
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in description_words if word.lower() not in stop_words]
    
    word_freq = Counter(filtered_words)
    most_common_words = word_freq.most_common(40)
    
    description = " ".join([word for word, freq in most_common_words])
    
    return description

# Main function
def main():
    file_path = upload_file()
    if not file_path:
        print("No file selected.")
        return
    
    frames, duration = analyze_video(file_path)
    description = generate_description(frames)
    
    print(f"Video Duration: {duration:.2f} seconds")
    print(f"Description: {description}")

if __name__ == "__main__":
    main()
