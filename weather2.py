from curses.panel import bottom_panel
from json import load
from locale import getlocale
from logging import getLogger
from re import search
from tkinter import *
import tkinter as tk
from tkinter import font
from geopy.geocoders import Nominatim
from tkinter import messagebox,ttk
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False,False)


def getWeather():
    city = textfield.get()
    
    getlocator = Nominatim(user_agent="geoapiExercises")
    location = getlocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    print(result)


#search box
Search_img = PhotoImage(file="assests/search.png")
myimg = Label(image=Search_img)
myimg.place(x=20,y=20)

textfield = tk.Entry(root, justify="center", width=20,font=("poppins",25,"bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50,y=40)
textfield.focus()

search_icon = PhotoImage(file="assests/search_icon.png")
myimg_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimg_icon.place(x=400,y=34)

#logo
logo_img = PhotoImage(file="assests/logo.png")
logo = Label(image=logo_img)
logo.place(x=150,y=100)

#bottom box
frame_img = logo_img = PhotoImage(file="assests/box.png")
frame_myimg = Label(image=frame_img)
frame_myimg.pack(padx=5,pady=5,side=BOTTOM)

#label
label1 = Label(root, text="WIND", font=("Helvetica",15,"bold"), fg="white", bg="#1ab5ef")
label1.place(x=120,y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica",15,"bold"), fg="white", bg="#1ab5ef")
label2.place(x=225,y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica",15,"bold"), fg="white", bg="#1ab5ef")
label3.place(x=430,y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetica",15,"bold"), fg="white", bg="#1ab5ef")
label4.place(x=650,y=400)

t = Label(font=("arial",70,"bold"), fg="#ee666d")
t.place(x=400,y=150)
c=Label(font=("arial",15,"bold"))
c.place(x=400,y=250)

w = Label(text="...", font=("arial",20,"bold"), bg="#1ab5ef")
w.place(x=120,y=440)
h = Label(text="...", font=("arial",20,"bold"), bg="#1ab5ef")
h.place(x=280,y=440)
d = Label(text="...", font=("arial",20,"bold"), bg="#1ab5ef")
d.place(x=450,y=440)
p = Label(text="...", font=("arial",20,"bold"), bg="#1ab5ef")
p.place(x=670,y=440)

root.mainloop()
