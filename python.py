#!/usr/bin/env python

import tkinter as tk
import datetime
import time
from pythonosc import udp_client
from pythonosc import osc_message_builder
from PIL import ImageTk, Image
from threading import Thread
import vlc

def now():
    return datetime.datetime.now().astimezone()

scriptstart = now()
file="Logs/"+now().date().isoformat()+" "+now().time().isoformat()[0:8].replace(':','-')+".log"

def pw(*text):
    pout = str(now()) + " "
    with open(file,"a") as f:
        f.write(str(now())+" ")
        for t in text:
            t=str(t)
            f.write(t+" ")
            pout += t + " "
            f.write("\n")
    print(pout)

pw("Script Start")

hintgiven = False

def blank():
    blank = tk.Tk()
    width,height=1920,1080 # set the variables 
    d=str(width)+"x"+str(height)
    width,height=1920,1080 # set the variables
    blank.geometry(d)
    blank.configure(bg='#000000')
    blank.title("Blank")
    blank.attributes("-fullscreen", True)
    blank.mainloop()

Thread(target=blank).start()

def send_osc(message, address="192.168.2.10", port=53000):
    client = udp_client.SimpleUDPClient(address, port)
    msg = osc_message_builder.OscMessageBuilder(address = message)
    msg = msg.build()
    client.send(msg)
    return "OSC Message Sent"

def alivetime():
    global scriptstart
    delta = now() - scriptstart
    days = delta.days
    hours = int(delta.seconds / 3600)
    minutes = int(delta.seconds / 60) - (hours * 60)
    seconds = delta.seconds - (hours * 3600) - (minutes * 60)
    days = str(days)
    hours = "0" + str(hours)
    minutes = "0" + str(minutes)
    seconds = "0" + str(seconds)
    out = days+":"+hours[-2:]+":"+minutes[-2:]+":"+seconds[-2:]
    return "Uptime: "+out

def win():
    
    pw("Win")
    inputtxt.config(state="readonly")
    printButton.config(state="disabled")
    background.create_text(960,550, text=" ",fill="white",font=("Flood std", 90,  'bold'), anchor="center")
    #time.sleep(1)
    pw(send_osc('/cue/{27.5}/stop'))
    pw(send_osc('/cue/{28}/go'))
    time.sleep(10)
    background.destroy()
    password.destroy()
    uvbutton.destroy()
    
    time.sleep(2)
    jon = tk.Label(task_window,text=" It Was Me All Along... ",font=("Flood std", 90,  'bold'),fg="green",bg="black")
    jon.place(relx=0.5,rely=0.5,anchor="center")
    time.sleep(5)
    task_window.destroy()
    print("Win End")
    runEnd()

def tryagain():
    global tryagaintxt
    pw("No Win")
    tryagaintxt.grid(column = 0, row = 2)
    inputtxt.config(state="readonly")
    time.sleep(2)
    
    inputtxt.config(state="normal")
    inputtxt.delete(0,'end')
    tryagaintxt.destroy()
    
    tryagaintxt = tk.Label(password, text="Try Again",font=("Montserrat", 20, "italic"), justify="left", anchor="w")

def printInput(*none):
    inp = inputtxt.get()
    pw("Password Inputted:",inp)
    if inp.lower() == "bulls":
        Thread(target=win).start()
    else:
        Thread(target=tryagain).start()

def uv():
    global hintgiven
    pw(hintgiven)
    if hintgiven == False:
        send_osc("/cue/{27}/go")
        hintgiven = True

def runTask():
    global inputtxt
    global printButton
    global background
    global tryagaintxt
    global password
    global task_window
    global uvbutton

    task_window = tk.Tk()
    width,height=1920,1080 # set the variables 
    d=str(width)+"x"+str(height)
    width,height=1920,1080 # set the variables
    task_window.geometry(d)
    task_window.configure(bg='#000000')
    task_window.title("Adam")

    background = tk.Canvas(task_window, width=1920, height=1080)

    bgimage = Image.open("CIA.jpg")
    bgimage = bgimage.resize((1920,1080), Image.LANCZOS)
    bgimage = ImageTk.PhotoImage(bgimage, master = background)

    background.create_image(960,540,anchor="center",image=bgimage)

    #background.create_text(100,885, text="Adam's Super Secret",font=("Montserrat", 50,  'bold'), fill="blue", anchor="w")
    #background.create_text(100,950, text="Login Page",font=("Montserrat", 50,  'bold'), fill="blue", anchor="w")
    #background.create_text(100,800, text="SLLET ",fill="magenta",font=("Flood std", 90,  'bold'), anchor="w")
    background.place(relx=0.5,rely=0.5,anchor="center")

    password = tk.Frame(task_window, padx=5, pady=5)


    usertxt = tk.Label(password, text="Username: ",font=("Montserrat", 20), justify="left", anchor="w")
    usertxt.grid(column = 0, row = 0)

    adamtxt = tk.Entry(password, width = 20, font=("Montserrat", 20))
    adamtxt.insert(0, 'TheDoctor')
    adamtxt.config(state="readonly")
    adamtxt.grid(column = 1, row = 0)

    pwdtxt = tk.Label(password, text="Password: ",font=("Montserrat", 20), justify="left", anchor="w")
    pwdtxt.grid(column = 0, row = 1)

    # TextBox Creation
    inputtxt = tk.Entry(password, width = 20, font=("Montserrat", 20))
    inputtxt.grid(column = 1, row = 1)
    inputtxt.bind('<Return>', printInput)
    inputtxt.focus()
      
    # Button Creation
    printButton = tk.Button(password, text = "Enter", command = printInput, font=("Montserrat", 20,  'bold'))
    printButton.grid(column = 1, row = 2)

    password.place(relx=0.05,rely=0.25,anchor="w")

    tryagaintxt = tk.Label(password, text="Try Again",font=("Montserrat", 20, "italic"), justify="left", anchor="w")

    uvbutton = tk.Button(task_window, text="Clue", font=("Montserrat", 40), command = uv)
    uvbutton.place(relx=0.99,rely=0.95,anchor="e")
        
    #password = tk.Text(task_window, height=1, width=30, font=("Montserrat", 20))
    #password.pack()
    #password.insert(tk.END, "Just a text Widget\nin two lines\n")

    task_window.attributes("-fullscreen", True)
    task_window.mainloop()

def runEnd():
    # create a new instance of the media player
    player = vlc.MediaPlayer()

    # set the media to play
    media = vlc.Media("Scene 3.mp4")
    player.set_media(media)

    # start playing the media
    player.play()

    # make the player go fullscreen
    player.set_fullscreen(True)
        
    while player.get_state() != vlc.State.Ended:
        time.sleep(0.5)
    print("Done")
    player.release()

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def print_handler(address, *args):
    print(f"{address}: {args}")


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")
    if address == "/task":
        Thread(target=runTask).start()
    elif address == "/end":
        Thread(target=runEnd).start()
    
dispatcher = Dispatcher()
dispatcher.map("/something/*", print_handler)
dispatcher.set_default_handler(default_handler)

ip = ""
port = 1337

server = BlockingOSCUDPServer((ip, port), dispatcher)
print("Ready")
#runTask()
#print("Task End")
#runEnd()
server.serve_forever()  # Blocks forever
print("End")
