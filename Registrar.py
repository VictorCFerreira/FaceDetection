from email import message
from tkinter import *
from turtle import left
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox
import os

winPath =os.path.dirname(__file__)
path_output_dir = "assets/"
salvar = None
cap = cv2.VideoCapture(0)

#cap = cv2.VideoCapture("rtsp://admin:Inviolavel1@177.101.141.181:555/cam/realmonitor?channel=3&subtype=0")    
## ^  Protocolo das cameras da entrada, mudar o No depois de channel para mudar de camera


def show_frames():
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   cv2image=cv2.resize(cv2image,(200,200))
   img = Image.fromarray(cv2image)
   imgtk = ImageTk.PhotoImage(image = img)
   LabelVideo.imgtk = imgtk
   LabelVideo.configure(image=imgtk)
   LabelVideo.after(20, show_frames)
   




def Registro():
    _,foto = cap.read()
    print("Nome: " + nome)
    print("Apelido: " + apelido)
    salvar = messagebox.askyesno("", "Deseja salvar esta foto?")
    if salvar == True:
        cv2.imwrite(os.path.join(path_output_dir, nome + '_' + apelido + '.png'), foto)




win=Tk()
win.title("Tela de Registro")
win.geometry("500x350")
win.configure(background="#ebebeb")



LabelVideo=Label(win)
LabelVideo.place(x=250, y=50, width=200, height=200)
Lnome=Label(win, text="Nome", bg="#ebebeb",fg=("#000"),anchor='nw')
Lnome.place(x=10,y=50,width=100,height=30)
Lapelido=Label(win, text="Apelido", bg="#ebebeb",fg=("#000"), anchor='nw')
Lapelido.place(x=10,y=110,width=100,height=30)
vNome=Entry(win)
vNome.place(x=10, y=80, width=200, height=30)
vApelido=Entry(win)
vApelido.place(x=10, y=140, width=200, height=30)
btn = Button(win,text="Registrar", command=Registro)
btn.place(x=300, y=260, width=100,height=30)
show_frames()
nome = vNome.get()
apelido = vApelido.get()




win.mainloop()


