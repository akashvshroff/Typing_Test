from tkinter import *
from tkinter import ttk
import time, math, sqlite3, random
from fuzzywuzzy import fuzz
from typing_strings import type_strings

def start_test():
    star['state'] = DISABLED
    stop['state'] = NORMAL
    reset['state'] = NORMAL
    global start, tstring
    test.delete('1.0', END)
    tstring = choose_string()
    ltx.set(tstring)
    check_input()

def check_input():
    global start
    if  test.get('1.0',"end-1c") == '':
        root.after(100,check_input)
    else:
        start = time.time()

def stop_test():
    global start,name
    star['state'] = NORMAL
    end = time.time()
    inp = test.get('1.0',"end-1c")
    try:
        t = abs(start - end)
        num_words = len(inp.split())
        test.delete('1.0', END)
        if num_words > 0:
            speed = '{:.2f}'.format((num_words/t) * 60)
            acc = str(fuzz.ratio(tstring,inp))
            sum = speed + acc
            res = 'Typing speed: {} wpm \nAccuracy: {}%'.format(speed,acc)
            cur.execute('Insert into Scores(name,wpm,accuracy,sum) VALUES (?,?,?,?)',(name,speed,acc,sum))
        else:
            res = 'You have not typed anything!'
        ltx.set(res)
    except NameError: #stopped without typing anything
        ltx.set("You have not typed anything!")
    conn.commit()

def choose_string():
    ts = ''
    s = random.choice(fs)
    for c,w in enumerate(s.split()):
        if c%6 == 0:
            ts += '\n'
        ts = ts + ' ' + w
    fs.remove(s)
    return ts

def reset_test():
    test.delete('1.0', END)
    check_input()

def score_disp():
    sc_dis.configure(state = 'normal')
    sc_dis.delete('1.0', END)
    cur.execute('SELECT name, wpm, accuracy from Scores ORDER BY sum DESC')
    rows = cur.fetchall()
    sc = ''
    for c, row in enumerate(rows):
        if c == 5:
            break
        sc += '{}. {}: Speed = {}, Accuracy = {}.'.format(c+1,*row)
        sc += '\n'
    sc_dis.insert(INSERT,sc)
    sc_dis.configure(state = 'disabled')

def quit_prg():
    sys.exit()

def sub_name():
    gs["state"] = NORMAL
    global name, fs
    name = n.get()
    n.set('Welcome {}! Click on start typing!'.format(name))
    ne["state"] = DISABLED
    fs = type_strings[:]
    ltx.set("Welcome to the test!\nClick start to show your first prompt and\nclick submit to reveal your score!")
    test.delete('1.0', END)
    test.insert(INSERT, "The timer will start when you start typing!")
    subname["state"] = DISABLED

def new_user():
    global name
    ne["state"] = NORMAL
    n.set('')
    subname["state"] = NORMAL

def change_tab(t):
    tabs.tab(1, state = 'normal')
    tabs.tab(2, state = 'normal')
    tabs.select(t)

root = Tk()
root.geometry("416x475")
root.configure(bg = '#9fbfdf')

tabs = ttk.Notebook(root)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tab3 = ttk.Frame(tabs)

tabs.add(tab1, text = "Get Started")
tabs.add(tab2, text = "Typing Test")
tabs.add(tab3, text = "Leaderboard")

tabs.pack(expand = 1, fill = 'both')

#TAB1 - Getting Started
welc = Label(tab1, text = "TYPING TEST", width = 41, bg = '#26558B', fg = '#f8f8ff' , font = ('System',20,'bold'), justify = LEFT)
welc.pack(side = 'top')
rtitle = Label(tab1, text = "Rules:", width = 41, bg = '#26558B', fg = '#f8f8ff' , font = ('System',20,'bold'), justify = LEFT)
rtitle.pack(side = 'top')
rules =  '1. The test measures your typing speed and accuracy by giving you 15-20 word prompts!\n2. You can either type the full prompt or a part of it but if you do not finish it, your accuracy will be low!\
          \n3. Once you finish, hit submit and try again or view the the leaderboard! Only the 5 best get on there.\n4. While typing, hit reset to try again on the same prompt. Once you finish, hit submit.\n5. Return to this page anytime to change the user and click the Leaderboard tab to view scores!\n6. Enter your name below and start typing!\n'
rls = Message(tab1, text = rules, bg = '#26558B', fg = '#f8f8ff' ,  font = ('System',12))
rls.pack()

n = StringVar()
n.set("Click on new user!")
ne = Entry(tab1, textvariable = n, width = 41, bg = '#f8f8ff', fg = '#26558B', font = ('System',12,'bold'), justify = LEFT, state = DISABLED)
ne.pack()


btnF = Frame(tab1, width = 40, bd = 0, bg = '#9fbfdf')
btnF.pack()
newuse = Button(btnF, text = 'New User', width = 18, bg = '#9fbfdf', fg = '#A42D41',font = ('System',12,'bold'), command = new_user)
newuse.pack(side = 'left')
subname = Button(btnF, text = "Submit User", width = 18, bg = '#9fbfdf', fg = '#A42D41', font = ('System',12,'bold'), command = sub_name, state = DISABLED)
subname.pack(side = 'left')


gs = Button(tab1, text = 'Start Typing',width = 37, bg = '#9fbfdf', fg = '#A42D41',font = ('System',12,'bold'), command = lambda: change_tab(1))
gs.pack()
gs["state"] = DISABLED

#TAB2 - TYPING TEST
ltx = StringVar()
ltx.set("Welcome to the test!\nClick start to show your first prompt and\nclick submit to reveal your score!")
lab = Label(tab2, textvariable = ltx, height = 8, bg = '#26558B', fg = '#f8f8ff', width = 48, font = ('System',13,'bold'), justify = LEFT, padx = 0, pady = 1)
lab.pack()

test = Text(tab2, height = 8, width = 48, bg = '#f8f8ff', fg = '#26558B', font = ('System',12,'bold'))
test.pack()
test.insert(INSERT, "The timer will start when you start typing!")

opf = Frame(tab2, width = 40, bd = 0, bg = '#9fbfdf')
opf.pack()

star = Button(opf, text = "Start", command = start_test, bg = '#9fbfdf', fg = '#A42D41',  font = ('System',16,'bold'), width = 13, height = 2)
star.pack(side = 'left')

stop = Button(opf, text = 'Stop', command = stop_test,  bg = '#9fbfdf', fg = '#A42D41', font = ('System',16,'bold'), width = 13, height = 2, state = DISABLED)
stop.pack(side = 'left')

reset = Button(opf, text = 'Reset', command = reset_test, bg = '#9fbfdf', fg = '#A42D41',  font = ('System',16,'bold'), width = 13, height = 2, state = DISABLED)
reset.pack(side = 'left')

fs = type_strings[:]

opf2 = Frame(tab2, width = 40, bd = 0, bg = '#9fbfdf')
opf2.pack()

menu = Button(opf2, text = 'Main Menu', command = lambda: change_tab(0), bg = '#9fbfdf', fg = '#A42D41',  font = ('System',16,'bold'), width = 20, height = 2)
menu.pack(side = 'left')
ldr = Button(opf2, text = 'Leaderboard', command = lambda: change_tab(2), bg = '#9fbfdf', fg = '#A42D41',  font = ('System',16,'bold'), width = 20, height = 2)
ldr.pack(side = 'left')

#TAB3 - LEADERBOARD SQL
conn = sqlite3.connect(r'C:\Users\akush\Desktop\Programming\Projects\Typing_Test\p1.sqlite')
cur = conn.cursor()
cur.executescript('''Create table if not exists Scores (name TEXT, wpm REAL,
accuracy REAL, sum REAL)''')
sc_l = Label(tab3, font = ('System',20,'bold'),  bg = '#26558B', fg = '#f8f8ff', text = 'LEADERBOARD: ', width = 40, height = 2)
sc_l.pack()
sc_dis = Text(tab3, font = ('System',16,'bold'),  bg = '#f8f8ff', fg = '#26558B', width = 40, height = 6, state = 'disabled')
sc_dis.pack()
f1 = Frame(tab3, width = 40, bd = 0, bg = '#9fbfdf')
f1.pack()
show_lbd = Button(f1, text = 'Update Leaderboard',  bg = '#9fbfdf', fg = '#A42D41', font = ('System',18,'bold'), width = 40, height = 3, command = score_disp)
show_lbd.pack()
f2 = Frame(tab3, width = 40, bd = 0, bg = '#9fbfdf')
f2.pack()
m1 = Button(f2, text = 'Main Menu', command = lambda: change_tab(0),  bg = '#9fbfdf', fg = '#A42D41', font = ('System',16,'bold'), width = 20, height = 3)
m1.pack(side = 'left')
t1 = Button(f2, text = 'Typing Test', command = lambda: change_tab(1),  bg = '#9fbfdf', fg = '#A42D41' ,font = ('System',16,'bold'), width = 20, height = 3)
t1.pack(side = 'left')
f3 = Frame(tab3, width = 40, bd = 0, bg = '#9fbfdf')
f3.pack()
q = Button(f3, text = 'Quit Program', command = quit_prg,  bg = '#9fbfdf', fg = '#A42D41' ,font = ('System',16,'bold'), width = 40, height = 2)
q.pack()

tabs.tab(1, state = 'disabled')
tabs.tab(2, state = 'disabled')

root.mainloop()
