from email.policy import default
import subprocess
import threading
from tkinter.font import BOLD
from turtle import bgcolor
from typing import Self
from xmlrpc.client import DateTime
from cv2.typing import Prim
import face_recognition
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from tkinter import PhotoImage
import subprocess
from datetime import datetime
import util
import numpy as np
import queue
import csv
import threading 

class App:
    global username_user 
    global password_user
    csv_filename = ""

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1156x650")

        self.bg_image = tk.PhotoImage(file="C:/Users/divij/source/repos/minor project/7468572.png")
        self.bg_label = tk.Label(self.main_window, image=self.bg_image)
        self.bg_label.grid(row=0, column=0, columnspan=2)

        self.webcam_label = util.getimagelabel(self.main_window)
        self.webcam_label.place(x=81.5, y=146, height=370, width=510)
        self.webcam_label.config(bg="black")

        self.user_image_label  = util.getimagelabel(self.main_window )
        self.user_image_label .place(x=763, y=73, height=230, width=320)

        self.login_button_main_button = util.get_button(self.main_window, "ID", "#A73DB7", self.login, fg="black", font_size=12)
        self.login_button_main_button.place(x=773, y=517, width=50, height=35)

        self.register_button_main_window = util.get_button(self.main_window, "REGISTER", "black", self.login_page, fg="#A73DB7", font_size=12)
        self.register_button_main_window.place(x=880, y=516, width=208, height=35)

        self.DB_DIR = './db'
        os.makedirs(self.DB_DIR, exist_ok=True)

        self.login_path = './login.txt'
        
        self.get_text_label_main_window = util.gettextlabel(self.main_window, 'Hey , there 🙋‍', font_size=11, fg="white")
        self.get_text_label_main_window.place(x=225, y=133, width=230)
        self.get_text_label_main_window.config(bg="black")

        self.get_text_label_main_window_2 = util.gettextlabel(self.main_window, 'WELCOME STUDENTS', font_size=14, fg="white")
        self.get_text_label_main_window_2.place(x=763, y=73, height=230, width=320)
        self.get_text_label_main_window_2.config(bg="black")

        self.get_text_label_main_window_3 = util.gettextlabel(self.main_window, "  Detecting...", font_size=14, fg="white")
        self.get_text_label_main_window_3.place(x=763, y=350, height=40, width=320)
        self.get_text_label_main_window_3.config(bg="black")

        self.get_text_label_main_window_id = util.gettextlabel(self.main_window, "  Detecting...", font_size=14, fg="white")
        self.get_text_label_main_window_id.place(x=763, y=410, height=40, width=320)
        self.get_text_label_main_window_id.config(bg="black")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.frame_queue = queue.Queue()
        self.recognition_thread = threading.Thread(target=self.process_faces, daemon=True)
        self.recognition_thread.start()

        self.process_webcam()
        self.main_window.mainloop()

    def process_webcam(self):
        """Continuously captures frames from webcam and updates the GUI."""
        ret, frame = self.cap.read()
        if not ret:
            self.webcam_label.after(10, self.process_webcam)
            return

        self.most_recent_image_arr = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if self.frame_queue.empty():  # Only add new frames if the queue is empty
                self.frame_queue.put(frame.copy())

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.most_recent_image_pil = Image.fromarray(img)
        ImageTk_ = ImageTk.PhotoImage(image=self.most_recent_image_pil)
        self.webcam_label.imagetk = ImageTk_
        self.webcam_label.configure(image=ImageTk_)

        self.webcam_label.after(10, self.process_webcam)

    def process_faces(self):
        """Runs face recognition on the most recent frame in the queue."""
        while True:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()
                unknown_people_img = './.tmp.jpg'
                cv2.imwrite(unknown_people_img, frame)

                try:
                    output = subprocess.check_output(['face_recognition', self.DB_DIR, unknown_people_img])
                    output = output.decode('utf-8').strip().split(',')[1]



                    name2 = output.split("\\")[0]
                    name3 =name2.split(".")[0].strip().upper()
                    self.name = name3.split("-")[0]
                    self.id2 =name3.split("-")[1]
                    print (self.name )
                    print(self.id2)
                    
                    

                    if self.name not in ["UNKNOWN_PERSON", "NO_PERSONS_FOUND"]:
                        if self.is_user_already_marked(self.id2):
                            self.main_window.after(0, self.update_already_registered , self.name, self.id2)
                        else:
                            self.main_window.after(0, self.update_name, self.name, self.id2)
                            self.save_login(self.name, self.id2)
                            self.create_csv_file(self.name, self.id2)

                    
                except Exception as e:
                    print(f"Error in face recognition: {e}")
                    self.get_text_label_main_window_2.config(text="USER NOT DETECTED ")
                    self.get_text_label_main_window_3.config(text="Detecting...")
                    self.get_text_label_main_window_id.config(text="Detecting...." )
                    self.get_text_label_main_window_2.after(5000 , lambda: self.get_text_label_main_window_2.config(text="Welcome students"))

    def is_user_already_marked(self, id2):
        csv_filename = datetime.now().strftime("data_%Y-%m-%d.csv")
        if os.path.exists(csv_filename):
            with open(csv_filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 1 and row[1] == id2:
                        return True
        return False

    def update_already_registered(self ,name ,id2):
        self.get_text_label_main_window_2.config(text=f"User is already registered")
        self.get_text_label_main_window_3.config(text=f"NAME = {name}")
        self.get_text_label_main_window_id.config(text=f"ID = {id2} " )
        self.get_text_label_main_window_2.after(5000 , lambda: self.get_text_label_main_window_2.config(text="Welcome students"))



    def update_name(self, name ,id2):
        """Updates the recognized name on the GUI."""
        self.get_text_label_main_window_3.config(text=f"NAME = {name}")
        self.get_text_label_main_window_id.config(text=f"ID = {id2} " )
        self.get_text_label_main_window_2.config(text =f"ATTENDENCE MARKED 👍")
        self.get_text_label_main_window_2.after(5000 , lambda: self.get_text_label_main_window_2.config(text="Welcome students"))
    


    def create_csv_file(self, name, id2):
        global csv_filename
        csv_filename = datetime.now().strftime("data_%Y-%m-%d.csv")

        self.file_name = csv_filename  
        data = [name, id2, "Present"]

    
        if not os.path.exists(self.file_name):
            with open(self.file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "ID", "ATTEND"])  
            

    
        try:
            with open(self.file_name, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

                 

   
    def save_login(self, name ,id2):
        with open(self.login_path, 'a') as f:
            f.write(f'{name} {id2} {datetime.now()}\n')



    
    def display_user_image(self, name ,id2):
        try:
             img_path = f"C:/Users/divij/source/repos/minor project/minor project/db/{name}-{id2}.jpg"  
             image = Image.open(img_path)
             image = image.resize((180, 240), Image.Resampling.LANCZOS)  
             self.photo = ImageTk.PhotoImage(image)


             img_label = tk.Label(self.main_window ,image=self.photo)
             img_label.image = self.photo  

             img_label.place(x=763, y=73, height=180, width=240) 
        except Exception as e:
            print(f"Error displaying user image: {e}")



    def login(self):
       

        if not hasattr(self, 'name') or not hasattr(self, 'id2'):
            util.messagebox_display('error', 'Try Again, no user found!')

        elif self.name in ["UNKNOWN_PERSON", "NO_PERSONS_FOUND"]:
            util.messagebox_display('error', 'Try Again, no user found!')

        else :
             


             self.new_login_window = tk.Toplevel(self.main_window)
             self.new_login_window.geometry("314x500")
             self.new_login_window.config(bg="black")

             self.bg_image_login = tk.PhotoImage(file="C:/Users/divij/source/repos/minor project/id_card.png")
             self.bg_label_login = tk.Label(self.new_login_window, image=self.bg_image_login)
             self.bg_label_login.grid(row=0, column=0, columnspan=2)

             self.get_text_label_login_window_name = util.gettextlabel(self.new_login_window , f": {self.name} "  ,font_size=22 ,fg="black" )
             self.get_text_label_login_window_name.place(x=105, y=300 , width=120)
             self.get_text_label_login_window_name.config(bg="#E4E4E4")

             self.get_text_label_login_window_id = util.gettextlabel(self.new_login_window , f": {self.id2} "  ,font_size=10 ,fg="black" )
             self.get_text_label_login_window_id.place(x=105, y=395 , width=120)
             self.get_text_label_login_window_id.config(bg="#E4E4E4")

             
             img_path = f"C:/Users/divij/source/repos/minor project/minor project/db/{self.name}-{self.id2}.jpg"  
             image = Image.open(img_path)
             image = image.resize((235, 180), Image.Resampling.LANCZOS)  
             self.photo = ImageTk.PhotoImage(image)


             img_label = tk.Label(self.new_login_window ,image=self.photo)
             img_label.image = self.photo  

             img_label.place(x=42, y=98, width=235, height=180) 


    

    def login_page(self):
        self.login_page_window = tk.Toplevel(self.main_window)
        self.login_page_window.geometry("657x344")
        self.login_page_window.config(bg="black")

        self.bg_image_login_page = tk.PhotoImage(file=r"C:\Users\divij\source\repos\minor project\login_page_minor.png")
        self.bg_label_login_page = tk.Label(self.login_page_window, image=self.bg_image_login_page)
        self.bg_label_login_page.grid(row=0, column=0, columnspan=2)

        self.username_login_page = util.gettextlabel(self.login_page_window  , 'USERNAME :' ,font_size=10 ,fg="black")
        self.username_login_page.place(x=410, y=150 ,height=30 , width=90)
        self.username_login_page.config(bg="white")

        self.password_login_page = util.gettextlabel(self.login_page_window  , 'PASSWORD :' ,font_size=10 ,fg="black")
        self.password_login_page.place(x=410, y=190 ,height=30 , width=90)
        self.password_login_page.config(bg="white")

        self.username_user = util.getentrytext(self.login_page_window)
        self.username_user.place(x=510, y=150 ,height=20 , width=70)

        self.password_user = util.getentrytext(self.login_page_window)
        self.password_user.place(x=510, y=190 ,height=20 , width=70)

        self.login_button_login_page_window = util.get_button(self.login_page_window , "login", "black", self.verify , fg="white" , font_size=10 )
        self.login_button_login_page_window.place(x=460, y=230 , width=80 ,height=30)


    def register_new_user(self):

        self.new_register_window = tk.Toplevel(self.main_window)
        self.new_register_window.geometry("1156x650")
        self.new_register_window.config(bg="black")

        self.bg_image_register = tk.PhotoImage(file="C:/Users/divij/source/repos/minor project/7468572.png")
        self.bg_label_register = tk.Label(self.new_register_window, image=self.bg_image_register)
        self.bg_label_register.grid(row=0, column=0, columnspan=2)

        self.new_register_window_accept = util.get_button(self.new_register_window , "accept", "#07d7fe", self.accept_new_user , fg="black" , font_size=12 )
        self.new_register_window_accept.place(x=763, y=518, width=325 , height=35)

        self.new_register_window_tryagain = util.get_button(self.new_register_window , "Try again", "black", self.try_again_new_user, fg="#07d7fe" ,font_size=12)
        self.new_register_window_tryagain.place(x=763, y=575 , width=325 ,height=35)

        self.capture_label = util.getimagelabel(self.new_register_window )
        self.capture_label.place(x=81.5, y=146, height=370, width=510 )
        self.capture_webcam(self.capture_label)

        self.get_entry_text_register_new_user_name = util.getentrytext(self.new_register_window)
        self.get_entry_text_register_new_user_name.place(x=860, y=330 ,height=30 , width=225)

        self.get_entry_text_register_new_user_id = util.getentrytext(self.new_register_window)
        self.get_entry_text_register_new_user_id.place(x=860, y=390 ,height=30 , width=225)

        self.get_text_label_register_new_user = util.gettextlabel(self.new_register_window  , 'PLEASE , ENTER YOUR NAME AND ID:' ,font_size=13 ,fg="white")
        self.get_text_label_register_new_user.place(x=763, y=73, height=230, width=320)

        self.get_text_label_register_new_user_name = util.gettextlabel(self.new_register_window  , 'NAME :' ,font_size=13 ,fg="white")
        self.get_text_label_register_new_user_name.place(x=763, y=330, height=30, width=75)

        self.get_text_label_register_new_user_id = util.gettextlabel(self.new_register_window  , 'ID:' ,font_size=13 ,fg="white")
        self.get_text_label_register_new_user_id.place(x=763, y=390, height=30, width=75)


    def capture_webcam (self , label):
        Imagetk = ImageTk.PhotoImage(image=self.most_recent_image_pil)
        label.imagetk = Imagetk
        label.configure(image=Imagetk)

        self.capture_image = self.most_recent_image_arr.copy()

    def accept_new_user (self):
        name =  self.get_entry_text_register_new_user_name.get("1.0", "end-1c")
        id2 =  self.get_entry_text_register_new_user_id.get("1.0", "end-1c")

        cv2.imwrite(os.path.join(self.DB_DIR , f'{name}-{id2}.jpg') ,self.capture_image)
        util.messagebox_display('SUCCCESS ',' USER IS REGISTERED SUCCESSFULLY') 
        self.new_register_window.destroy()

    def try_again_new_user(self):
        self.new_register_window.destroy()

    def verify (self):
        username = self.username_user.get("1.0", "end-1c").strip()  
        password = self.password_user.get("1.0", "end-1c").strip()

        if username =='' and password =='':
            util.messagebox_display('ERROR','blanks are not allowd')
        elif username =='divij2004' and password =='123456' :
            self.register_new_user()
            self.login_page_window.destroy()
        else :
            util.messagebox_display('ERROR','wrong username or password')





    





if __name__ == "__main__":
    app = App()
    app.main_window.mainloop()