from tkinter import *
import tkinter as tk
from tkinter import messagebox
import customtkinter
import sys
from pystray import MenuItem as item
import pystray
from PIL import Image
import datetime
from notifypy import Notify
from playsound import playsound
import threading
from datetime import timedelta
from threading import *
import time

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.geometry("400x340+450+200")
root.resizable(False, False)
root.title('Pratical Alarm')
root.iconphoto(True, tk.PhotoImage(file='alarm2.png'))

def add_sec(qtd):
    now = datetime.datetime.strptime(entry.get(), '%H:%M:%S')
    entry.delete(0, tk.END)
    entry.insert(0,add_time(now,0,0,qtd))

def add_min(qtd):
    now = datetime.datetime.strptime(entry.get(), '%H:%M:%S')
    entry.delete(0, tk.END)
    entry.insert(0,add_time(now,0,qtd,0))

def add_hour(qtd):
    now = datetime.datetime.strptime(entry.get(), '%H:%M:%S')
    entry.delete(0, tk.END)
    entry.insert(0,add_time(now,qtd,0,0))

def next_hour():
    now = datetime.datetime.now()
    now = now.replace(minute=0, second=0, microsecond=0)
    entry.delete(0, tk.END)
    entry.insert(0,add_time(now,1,0,0))

def set_now():
    now = datetime.datetime.now()
    entry.delete(0, tk.END)
    entry.insert(0,add_time(now,0,0,0))

def add_time(time,qtd_h,qtd_m,qtd_s):
  new_time = time + timedelta(hours=qtd_h)
  new_time = new_time + timedelta(minutes=qtd_m)
  new_time = new_time + timedelta(seconds=qtd_s)
  return new_time.strftime("%H:%M:%S")

items = []
alarms = []
alarms_names = []
stop_threads = False
all_threads = []

def clean_alarms():
  global items
  global alarms
  global stop_threads
  items.clear()
  for alarm in alarms:
    alarm.destroy()
  alarms.clear()
  stop_threads = True
  set_now()
  bt_set_alarm.configure(state=tk.NORMAL)
  threading.Thread(target=playsound, args=('mixkit-fast-sweep-transition-174.wav',), daemon=True).start()

def set_alarm():
  global stop_threads
  global alarms
  stop_threads = False
  text = entry.get()
  for alarm in alarms:
    if alarm.text[:8] == text:
      return
  if len(alarms) == 4:
    return
  if len(alarms) == 3:
    bt_set_alarm.configure(state=tk.DISABLED)
  threading.Thread(target=playsound, args=('mixkit-gaming-lock-2848.wav',), daemon=True).start()
  global items
  items.append(pystray.MenuItem(text,None))
  set_now()
  add_label(text)
  Threading(text)

def Threading(text_time):
    t1=Thread(target=new_alarm, args=(text_time,))
    t1.daemon = True
    t1.start()
    all_threads.append(t1)

def new_alarm(text_time):
    now = datetime.datetime.now()
    hour = datetime.datetime.strptime(text_time, '%H:%M:%S').hour
    minute = datetime.datetime.strptime(text_time, '%H:%M:%S').minute
    second = datetime.datetime.strptime(text_time, '%H:%M:%S').second
    time_alarm = now.replace(hour=hour,minute=minute,second=second)
    if now>time_alarm:
      time_alarm = time_alarm.replace(day=now.day+1)
    while True:
        if stop_threads:
          break
        time.sleep(1)
        current_time = datetime.datetime.now()
        if current_time>time_alarm:
            threading.Thread(target=playsound, args=('loud_alarm_clock.mp3',), daemon=True).start()
            global alarms
            description = ''
            for alarm in alarms:
              if alarm.text[:8] == text_time:
                alarm.config(fg="gray")
                description = alarm.text[12:]
            messagebox.showwarning("alarm", description)
            break

def labelText(e):
  return e.text[:9]

def add_label(text_time):
  dialog = customtkinter.CTkInputDialog(master=None, text="Enter a name:", title="New Alarm")
  dialog_input = dialog.get_input()
  if dialog_input is None:
    dialog_input = ''
  description = text_time+'    '+dialog_input[:25]
  label = customtkinter.CTkLabel(root,bg_color=None,text_color="black",text_font=("Helvetica 12 bold"),width=10,anchor='w',text=description)
  label.pack(side=tk.LEFT, fill=tk.BOTH)
  pos = 0.4+(len(alarms)/10)
  label.place(relx=0.11,rely=pos)
  alarms.append(label)
  for alarm in alarms:
    alarms.sort(key=labelText)
  i = 0
  for alarm in alarms:
    pos = 0.4+(i/10)
    alarm.place(relx=0.11,rely=pos)
    i += 1

def quit_window(icon, item):
  global stop_threads
  stop_threads = True
  icon.stop()
  root.destroy()
  sys.exit()

def hide_window():
  global items
  if len(items) == 0:
    sys.exit()
  else:
    root.withdraw()
    items.append(pystray.MenuItem('Quit', quit_window))
    image=Image.open('alarm5.ico')
    icon=pystray.Icon("name", image, "title", items)
    icon.run()

root.protocol('WM_DELETE_WINDOW', hide_window)

frame = customtkinter.CTkFrame(master=root, width=400, height=310, fg_color=root['bg'],
border_color="#323232", border_width=1)
frame.pack(padx=5, pady=20)
frame.place(rely=0.05)

button = customtkinter.CTkButton(master=root, text="+15 s", hover_color="#9f0000", fg_color="red4", text_color="white", 
  corner_radius=12, width = 20, command=lambda:add_sec(15))
button.place(relx=0.1, rely=0.15, anchor=tk.CENTER)

button = customtkinter.CTkButton(master=root, text="+5 m", hover_color="#9f0000", fg_color="red4", text_color="white", 
  corner_radius=12, width = 20, command=lambda:add_min(5))
button.place(relx=0.26, rely=0.15, anchor=tk.CENTER)

button = customtkinter.CTkButton(master=root, text="+30 m", hover_color="#9f0000", fg_color="red4", text_color="white", 
  corner_radius=12, width = 20, command=lambda:add_min(30))
button.place(relx=0.42, rely=0.15, anchor=tk.CENTER)

button = customtkinter.CTkButton(master=root, text="+1 h", hover_color="#9f0000", fg_color="red4", text_color="white", 
  corner_radius=12, width = 20, command=lambda:add_hour(1))
button.place(relx=0.58, rely=0.15, anchor=tk.CENTER)

button = customtkinter.CTkButton(master=root, text="+4 h", hover_color="#9f0000", fg_color="red4", text_color="white", 
  corner_radius=12, width = 20, command=lambda:add_hour(4))
button.place(relx=0.73, rely=0.15, anchor=tk.CENTER)

button = customtkinter.CTkButton(master=root, text="next h", hover_color="#9f0000", fg_color="red4", text_color="white", 
  corner_radius=12, width = 20, command=lambda:next_hour())
button.place(relx=0.89, rely=0.15, anchor=tk.CENTER)

now = datetime.datetime.now()
entry = customtkinter.CTkEntry(master=root,
                               placeholder_text=f"{now.hour}:{now.minute}:{now.second}",
                               width=120,
                               height=25,
                               border_width=2,
                               corner_radius=10,
                               justify=tk.CENTER)
entry.place(relx=0.5, rely=0.28, anchor=tk.CENTER)
entry.delete(0, tk.END)
entry.insert(0, f"{str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}:{str(now.second).zfill(2)}")

button = customtkinter.CTkButton(master=root, text="now", hover_color="#9f0000", fg_color="red4", text_color="white", 
  corner_radius=12, width = 20, command=lambda:set_now())
button.place(relx=0.73, rely=0.28, anchor=tk.CENTER)

frame = customtkinter.CTkFrame(master=root, width=320, height=136, fg_color=root['bg'],
border_color="#121212", border_width=2)
frame.pack(padx=5, pady=20)
frame.place(relx=0.1, rely=0.393)

bt_set_alarm = customtkinter.CTkButton(master=root, text="Set Alarm", command=lambda:set_alarm())
bt_set_alarm.place(relx=0.3, rely=0.9, anchor=tk.CENTER)
button = customtkinter.CTkButton(master=root, text="Clean Alarms", command=lambda:clean_alarms(),hover_color="#551111", fg_color="#771111")
button.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

tk.mainloop()