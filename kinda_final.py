import face_recognition
import cv2
import numpy as np
import csv#comma seperated files
import time
import os #to acess all the fies in the system
from datetime import datetime
import RPi.GPIO as GPIO
'''
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/home/pi/Downloads/pro-techt-1f798-firebase-adminsdk-i1tf6-9f8eb39a7c.json")
firebase_admin.initialize_app(cred)
db = firebase.client()
collection = db.collection("db")
res = collection.document(1).set({
    'totalInput':0
    })
'''
#PIR_in Sensor Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

#PIR_out Sensor Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)


#Servo Motor Setup
servoPin = 7
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)
pin7 = GPIO.PWM(servoPin, 50)
pin7.start(0)

def angleToDutyConvert(angle):
  dutyCycle = angle / 18 + 2
  GPIO.output(servoPin, GPIO.HIGH)
  pin7.ChangeDutyCycle(dutyCycle)
  time.sleep(0.5)
  GPIO.output(servoPin, GPIO.LOW)
  time.sleep(0.5)
  
def sweep(degrees):
  for pos in range(0, degrees, +120):
    #print(pos)
    angleToDutyConvert(pos)
  for pos in range(degrees, 0, -120):
    #print(pos)
    angleToDutyConvert(pos)

while True:
#for x in range(1):
    i = GPIO.input(15)
    if i == 1:
        print("Welcome")
        
        video_capture = cv2.VideoCapture(0)

        #loading the images + encoding(reading all the data)
        anisha_image =face_recognition.load_image_file("images/anisha.jpg")
        anisha_encoding = face_recognition.face_encodings(anisha_image)[0]

        chakrika_image =face_recognition.load_image_file("images/chakrika.jpg")
        chakrika_encoding = face_recognition.face_encodings(chakrika_image)[0]

        known_faces_encoding = [anisha_encoding,chakrika_encoding]

        known_faces_name = ["anisha", "chakrika", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"]

        Room = known_faces_name.copy()
        face_location = []#stores the loc of face - coordinates
        face_encoding = []#data encoding
        face_names =[]#names storing
        s=True

        now = datetime.now()
        current_data = now.strftime("%d - %m - %y")

        #writing the file
        f = open(current_data + '.csv', 'w+', newline='')
        lnwriter = csv.writer(f)

        '''
        while True:
            i = GPIO.input(11)
            if i == 0:
                print("No Intruder")
                time.sleep(1)
            elif i == 1:
                #name = "Breach"
                print("Intruder Alert!")
                time.sleep(1)
        '''
        while True:
            _,frame = video_capture.read()#video input reading
            small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)#decreasing the size
            rgb_small_frame = small_frame[:,:,::-1]#bgr-->rgb
            if s :
                face_locations = face_recognition.face_locations(rgb_small_frame)#recognises presence o f a face in the frame
                face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)#store the dat of the coming frame
                face_names=[]
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_faces_encoding,face_encoding)
                    name = "Unknown"
                    face_distance = face_recognition.face_distance(known_faces_encoding,face_encoding)
                    best_match_index = np.argmin(face_distance)#?
                    if matches[best_match_index]:
                        name = known_faces_name[best_match_index]
                    
                    face_names.append(name)
                    if name in known_faces_name:
                        if name in Room:
                            Room.remove(name)
                            print(Room)
                            if name != "Unknown":  #runs for those who do not belong to the room
                                sweep(120)
                                sweep(-120)      
                                
                            #elif name == "Unknown":
                                #sweep(-120)
                            #sweep(-120)
                            '''
                            else:
                                i = GPIO.input(11)
                                if i == 1:
                                    name = "Breach"
                                    print("Intruder Alert!")
                                    time.sleep(1)
                            '''
                            
                        current_time = now.strftime("%H - %M - %S")
                        lnwriter.writerow([name,current_time])
                        f.flush()
                        
                        
            cv2.imshow("register",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()
        f.close()
