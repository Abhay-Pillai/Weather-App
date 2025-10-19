from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import mysql.connector
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderInsufficientPrivileges
import time
time.sleep(1)
geolocator = Nominatim(user_agent="user_email")



 # Window
class Weather:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1500x900+0+0")
        self.root.title("Weather App Management System")

        # Title Window
        title = Label(self.root, text="WEATHER MANAGEMENT SYSTEM", font=('times new roman', 40, 'bold'), fg='black', bg='skyblue')
        title.place(x=0, y=0, width=1500, height=100)

        # Add logo
        img_logo = Image.open('App.jpg')
        img_logo = img_logo.resize((100, 100))
        self.photo_logo = ImageTk.PhotoImage(img_logo)

        self.logo = Label(self.root, image=self.photo_logo)
        self.logo.place(x=150, y=5, width=100, height=100)

        # To add Background image
        self.add_image(self.root, 'background.jpg', (0, 100), (1500, 600))
        
        #Search Box
        self.add_image(self.root, 'search.jpg', (0, 100), (600, 100))
        self.add_image(self.root, 'climate.png', (0,220), (200,200))
        self.add_image(self.root, 'rectangle.png', (5,450), (1350, 160))

        self.textfield = tk.Entry(self.root, font=("Times New Roman", 40, "bold"), width=15, bg="white", border=0, fg="black")
        self.textfield.place(x=45,y=120)
        self.textfield.focus()
        
        Button_Search = Button(self.root, text = "Search", font=("Times New Roman",20,'bold'),width=15,bg='black',fg='red', command=self.getWeather)
        Button_Search.place(x=600,y=120)

        #time
        name = Label(root,  text = "Current Time:", font=("arial",15, "bold"))
        name.place(x=300,y=250)
        name2 = Label(root,  text = "Current Date:", font=("arial",15, "bold"))
        name2.place(x=500,y=250)
        self.clock=Label(root, font=("Helvetica", 20))
        self.clock.place(x=300,y=300)
        self.date_label=Label(root, font=("Helvetica", 20))
        self.date_label.place(x=500,y=300)

        #Labels
        label1 = Label(self.root, text="Humidity(%)", font=("Helvetica",20, "bold"), fg="red", bg="white")
        label1.place(x=10, y=470)
        label2 = Label(self.root, text="Air Pressure(Mbar)", font=("Helvetica",20, "bold"), fg="red", bg="white")
        label2.place(x=350, y=470)
        label3 = Label(self.root, text="Dew Point(°C)", font=("Helvetica",20, "bold"), fg="red", bg="white")
        label3.place(x=750, y=470)
        label4 = Label(self.root, text="Wind Speed(MPH)", font=("Helvetica",20,  "bold"), fg="red", bg="white")
        label4.place(x=1100, y=470)

        t1 = Label(self.root, text = "Current Temperature", font=("arial",15,"bold"))
        t1.place(x=700,y=250)
        c1 = Label(self.root, text = "Current Condition", font=("arial",15,"bold"))
        c1.place(x=1000, y=250)
        self.t=Label(font=("Helvetica",20,),fg="#ee666d")
        self.t.place(x=700,y=300)
        self.c=Label(font=("Helvetica",20,))
        self.c.place(x=1000,y=300)

        self.entry1 = Label(text="-----", font=("Helvetica",20,  "bold"), bg="white")
        self.entry1.place(x=10, y=540)
        self.entry2 = Label(text="-----", font=("Helvetica",20,  "bold"), bg="white")
        self.entry2.place(x=350, y=540)
        self.entry3 = Label(text="-----", font=("Helvetica",20,  "bold"), bg="white")
        self.entry3.place(x=760, y=540)
        self.entry4 = Label(text="-----", font=("Helvetica",20,  "bold"), bg="white")
        self.entry4.place(x=1160, y=540)

        
        # Create a button to open a new window
        Bt = Button(self.root, text="Past Weather Report", font=('Times New Roman', 15, 'bold'), width=25, height= 2, bg='black',fg='white', command=self.open_win)
        Bt.place(x=550, y=630)

        
    def getWeather(self):
        try:
            city = self.textfield.get()
            # Set a more descriptive user-agent
            geolocator = Nominatim(user_agent="user_Name")
            location = geolocator.geocode(city)
            if location:
                obj = TimezoneFinder()
                result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

                home = pytz.timezone(result)
                local_time = datetime.now(home)
                current_time = local_time.strftime("%I: %M %p")
                self.clock.config(text=current_time)
                local_date = local_time.date()  
                self.date_label.config(text=str(local_date)) 

                # Weather API
                api = "https://api.openweathermap.org" + city + "&appid=key_id"
                json_data = requests.get(api).json()
                condition = json_data['weather'][0]['main']
                temp = int(json_data['main']['temp'] - 273.15)
                humidity = json_data['main']['humidity']
                pressure = json_data['main']['pressure']
                wind = json_data['wind']['speed']
                dew = (temp - (100 - humidity) / 5)

                self.t.config(text=(temp, "°C"))
                self.c.config(text=(condition))

                self.entry1.config(text=humidity)
                self.entry2.config(text=pressure)
                self.entry3.config(text=dew)
                self.entry4.config(text=wind)

            else:
                messagebox.showerror("Error", "Location not found!")

        except GeocoderTimedOut as e:
            messagebox.showerror("Geocoding service timed out", "Please try again later.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid City")

    def open_win(self):
            self.open_win = Toplevel(self.root)
            self.open_win.geometry("1500x900+0+0")
            self.open_win.title("Weather App Management System")


            self.var_W_ID=StringVar()
            self.var_State=StringVar()
            self.var_City=StringVar()
            self.var_Date=StringVar()
            self.var_Temp=StringVar()
            self.var_Hum=StringVar()
            self.var_AirP=StringVar()
            self.var_Dew=StringVar()
            self.var_Wind=StringVar()
       

#Title Window
            title=Label(self.open_win,text="WEATHER MANAGEMENT SYSTEM",font=('times new roman',40,'bold'),fg='black',bg='skyblue')
            title.place(x=0,y=0,width=1500,height=100)
        
#Add logo
            image_logo = Image.open('App.jpg')
            image_logo = image_logo.resize((100,100))
            self.photo_logo1 = ImageTk.PhotoImage(image_logo)

            self.logo1 = Label(self.open_win,image=self.photo_logo1)
            self.logo1.place(x=150,y=5,width=100,height=100)

#images Frame 
            img_frame = Frame(self.open_win,bd=2,relief=RIDGE,bg='white')
            img_frame.place(x=0,y=100,width=1500,height=200)
        
# Add images
            self.add_image(img_frame, 'image1.png', (0, 0), (500, 190))
            self.add_image(img_frame, 'image2.jpg', (500, 0), (500, 190))
            self.add_image(img_frame, 'image3.png', (1000, 0), (380, 190))

#Main Frame
            Main_frame=Frame(self.open_win,bd=2,relief=RIDGE,bg='white')
            Main_frame.place(x=0,y=300,width=1500,height=650)

#Past Weather Report Entry
            Past_weather=LabelFrame(Main_frame, bd=2, relief=RIDGE, text='Past Weather Report Entry',font=('Arial',25,),fg='red',bg='blue')
            Past_weather.place(x=0,y=0,width=1500,height=310)

#Entry fields
        #Weather_id
            W_ID= Label(Past_weather,text='Weather ID',font=('Calibri',15,'bold'),fg='orange red',bg='white')
            W_ID.grid(row=0,column=0,padx=2,sticky=W)

            select_W_ID=ttk.Combobox(Past_weather, textvariable=self.var_W_ID, font=('Calibri',14),width=17,state='readonly')
            select_W_ID['value'] = ('Select Weather ID','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
            select_W_ID.current(0)
            select_W_ID.grid(row=0,column=1,padx=2,pady=10,sticky=W)

            #State
            State = Label(Past_weather,text='State',font=('Calibri',15,'bold'),fg='orange red',bg='white')
            State.grid(row=1,column=0,padx=2,sticky=W)

            select_state=ttk.Combobox(Past_weather, textvariable=self.var_State, font=('Calibri',14),width=17,state='readonly')
            select_state['value'] = ('Select State',  'Maharashtra')
            select_state.current(0)
            select_state.grid(row=1,column=1,padx=2,pady=10,sticky=W)

            #city of India
            City = Label(Past_weather,text='City',font=('Calibri',15,'bold'),fg='orange red',bg='white')
            City.grid(row=2,column=0,padx=2,sticky=W)

            select_city=ttk.Combobox(Past_weather, textvariable=self.var_City, font=('Calibri',14),width=17,state='readonly')
            select_city['value'] = ('Select City', 'Mumbai', 'Pune', 'Delhi', 'Bangalore', 'Ahmedabad', 'Chennai', 'Kolkata','Surat', 'Jaipur', 'Hyderabad' )
            select_city.current(0)
            select_city.grid(row=2,column=1,padx=2,pady=10,sticky=W)

            #Date
            date = Label(Past_weather,font=('Calibri',15,'bold'),text='Date(dd/mm/yyyy)', bg='white')
            date.grid(row=0,column=2, padx=2,pady=5,sticky=W)

            date_name = ttk.Entry(Past_weather, textvariable=self.var_Date, width=20,font=("Calibri",12))
            date_name.grid(row=0,column=3,padx=2,pady=10,sticky=W)

            #Temperature
            Temp = Label(Past_weather,font=("Calibri",15,"bold"),text="Temperature(°C):",bg="white")
            Temp.grid(row=1,column=2,sticky=W,padx=3,pady=2)

            Temp_name = ttk.Entry(Past_weather, textvariable=self.var_Temp, width=20,font=("Calibri",12))
            Temp_name.grid(row=1,column=3,padx=3,pady=2)

        #Humidity
            Hum = Label(Past_weather,font=("Calibri",15,"bold"),text="Humidity(%):",bg="white")
            Hum.grid(row=2,column=2,sticky=W,padx=3,pady=2)

            Hum_name = ttk.Entry(Past_weather, textvariable=self.var_Hum, width=20,font=("Calibri",12))
            Hum_name.grid(row=2,column=3,padx=3,pady=2)
        
        #Air Pressure
            AirP = Label(Past_weather,font=("Calibri",15,"bold"),text="Air Pressure(Pa):",bg="white")
            AirP.grid(row=0,column=4,sticky=W,padx=3,pady=2)


            AirP_name = ttk.Entry(Past_weather, textvariable=self.var_AirP, width=20,font=("Calibri",12))
            AirP_name.grid(row=0,column=5,padx=3,pady=2)
 
        #Air Quality
            Dew = Label(Past_weather,font=("Calibri",15,"bold"),text="Dew Point(°C):",bg="white")
            Dew.grid(row=1,column=4,sticky=W,padx=3,pady=2)

            Dew_name = ttk.Entry(Past_weather, textvariable=self.var_Dew, width=20,font=("Calibri",12))
            Dew_name.grid(row=1,column=5,padx=3,pady=2)

        #Wind Speed
            Wind = Label(Past_weather,font=("Calibri",15,"bold"),text="Wind Speed(MPH):",bg="white")
            Wind.grid(row=2,column=4,sticky=W,padx=3,pady=2)

            Wind_name = ttk.Entry(Past_weather, textvariable=self.var_Wind, width=20,font=("Calibri",12))
            Wind_name.grid(row=2,column=5,padx=3,pady=2)
        
            #Button Frame
            Button_Frame = Frame(Past_weather,bd=2,relief = RIDGE, bg='white')
            Button_Frame.place(x=1000,y=10,width=340,height=150)

         #Button options    
            Button_Insert = Button(Button_Frame, text = "Insert", command = self.add_data, font=("Garamond",15,'bold'),width=13,bg='black',fg='red')
            Button_Insert.grid(row=0,column=0,padx=1,pady=5)           

            Button_Update = Button(Button_Frame, text = "Update", command = self.update_data, font=("Garamond",15,'bold'),width=13,bg='black',fg='red')
            Button_Update.grid(row=1,column=0,padx=1,pady=5)

            Button_Delete = Button(Button_Frame, text = "Delete", command = self.delete_data, font=("Garamond",15,'bold'),width=13,bg='black',fg='red')
            Button_Delete.grid(row=2,column=0,padx=1,pady=5)
        
            Button_Clear = Button(Button_Frame, text = "Clear", command = self.reset_data, font=("Garamond",15,'bold'),width=13,bg='black',fg='red')
            Button_Clear.grid(row=0,column=1,padx=1,pady=5)

            Button_Search = Button(Button_Frame, text = "Search", command = self.search_data, font=("Garamond",15,'bold'),width=13,bg='black',fg='red')
            Button_Search.grid(row=1,column=1,padx=1,pady=5)

            Button_Display = Button(Button_Frame, text = "Display", command = self.fetch_data, font=("Garamond",15,'bold'),width=13,bg='black',fg='red')
            Button_Display.grid(row=2,column=1,padx=1,pady=5)
     

 # --------------------------------------------------------------------------------------------------------Past Weather Report Information Table--------------------------------------------------------------------------------------------------------
        #Past Weather Information Report
            Past_Information=LabelFrame(Main_frame, bd=2, relief=RIDGE, text='Past Weather Report Information Table',font=('Arial',25),fg='red',bg='lightblue')
            Past_Information.place(x=0,y=210,width=1500,height=350)

            table_frame = Frame(Past_Information, bd=3, relief = RIDGE, bg='lightblue')
            table_frame.place(x=0,y=0, width=1365, height=150)

            scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
            scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

            self.Mumbai_table = ttk.Treeview(table_frame, column = ("W_ID", "state", "city", "date",  "Temp", "Hum" , "AirP", "AirQ",  "Wind"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
       
            scroll_x.pack(side=BOTTOM, fill=X)
            scroll_y.pack(side=RIGHT, fill=Y)
        
            scroll_x.config(command=self.Mumbai_table.xview)
            scroll_y.config(command=self.Mumbai_table.yview)

            self.Mumbai_table.heading('W_ID',text='W_ID')
            self.Mumbai_table.heading('state',text='State')
            self.Mumbai_table.heading('city',text='City')
            self.Mumbai_table.heading('date',text='Date')
            self.Mumbai_table.heading('Temp',text='Temperature')
            self.Mumbai_table.heading('Hum',text='Humdidity')
            self.Mumbai_table.heading('AirP',text='Air Pressure')
            self.Mumbai_table.heading('AirQ',text='Air Quality')
            self.Mumbai_table.heading('Wind',text='Wind Speed')

            self.Mumbai_table['show'] = 'headings'

            self.Mumbai_table.column('W_ID',width=150)
            self.Mumbai_table.column('city',width=150)
            self.Mumbai_table.column('date',width=150)
            self.Mumbai_table.column('Temp',width=150)
            self.Mumbai_table.column('Hum',width=150)
            self.Mumbai_table.column('AirP',width=150)
            self.Mumbai_table.column('AirQ',width=150)
            self.Mumbai_table.column('Wind',width=150)

            self.Mumbai_table.pack(fill=BOTH,expand=1)
            
            self.Mumbai_table.bind("<ButtonRelease>",self.get_cursor)

            style = ttk.Style()
            style.configure("Treeview", background="lightblue", foreground="black", rowheight=25, fieldbackground="lightblue")
            style.configure("Treeview.Heading", font=('Arial', 12), background='lightblue', foreground='black', fieldbackground="lightblue")
            style.map("Treeview", background=[('selected', 'darkblue')])

        
#-----------------------------------------------------------------------------------------------------------------Database Connections---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Insert Button function
    def add_data(self):
        if self.var_City.get()=="" or self.var_Date.get()=="" or self.var_W_ID.get()=="" or self.var_State.get()=="" or self.var_Temp.get()=="" or self.var_Hum.get()=="" or  self.var_AirP.get()=="" or self.var_Dew.get()=="" or self.var_Wind.get()=="":
            messagebox.showerror('Error', 'All fields are required', parent=self.open_win)
        else:
            try:
                conn = mysql.connector.connect(host='localhost', username='root', passwd='your_passsword', database='weather')
                my_cursor = conn.cursor()
                if (self.var_City.get()=='Mumbai'):
                    my_cursor.execute('insert into mumbai values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Pune'):
                    my_cursor.execute('insert into pune values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Delhi'):
                    my_cursor.execute('insert into delhi values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Bangalore'):
                    my_cursor.execute('insert into bangalore values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Hyderbad'):
                    my_cursor.execute('insert into hyderbad values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Jaipur'):
                    my_cursor.execute('insert into jaipur values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Surat'):
                    my_cursor.execute('insert into surat values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Ahmedabad'):
                    my_cursor.execute('insert into ahemdabad values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Chennai'):
                    my_cursor.execute('insert into chennai values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                elif (self.var_City.get()=='Kolkata'):
                    my_cursor.execute('insert into kolkata values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), self.var_Date.get(),
                                                                                                                                                          self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                          self.var_Wind.get() ))

                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Success','City Data Record has been inserted!', parent=self.open_win)
                else:
                    messagebox.showerror('Error', 'City field is required', parent=self.open_win)
            except  Exception as es:
                messagebox.showerror('Error', f'(Due To:{str(es)}', parent=self.open_win)
                


    def get_cursor(self,event=""):
        cursor_row = self.Mumbai_table.focus()
        content = self.Mumbai_table.item(cursor_row)
        data = content['values']

        self.var_W_ID.set(data[0])
        self.var_State.set(data[1])
        self.var_City.set(data[2])
        self.var_Date.set(data[3])
        self.var_Temp.set(data[4])
        self.var_Hum.set(data[5])
        self.var_AirP.set(data[6])
        self.var_Dew.set(data[7])
        self.var_Wind.set(data[8])
        
    #Update button function
    def update_data(self):
        if self.var_City.get()=="" or self.var_Date.get()=="" or self.var_W_ID.get()=="" or self.var_State.get()=="" or self.var_Temp.get()=="" or self.var_Hum.get()=="" or  self.var_AirP.get()=="" or self.var_Dew.get()=="" or self.var_Wind.get()=="":
            messagebox.showerror('Error', 'All fields are required', parent=self.open_win)
        else:
            try:
                update=messagebox.askyesno('Update', 'Are you sure to update this city data record ?', parent=self.open_win)
                if update>0:
                    conn = mysql.connector.connect(host='localhost', username='root', passwd='your_password', database='weather')
                    my_cursor = conn.cursor()
                    if (self.var_City.get()=='Mumbai'):
                        my_cursor.execute('update mumbai set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Pune'):
                        my_cursor.execute('update pune set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Delhi'):
                        my_cursor.execute('update delhi set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Bangalore'):
                        my_cursor.execute('update bangalore set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Ahemdabad'):
                        my_cursor.execute('update ahemdabad set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Chennai'):
                        my_cursor.execute('update chennai set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Kolkata'):
                        my_cursor.execute('update kolkata set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Surat'):
                        my_cursor.execute('update surat set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Jaipur'):
                        my_cursor.execute('update jaipur set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)
                    elif (self.var_City.get()=='Hyderabad'):
                        my_cursor.execute('update hyderabad set W_ID=%s,State=%s,City=%s,Temperature=%s,Humidity=%s,Air_Pressure=%s,Dew_Point=%s,Wind_Speed=%s where Date=%s',(self.var_W_ID.get(), self.var_State.get(), self.var_City.get(), 
                                                                                                                                                                                                                                                                                                  self.var_Temp.get(), self.var_Hum.get(), self.var_AirP.get(), self.var_Dew.get(),
                                                                                                                                                                                                                                                                                                  self.var_Wind.get(), self.var_Date.get() ))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Update', 'City Data Record has been updated!', parent=self.open_win)   
                    else:
                        messagebox.showerror('Error', 'City field is required', parent=self.open_win)
                else:
                    if not update:
                        return
            except  Exception as es:
                messagebox.showerror('Error', f'(Due To:{str(es)}', parent=self.open_win)

    #Delete button function
    def delete_data(self):
        if self.var_City.get()=="" or self.var_Date.get()=="" :
            messagebox.showerror('Error', 'Date and City field is required', parent=self.open_win)
        else:
            try:
                delete=messagebox.askyesno('Delete', 'Are you sure to delete this city data record ?', parent=self.open_win)
                if delete>0:
                    conn = mysql.connector.connect(host='localhost', username='root', passwd='your_password', database='weather')
                    my_cursor = conn.cursor()
                    if (self.var_City.get()=='Mumbai'):
                        sql = 'delete from mumbai where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Pune'):
                        sql = 'delete from pune where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Bangalore'):
                        sql = 'delete from bangalore where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Chennai'):
                        sql = 'delete from chennai where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Delhi'):
                        sql = 'delete from delhi where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Surat'):
                        sql = 'delete from surat where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Kolkata'):
                        sql = 'delete from kolkata where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Jaipur'):
                        sql = 'delete from jaipur where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Ahemdabad'):
                        sql = 'delete from ahemdabad where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    elif (self.var_City.get()=='Hyderabad'):
                        sql = 'delete from hyderabad where date=%s'
                        value=(self.var_Date.get(),)
                        my_cursor.execute(sql,value)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo('Deletion', 'City Data Record has been deleted!', parent=self.open_win)
                    else:
                        messagebox.showerror('Error', 'City field is required', parent=self.open_win)
                else:
                    if not delete:
                        return

            except  Exception as es:
                messagebox.showerror('Error', f'(Due To:{str(es)}', parent=self.open_win)

    #Clear Button function
    def reset_data(self):
        self.var_W_ID.set("Select Weather ID")
        self.var_State.set("Select State")
        self.var_City.set("Select City")
        self.var_Date.set("")
        self.var_Temp.set("")
        self.var_Hum.set("")
        self.var_AirP.set("")
        self.var_Dew.set("")
        self.var_Wind.set("")

    #Search Button function
    def search_data(self):
        if self.var_City.get()=="" or self.var_Date.get()=="" :
            messagebox.showerror('Error', 'Please give the Date and City', parent=self.open_win)
        else:
             try:
                 conn = mysql.connector.connect(host='localhost', username='root', passwd='your_password', database='weather')
                 my_cursor = conn.cursor()
                 if (self.var_City.get()=='Mumbai'):
                     query = "SELECT * FROM mumbai WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                 elif (self.var_City.get()=='Pune'):
                     query = "SELECT * FROM pune WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                elif (self.var_City.get()=='Surat'):
                     query = "SELECT * FROM surat WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                 elif (self.var_City.get()=='Bangalore'):
                     query = "SELECT * FROM bangalore WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                  elif (self.var_City.get()=='Hyderabad'):
                     query = "SELECT * FROM hyderabad WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                   elif (self.var_City.get()=='Delhi'):
                     query = "SELECT * FROM delhi WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                   elif (self.var_City.get()=='Jaipur'):
                     query = "SELECT * FROM jaipur WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                  elif (self.var_City.get()=='Chennai'):
                     query = "SELECT * FROM chennai WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                  elif (self.var_City.get()=='Kolkata'):
                     query = "SELECT * FROM kolkata WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                 elif (self.var_City.get()=='Ahmedabad'):
                     query = "SELECT * FROM ahemdabad WHERE Date LIKE %s"  # Replace 'date_column' with the actual column name
                     pattern = f"%{self.var_Date.get()}%"
                     my_cursor.execute(query, (pattern,))
                     rows = my_cursor.fetchall()
                     if len(rows)!=0:
                          self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                          for i in rows:
                                self.Mumbai_table.insert("",END,values=i)
                     conn.commit()
                     conn.close()
                     messagebox.showinfo('Searching', 'City Data Record has been Searched!', parent=self.open_win)
                 else:
                     messagebox.showerror('Error', 'City field is required', parent=self.open_win)
             except  Exception as es:
                 messagebox.showerror('Error', f'(Due To:{str(es)}', parent=self.open_win)

    #Display Button Function
    def fetch_data(self):
        if self.var_City.get()=="":
            messagebox.showerror('Error', 'All fields are required', parent=self.open_win)
        else:
            conn = mysql.connector.connect(host='localhost', username='root', passwd='your_password', database='weather')
            my_cursor = conn.cursor()
            if (self.var_City.get()=='Mumbai'):
                my_cursor.execute('select * from mumbai')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Pune'):
                my_cursor.execute('select * from pune')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Bangalore'):
                my_cursor.execute('select * from bangalore')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Hyderabad'):
                my_cursor.execute('select * from hyderabad')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Delhi'):
                my_cursor.execute('select * from delhi')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Kolkata'):
                my_cursor.execute('select * from kolkata')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Jaipur'):
                my_cursor.execute('select * from jaipur')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Surat'):
                my_cursor.execute('select * from surat')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Ahemdabad'):
                my_cursor.execute('select * from ahemdabad')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            elif (self.var_City.get()=='Chennai'):
                my_cursor.execute('select * from chennai')
                data = my_cursor.fetchall()
                if len(data)!=0:
                    self.Mumbai_table.delete(*self.Mumbai_table.get_children())
                    for i in data:
                        self.Mumbai_table.insert("",END,values=i)
                        conn.commit()
            else:
                messagebox.showerror('Error', 'City field is required', parent=self.open_win)
            conn.close()
            messagebox.showinfo('Displaying', 'All City Data Record has been Dispalyed!', parent=self.open_win)
            
    

    def add_image(self, frame, image_path, position, size):
        image = Image.open(image_path)
        image = image.resize(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = Label(frame, image=photo)
        label.image = photo                                                                                                                                                     # Keep a reference to avoid garbage collection
        label.place(x=position[0], y=position[1], width=size[0], height=size[1])

        
        
if __name__=="__main__":    
    root =Tk()
    obj=Weather(root)
    root.mainloop()


