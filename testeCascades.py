from email.mime import image
from pydoc import doc
from random import randint
import cv2
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
import pyttsx3

rosto_frente = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
sorrir_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
olhos_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
rosto_perfil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

#cap = cv2.VideoCapture("rtsp://admin:Inviolavel1@177.101.141.181:555/cam/realmonitor?channel=1&subtype=0")
cap = cv2.VideoCapture(0)

tts = pyttsx3.init()
#CascadeSorteada = randint(1, 3)
CascadeSorteada = (2)
   

def DetecRosto ():

        rosto=rosto_frente.detectMultiScale(frame, 1.3, 5)

        if len(rosto) > 0:
            ("detectou rosto")

            for (x,y,w,h) in rosto:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,150), 2)

def DetecSorriso():

        sorriso=sorrir_cascade.detectMultiScale(frame, 1.7, 18)

        if len(sorriso) > 0:
            ("detectou sorriso")
        
        for (x,y,w,h) in sorriso:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

def DetecOlhos():

        olhos=olhos_cascade.detectMultiScale(frame, 1.3, 5)

        if len(olhos) == 0:
            print('fechou os olhos')
        
        
        for (x,y,w,h) in olhos:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (155,0,0), 2)



while True:
    ret,frame = cap.read()
    ##frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (0, 0), fx=0.8, fy=0.8)

    if CascadeSorteada == 1:
        print(CascadeSorteada)
        DetecRosto()

    elif CascadeSorteada == 2:
        print(CascadeSorteada)
        DetecSorriso()

    elif CascadeSorteada == 3:
        print(CascadeSorteada)
        DetecOlhos()

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1)
    if key >= 2 :
        break

