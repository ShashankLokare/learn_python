{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import cv2\
from transformers import BlipProcessor, BlipForConditionalGeneration\
import torch\
\
# Initialize the BLIP model and processor\
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")\
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")\
\
def describe_frame(frame):\
    # Convert the frame to a format suitable for the model\
    inputs = processor(images=frame, return_tensors="pt")\
\
    # Generate description\
    out = model.generate(**inputs)\
    description = processor.decode(out[0], skip_special_tokens=True)\
    return description\
\
def describe_video(video_path):\
    # Open the video file\
    cap = cv2.VideoCapture(video_path)\
    frame_rate = cap.get(cv2.CAP_PROP_FPS)\
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))\
    duration = frame_count / frame_rate\
\
    print(f"Video Frame Rate: \{frame_rate\} FPS")\
    print(f"Video Duration: \{duration:.2f\} seconds")\
\
    frame_descriptions = []\
\
    while cap.isOpened():\
        ret, frame = cap.read()\
        if not ret:\
            break\
\
        # Resize frame for faster processing (optional)\
        frame = cv2.resize(frame, (320, 240))\
\
        # Describe the frame\
        description = describe_frame(frame)\
        frame_descriptions.append(description)\
        print(description)\
\
    cap.release()\
    return frame_descriptions\
\
if __name__ == "__main__":\
    video_path = "path_to_your_video.mp4"  # Replace with your video file path\
    descriptions = describe_video(video_path)\
    for i, desc in enumerate(descriptions):\
        print(f"Frame \{i\}: \{desc\}")\
}