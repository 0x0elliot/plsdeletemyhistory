import optparse
import subprocess
import os
import random
import sqlite3
import sys
import time
from termcolor import colored

__author__="0x0elliot"

bash=False

home=os.environ["HOME"]

parser=optparse.OptionParser()

parser.add_option('-s','--seconds',dest="seconds", help="Time after which you would like to delete your history [Seconds]", type=int)

parser.add_option('-c','--chrome', dest="chrome", help="Specifically clean it for chrome. [Browser is set to be chrome by default.]", action="store_true")

parser.add_option('-d','--days', dest='days', help="Specifically after how many days do you want your history to be wiped.", type=str)

parser.add_option("-f",'--firefox',dest="firefox",help="[NOT IMPLEMENTED YET!] Specifically clean it for firefox", action="store_true")

parser.add_option('-v','--verbose', dest='verbose',help="Verbose", action="store_true")

parser.add_option('-b', '--bash', dest='bash',help="Clear bash history as well.", action="store_true")

parser.add_option('-o','--power-off',dest='poweroff', help='Power-off your computer after doing the cleaning.',action="store_true")

(options,args)=parser.parse_args()

chrome=True
firefox=False
v=False

if("-f" in sys.argv or "--firefox" in sys.argv):
    firefox=True
    print(colored("I am sorry! This option has not been implemented for firefox yet! Apologies. You can contribute to the project at and contribute and add that feature though :)"))
    if "-c" not in sys.argv and "--chrome" not in sys.argv:
        chrome=False

if options.seconds==None and options.days==None:
    print(colored('Either --days or --seconds is necessary!','red'))
    quit()


elif options.seconds!=None and options.days!=None:
    print(colored('You gave both seconds and days. Choose one.','red'))
    quit()

elif options.seconds!=None and options.days==None:
    time_to_sleep=options.seconds

elif options.seconds==None and options.days!=None:
    time_to_sleep=options.days*60*60*24

if "-v" in sys.argv or "--verbose" in sys.argv:
    v=True

if "-b" in sys.argv or "--bash" in sys.argv:
    bash=True #lol my dude needs both his bash history and browser history cleaned.

#print(colored("Be careful! You would need to make sure that your browser has been closed!", 'red'))

turnoff=False

if "-o" in sys.argv or "--power-off" in sys.argv:
    turnoff=True

def delete_history_chrome():
    path=f'{home}/.config/google-chrome/Default/History'
    #print(path) #-> for debug
    #quit() #break point

    con=sqlite3.connect(path)
    c=con.cursor()
    result=True

    try:
        ids=[]
        sys.stdout.flush()
        print()
        if v==True:
            sys.stdout.write('Detecting history to delete..')
        for rows in c.execute("select id,url from urls"):
            sys.stdout.flush()
            if v==True:
                sys.stdout.write(colored('\rDetecting history to delete.','blue'))
                time.sleep(0.2)
                sys.stdout.flush()
            ids.append((rows[0],))
            if v==True:
                sys.stdout.write(colored('\rDetecting history to delete..','magenta'))
                time.sleep(0.2)
        if v==True:
            sys.stdout.flush()
            sys.stdout.write(colored('Detected..Deleting history..','cyan'))
        c.executemany('delete from urls where id=?',ids)
        con.commit()
        print()
        os.system('clear')
        if bash==True:
            os.system('cat /dev/null > ~/.bash_history')
        print('Done! ;)')
        if turnoff==True:
            os.system("poweroff")
    except Exception as e:
        sys.stdout.flush()
        print()
        os.system('clear')
        print(colored("An error happened. Are you sure that you are not running chrome while trying to run this script? if yes, then first close chrome else this error will keep on coming.", 'red'))
        print()
        print(colored("The error:",'cyan'))
        print(e)

os.system('clear')

if chrome==True and firefox==False:
    colors=['red','white','magenta','red','cyan','blue','yellow','green']
    for i in range(time_to_sleep):
        time.sleep(1)
        if i%5==0:
            #os.system('clear')
            sys.stdout.flush()
            sys.stdout.write(colored("\rSleeping",random.choice(colors)))
        sys.stdout.flush()
        random.shuffle(colors)
        sys.stdout.write(colored(".",random.choice(colors)))
    delete_history_chrome()

elif firefox==True:
    print("Sorry! The firefox option hasn't been implemented yet! Feel free to contribute to the project and implementing it on your own :)")
    quit()
