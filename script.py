#It imports libraries
import matplotlib.pyplot as plt
import cv2,time,pandas
from datetime import datetime
#It creates CascadeClassifier object that detect faces
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
"""
Status_list is a list containing 0 and 1 from every frame.
If there was a face in the frame, 1 was added to the list, and if not 0.
"""
status_list=[0,0]
times=[]
"""
Time spent in front of the computer in seconds
"""
FullTime=0
"""
Creates a dataframe that contains information about how many hours I spent before
computer on a given day
"""
try:
    df=pandas.read_csv("Time.csv")
except:
    df=pandas.DataFrame(columns=["Day","Time"])
#It turns on webcam
video=cv2.VideoCapture(0)
while True:
    """
    Initially, the variable status is 0, if the face appears in the frame, its value
    will change to 1
    """
    status=0
    #Records frame
    check, frame = video.read()

    #Creates other variable for grey frame
    img_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #Finds coordinates of a face on a frame, and store it in faces variable
    faces=face_cascade.detectMultiScale(img_gray,
    scaleFactor=1.1,
    minNeighbors=13)

    #Draws a green rectangle around a face
    for x,y,w,h in faces:
        img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    #Shows frame
    cv2.imshow("Color",frame)
    #Chcanges status value
    if faces is not ():
        status=1
    status_list.append(status)
    #Saves how much time the face is visible on the webcam
    if status_list[-1]==1 and status_list[-2]==0:
        start=time.time()

    if status_list[-1]==0 and status_list[-2]==1:
        end=time.time()
        times.append(end-start)

    #If q is pressed it closes all windows
    key=cv2.waitKey(1)
    if key==ord("q"):
        if status==1:
            end=time.time()
            times.append(end-start)
        break

video.release()
cv2.destroyAllWindows


for i in times:
    FullTime=FullTime+i

#Turns seconds into hours
FullTime=FullTime*(1/3600)
#Saves data in Time.csv and shows a bar chart
Days=df['Day'].values.tolist()
Time=df['Time'].values.tolist()
try:
    if datetime.now().strftime("%y-%m-%d") == Days [-1]:
        Time[-1]=Time[-1]+FullTime
        df=pandas.DataFrame(columns=["Day","Time"])
        n=0
        for i in Days:
            df=df.append({"Day":i,'Time':Time[0]},ignore_index=True)
            n=n+1

        df.to_csv("Time.csv",index=False)
    else:
        df=df.append({"Day":datetime.now().strftime("%y-%m-%d"),
        'Time':FullTime},ignore_index=True)
        df.to_csv("Time.csv",index=False)
except:
    df=df.append({"Day":datetime.now().strftime("%y-%m-%d"),
    'Time':FullTime},ignore_index=True)
    df.to_csv("Time.csv",index=False)
df=pandas.read_csv("Time.csv")
Days=df['Day'].values.tolist()
Time=df['Time'].values.tolist()

plt.bar(Days,Time)
plt.xlabel("Day")
plt.ylabel("Hours")
plt.title("Hours in front of the computer")
plt.show()
