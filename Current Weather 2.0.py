from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut, GeocoderInsufficientPrivileges
time.sleep(1)
geolocator = Nominatim(user_agent="abhaypillai26@gmail.com")


 # Window
root = Tk()
root.geometry("1500x900+0+0")
root.title("Weather App Management System")

    
def  getWeather():
        try:
            city=textfield.get()
            geolocator= Nominatim(user_agent="geoapiExercises")
            location= geolocator.geocode(city)
            obj= TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude,lat=location.latitude)

            home=pytz.timezone(result)
            local_time=datetime.now(home)
            current_time=local_time.strftime("%I: %M %p")
            clock.config(text=current_time)
            local_date = local_time.date()  
            date_label.config(text=str(local_date)) 

        #weather
            api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=68e90928d3f3bca4a545b02c1f4ad784"

            json_data = requests.get(api).json()
            condition = json_data['weather'][0]['main']
            temp = int(json_data['main']['temp']-273.15)
            humidity = json_data['main']['humidity']
            pressure = json_data['main']['pressure']
            wind = json_data['wind']['speed']
            dew = (temp - (100 - humidity) / 5)

            t.config(text=(temp,"°C"))
            c.config(text=(condition))

            entry1.config(text=humidity)
            entry2.config(text=pressure)
            entry3.config(text = dew)
            entry4.config(text=wind)
        
        except GeocoderTimedOut as e:
            messagebox.showerror("Geocoding service timed out. Please try again later.")
    

def add_image(frame, image_path, position, size):
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label = Label(frame, image=photo)
    label.image = photo                                                                                                                                                     # Keep a reference to avoid garbage collection
    label.place(x=position[0], y=position[1], width=size[0], height=size[1])

        
        
# Title Window
title = Label(root, text="WEATHER MANAGEMENT SYSTEM", font=('times new roman', 40, 'bold'), fg='black', bg='skyblue')
title.place(x=0, y=0, width=1500, height=100)

# Add logo
img_logo = Image.open('App.jpg')
img_logo = img_logo.resize((100, 100))
photo_logo = ImageTk.PhotoImage(img_logo)

logo = Label(root, image=photo_logo)
logo.place(x=150, y=5, width=100, height=100)

# To add Background image
add_image(root, 'background.jpg', (0, 100), (1500, 600))
        
#Search Box
add_image(root, 'search.jpg', (0, 100), (600, 100))
add_image(root, 'climate.png', (0,220), (200,200))
add_image(root, 'rectangle.png', (5,450), (1350, 160))

textfield = tk.Entry(root, font=("Times New Roman", 40, "bold"), width=15, bg="white", border=0, fg="black")
textfield.place(x=45,y=120)
textfield.focus()
        
Button_Search = Button(root, text = "Search", font=("Times New Roman",20,'bold'),width=15,bg='black',fg='red', command=getWeather)
Button_Search.place(x=600,y=120)

#time
name = Label(root,  text = "Current Time:", font=("arial",15, "bold"))
name.place(x=300,y=250)
name2 = Label(root,  text = "Current Date:", font=("arial",15, "bold"))
name2.place(x=500,y=250)
clock=Label(root, font=("Helvetica", 20))
clock.place(x=300,y=300)
date_label=Label(root, font=("Helvetica", 20))
date_label.place(x=500,y=300)

#Labels
label1 = Label(root, text="Humidity(%)", font=("Helvetica",20, "bold"), fg="red", bg="white")
label1.place(x=10, y=470)
label2 = Label(root, text="Air Pressure(Mbar)", font=("Helvetica",20, "bold"), fg="red", bg="white")
label2.place(x=350, y=470)
label3 = Label(root, text="Dew Point(°C)", font=("Helvetica",20, "bold"), fg="red", bg="white")
label3.place(x=750, y=470)
label4 = Label(root, text="Wind Speed(MPH)", font=("Helvetica",20,  "bold"), fg="red", bg="white")
label4.place(x=1100, y=470)

t1 = Label(root, text = "Current Temperature", font=("arial",15,"bold"))
t1.place(x=800,y=250)
c1 = Label(root, text = "Current Condition", font=("arial",15,"bold"))
c1.place(x=1100, y=250)
t=Label(font=("Helvetica",20,),fg="#ee666d")
t.place(x=800,y=300)
c=Label(font=("Helvetica",20,))
c.place(x=1100,y=300)

entry1 = Label(text=". . .", font=("Helvetica",20,  "bold"), bg="white")
entry1.place(x=10, y=540)
entry2 = Label(text=". . .", font=("Helvetica",20,  "bold"), bg="white")
entry2.place(x=350, y=540)
entry3 = Label(text=". . .", font=("Helvetica",20,  "bold"), bg="white")
entry3.place(x=760, y=540)
entry4 = Label(text=". . .", font=("Helvetica",20,  "bold"), bg="white")
entry4.place(x=1160, y=540)

        
# Create a button to open a new window
Bt = Button(root, text="Past Weather Report", font=('Times New Roman', 15, 'bold'), width=25, height= 2, bg='black',fg='white')
Bt.place(x=550, y=630)
        

root.mainloop()

