#-*-coding:utf8;-*-

import curses
from curses.textpad import Textbox, rectangle
import socket
import menu
import sys
from time import ctime
import form
from threading import Thread
import os
from configparser import SafeConfigParser

g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ft = 'localhost'
#port = 2112
nick = "Siz"
nck = "Gelen"
directory = os.path.dirname(os.path.realpath(__file__))
real_directory = directory + '/'
config_dirtoformat = '{}/config.ini'
logdir = "{}/logs/".format(directory)
config_dir = config_dirtoformat.format(directory)
config = SafeConfigParser()
timesplit = ctime().split(" ")
logname = "guichatlog "+timesplit[2] +" "+ timesplit[1] +" "+ timesplit[4] +" "+ timesplit[3]
if not os.path.exists("{}/logs/".format(directory)):
    os.makedirs("{}/logs/".format(directory))


def check():
    global first_run, logging
    if not os.path.isfile(config_dir):
        first_run = 1
        file = open(config_dir, "w")
        config.read(config_dir)
        config.add_section("main")
        logging = "False"
    else:
        first_run = 0

def saveload():
    global ft, port, logging
    if first_run:
        file = open(config_dir, "w")
        config.read(config_dir)
        config.set("main", "ip",ft)
        config.set("main", "port", str(port))
        config.set("main", "logging", logging)
        config.write(file)
    config.read(config_dir)
    ft = config.get("main", "ip")
    port = int(config.get("main", "port"))
    logging = config.get("main", "logging")
 
 
def configscreen():
    global first_run
    list1 = ["IP VE PORT U AYARLA", "CHAT KAYDI"]
    choice1= menu.create(list1)
    if choice1 == 0:
        setip()
        first_run = 1
        saveload()
    else:
        logconfig()
        
def logconfig():
    global logging
    global first_run
    choice = menu.create(["CHATLOG U ETKINLESTIR", "CHATLOG U KAPAT"])
    if choice == 0:
        logging = "True"
        print("Log aktiflestirildi uygulama tekrar baslatiliyor.")
        first_run = 1
        saveload()
        sys.exit()
    else:
        logging = "False"
        print("Log kapatildi uygulama tekrar baslatiliyor.")
        first_run = 1
        saveload()
        sys.exit()


def makelogfile():
    global logfile
    if logging == "True":
        logfile = open(logdir+logname, "w")

def writelog(veri):
    if logging == "True":
        logfile.write(veri)
        logfile.flush()
        os.fsync(logfile.fileno())
def setmode():
    liste = ['Server', 'Client']
    mode = menu.create(liste)
    return mode

def mainmenu():
    return menu.create(["BASLAT", "CONFIG", "CIKIS"])

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
        writelog(ctime().split(" ")[3]+"     "+gelen+"\n")
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
    check()
    if first_run:
        setip()
    saveload()
    makelogfile()
    getchoice = mainmenu()
    if getchoice == 0:
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
    if getchoice == 1:
        configscreen()
    if getchoice == 2:
        sys.exit()
def mainer():
    try:
        main()
    except Exception as e:
        print(e)
        
if __name__ == "__main__":
    main()
   
        
