from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from vision import detect_text
 
 
global capture, switch
capture=0
switch=1
 
#instatiate flask app  
app = Flask(__name__, template_folder='./templates')
 
 
camera = cv2.VideoCapture(0)

 
def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read()
        if success:  
            if(capture):
                capture=0
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                detect_text(frame)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass
 
 
@app.route('/')
def index():
    return render_template('index.html')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
@app.route('/requests', methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1                          
                
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')
  
if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()