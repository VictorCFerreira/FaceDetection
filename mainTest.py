from multiprocessing.connection import wait
from turtle import left, right
import cv2
from cv2 import destroyAllWindows
from cv2 import CascadeClassifier
from cv2 import CAP_PROP_FPS
from cv2 import CAP_PROP_BUFFERSIZE
import face_recognition
import face_recognition_models
from face_encode import SimpleFacerec
import pyttsx3
import sendUDP
import time
import ReduzLag
import threading


class FreshestFrame(threading.Thread):
    def __init__(self, capture, name='FreshestFrame'):
        self.capture = capture
        assert self.capture.isOpened()

        # this lets the read() method block until there's a new frame
        self.cond = threading.Condition()

        # this allows us to stop the thread gracefully
        self.running = False

        # keeping the newest frame around
        self.frame = None

        # passing a sequence number allows read() to NOT block
        # if the currently available one is exactly the one you ask for
        self.latestnum = 0

        # this is just for demo purposes        
        self.callback = None
        
        super().__init__(name=name)
        self.start()

    def start(self):
        self.running = True
        super().start()

    def release(self, timeout=None):
        self.running = False
        self.join(timeout=timeout)
        self.capture.release()

    def run(self):
        counter = 0
        while self.running:
            # block for fresh frame
            (rv, img) = self.capture.read()
            assert rv
            counter += 1

            # publish the frame
            with self.cond: # lock the condition for this operation
                self.frame = img if rv else None
                self.latestnum = counter
                self.cond.notify_all()

            if self.callback:
                self.callback(img)

    def read(self, wait=True, seqnumber=None, timeout=None):
        # with no arguments (wait=True), it always blocks for a fresh frame
        # with wait=False it returns the current frame immediately (polling)
        # with a seqnumber, it blocks until that frame is available (or no wait at all)
        # with timeout argument, may return an earlier frame;
        #   may even be (0,None) if nothing received yet

        with self.cond:
            if wait:
                if seqnumber is None:
                    seqnumber = self.latestnum+1
                if seqnumber < 1:
                    seqnumber = 1
                
                rv = self.cond.wait_for(lambda: self.latestnum >= seqnumber, timeout=timeout)
                if not rv:
                    return (self.latestnum, self.frame)

            return (self.latestnum, self.frame)

##rosto_frente = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
sorrir_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
#olhos_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#rosto_perfil_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')

tts = pyttsx3.init()
sfr = SimpleFacerec()
sfr.load_encoding_images("assets/")

#cap = cv2.VideoCapture(0)
capLento = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("rtsp://admin:Inviolavel1@177.101.141.181:555/cam/realmonitor?channel=3&subtype=0")
#capLento = cv2.VideoCapture("rtsp://admin:Inviolavel1@177.101.141.181:555/cam/realmonitor?channel=3&subtype=0")

capLento.set(CAP_PROP_FPS, 10)
#capLento.set(CAP_PROP_BUFFERSIZE, 0)
cap = ReduzLag.FreshestFrame(capLento)  



cont =0
cor = 0
lido = False
while True:
    
    ret,frame = cap.read()
    frame = cv2.resize(frame,(0, 0),fx=1, fy=1)
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("Frame", frame)

    face_locations, face_names = sfr.detect_known_faces(frameRGB)
    for face_loc, name in zip(face_locations, face_names):
        namePessoa = name.partition("_")[2]
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.putText(frame,namePessoa, (x1,y1 -10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 5)
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,150), 2)
        
        cv2.imshow("Frame", frame)

        if name != 'Unknown':
            #sendUDP.MandarUDP()
            print('Detectou conhecido, esperando 5 sec')
            print(namePessoa)
            sorriso=sorrir_cascade.detectMultiScale(frame, 1.5, 18)

            if len(sorriso):
                print('sorriso do ' + namePessoa)

                for (x,y,w,h) in sorriso:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                cv2.imshow('frame', frame)
            #tts.say("Olá " + namePessoa +"! seja bem vindo!")
            #tts.runAndWait()
            #time.sleep(5)
            #print(name)
            #time.sleep(1)
            #print(name + "depois de um segundo")
            #cap.release
            #print("esperar 15 segundos")
            #time.sleep(15)
            #print("passou 15 segundos")
            #cap = cv2.VideoCapture(0)
            
            
            

        elif name == 'Unknown':
            #tts.say('Desconhecido')
            print('desconhecido')
            #print(name)
            #time.sleep(1)
            #print(name + "depois de um segundo")
            #cap.release
            #print("esperar 15 segundos")
            #time.sleep(15)
            #print("passou 15 segundos")
            #cap = cv2.VideoCapture(0)   
    
    key = cv2.waitKey(1)
    if key >= 2 :
        break


cap.release()
cv2.destroyAllWindows

