import cv2 
import time
import datetime

current_time = datetime.datetime.now().strftime("%d-%m-%Y")

#getting your webcam to open
capture = cv2.VideoCapture(0)

#This is for the face and body detection built-in by opencv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")


#these variables are for when no one is in frame, after 5 seconds it will stop recording 
detection = False
detection_stopped_time = None
timer_started = False
SECOND_TO_RECORD_AFTER_DETECTION = 5

#This is the frame size of the video recording
frame_size = (int(capture.get(3)), int(capture.get(4)))
#this is the format for the video recording. 
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


while True:
    # this reads frames on your webcam, then displaying it  
    Webcam, frame = capture.read()

    #This converts your frame to a grayscale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #This uses your grayscale image to detect the faces, the "1.3" is the scale factor, it presents the accuracy. The "5"is how many faces you want to detect
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5) #This uses your grayscale image to detect the bodies, the "1.3" is the scale factor, it presents the accuracy. The "5"is how many faces you want to detect
   
   #this is the if statement for the timer, recording and automatic stoppage of recording
    if len(faces) + len(bodies) > 0: 
        if detection:
            #resets timer when you detect a new face
            timer_started = False 
        else: 
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%S") #this sets up the timer 
            #this is for saving the video recording, and the title.
            output = cv2.VideoWriter(
                f"{current_time}.mp4", fourcc, 20.0, frame_size)
            print("Started Recording !")
    elif detection:
        if timer_started:
            #this sets the timer for no detection, if 5 seconds has been passed, the program will stop recording
            if time.time() - detection_stopped_time >= SECOND_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                output.release()
                print("Stopped Recording")

        else: 
            timer_started = True
            detection_stopped_time = time.time()
        

    if detection:
        output.write(frame)

    #This draws the frame on the detected face/body
    for (x, y, width, height) in faces:                       #This is the color and thickness
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)

    cv2.putText(frame, 
                f"{current_time}", (0, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 3,)
    #The window that shows you the video frame
    cv2.imshow("Security Camera" , frame)

    #When you press "x" the program ends
    if cv2.waitKey(1) == ord("x"):
        break

output.release()
capture.release()
cv2.destroyAllWindows()
