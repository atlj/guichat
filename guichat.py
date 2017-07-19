#-*-coding:utf8;-*-

import curses
from curses.textpad import Textbox, rectangle
import socket
import menu
import form
from threading import Thread
import os

g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ft = 'localhost'
#port = 2112
nick = "Siz"
nck = "Gelen"

def setmode():
    liste = ['Server', 'Client']
    mode = menu.create(liste)
    return mode

def setip():
    global ft
    global port
    liste = ["IP ADRESI:", "PORT:"]
    getter = form.create("CONFIG", liste)
    ft = getter[0]
    try:
        port = int(getter[1])
    except ValueError:
        setip()
    
def baglan():
    g.connect((ft,port))
    
def bind():
    global c
    global addr
    f = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f.bind((ft, port))
    f.listen(2)
    c, addr = f.accept()
    
def clireceive():
    global person
    global nck
    while 1:
        msg = g.recv(1024).decode("utf-8")
        if "color" in msg:
            bolum = msg.split(" ")
            bolum = bolum[-1]
            if bolum == "green":
                person = green
            if bolum == "red":
                person = red
            if bolum == "white":
                person = white
            if bolum == "cyan":
                person = cyan
        if "nick" in msg:
            bol = msg.split(" ")
            nck = bol[-1] 
        al("recv;"+nck+"> "+msg, person, you)
           
def servreceive():
    global person
    global nck
    while 1:
        msg = c.recv(1024).decode("utf-8")
        if "color" in msg:
            bolum = msg.split(" ")
            bolum = bolum[-1]
            if bolum == "green":
                person = green
            if bolum == "red":
                person = red
            if bolum == "white":
                person = white
            if bolum == "cyan":
                person = cyan
        if "nick" in msg:
            bol = msg.split(" ")
            nck = bol[-1] 

        al("recv;"+nck+"> "+msg, person, you)      
        
def send(msg):
    g.send(bytes(msg, "UTF-8"))
    
def servsend(msg):
    c.send(bytes(msg,"UTF-8"))

def init():
    global person
    global you
    global screen
    global red
    global green
    global cyan
    global white
    global h
    global b
    global gelenlist
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(10,curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(11,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(12,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(13,curses.COLOR_WHITE, curses.COLOR_BLACK)
    red = curses.color_pair(11)
    cyan = curses.color_pair(12)
    white = curses.color_pair(13)
    green = curses.color_pair(10)
    h = curses.A_NORMAL
    b = curses.A_BOLD
    gelenlist = " ; "*10
    gelenlist = gelenlist.split(" ")
    person = curses.color_pair(13)
    you = curses.color_pair(13)
    
def al(gelen,colrec,colsend):
      
    while 1:
        a = 0
        b = 1
        c = 3
        screen.border(0)
        screen.clear()
        screen.refresh()
        gelenlist[10] = gelen
        for oge in gelenlist:
            if b < 11:
                gelenlist[a]=gelenlist[b]
            if a < 10:
                gelenbol = gelenlist[a].split(";")
                kind = gelenbol[0]
                if kind == "recv":
                    screen.addstr(c, 6, gelenbol[1], colrec)
                if kind == "send":
                    screen.addstr(c, 6, gelenbol[1], colsend)
       
            a = a + 1
            b = b + 1
            c = c + 1
        screen.refresh()    
        win.border(0)
        win.refresh()
        break
        
        
def gonder():
    global nick
    global you
    global mesaj
    global win
    win = curses.newwin(4, 24, 15, 9)
    win.border(0)
    win.refresh()
    while 1:
        try:
            mesaj = win.getstr(1,1).decode("utf-8")
        except Exception as e:
            pass
        if "color" in mesaj:
            bolum = mesaj.split(" ")
            bolum = bolum[-1]
            if bolum == "green":
                you = green
            if bolum == "white":
                you = white
            if bolum == "cyan":
                you = cyan
            if bolum == "red":
                you = red
        if "nick" in mesaj:
            bol = mesaj.split(" ")
            nick = bol[-1]
        if mesaj:
            if not mesaj == " ":
                al("send;"+nick+"> "+mesaj, person, you)
        win.clear()
        win.border(0)
        win.refresh()
        servsend(mesaj)

def cligonder():
    global you
    global win
    global mesaj
    global nick
    win = curses.newwin(4, 24, 15, 9)
    win.border(0)
    win.refresh()
    while 1:
        try:
            mesaj = win.getstr(1,1).decode("utf-8")
        except Exception as e:
            pass
        if "color" in mesaj:
            bolum = mesaj.split(" ")
            bolum = bolum[-1]
            if bolum == "green":
                you = green
            if bolum == "white":
                you = white
            if bolum == "cyan":
                you = cyan
            if bolum == "red":
                you = red
        if "nick" in mesaj:
            bol = mesaj.split(" ")
            nick = bol[-1]
        if mesaj:
            if not mesaj == " ":
                al("send;"+nick+"> "+mesaj, person, you)
        win.clear()
        win.border(0)
        win.refresh()
        send(mesaj)

        
def main():
    os.system("clear")
    print("""



                  GUICHAT
              Created By: atli
               github.com/atlj
        Devam Etmek Icin Bir Tusa Basin.
        
        
        """)
    input("")
    init()
    setip()
    if not setmode():
        bind()
        os.system("clear")
        t1 = Thread(target=servreceive, args=())
        t2 = Thread(target=gonder, args=())
        t1.start()
        t2.start()
    else:
        baglan()
        os.system("clear")
        t1= Thread(target=clireceive, args=())
        t2 = Thread(target=cligonder, args=())
        t1.start()
        t2.start()
  
def mainer():
    try:
        main()
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    mainer()
   
        
