import tkinter as tk
from tkinter import messagebox

def get_button(window  ,text, color , command , fg="black" ,  font_size =10):
    button = tk.Button (
        window,
        activebackground ="black",
        text = text,
        fg = fg,
        font=("impact", font_size),
        
        bg = color,
        command = command,
        height = 2,
        width = 20,
        highlightbackground="blue",
        highlightcolor="white",
        
    )
    return button 

def getimagelabel (window):
    lable = tk.Label(window , activebackground="black" , borderwidth=5)
    lable.grid (row=0, column=0)
    return lable

def gettextlabel (window , text ,font_size =10  ,fg="black"):
    lable = tk.Label(window , text =text ,fg=fg ,font=("Arial", font_size),)
    lable.grid (row=0, column=0)
    lable.config(justify="left" , bg="black")
    return lable

def getentrytext (window , ):
    inputtext = tk.Text(window , height=2 , width=25 )
    return inputtext
    

def messagebox_display(title , description):
    messagebox.showinfo(title , description)