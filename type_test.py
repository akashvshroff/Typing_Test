from tkinter import *
from tkinter import ttk
import time, sqlite3, sys, random
from fuzzywuzzy import fuzz
from typing_strings import type_strings


class TypeTest:

    def __init__(self,master):
        self.master = master
        self.conn = sqlite3.connect(r'C:\Users\akush\Desktop\Programming\Projects\Typing_Test\type_t.sqlite')
        self.cur = self.conn.cursor()
        self.cur.executescript('''Create table if not exists Scores (name TEXT, wpm REAL,
        accuracy REAL, sum REAL)''')
        self.master.geometry("416x475")
        self.master.configure(bg = '#9fbfdf')

        self.tabs = ttk.Notebook(self.master) #creating Notebook structure and tabs

        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.tabs.add(self.tab1, text = "Get Started")
        self.tabs.add(self.tab2, text = "Typing Test")
        self.tabs.add(self.tab3, text = "Leaderboard")

        self.tabs.pack(expand = 1, fill = 'both') #show the tabs

        #Setting up tab 1 - The getting started tab

        self.welc = Label(self.tab1, text = "TYPING TEST", width = 41, font = ('System',20,'bold'), bg = '#26558B', fg = '#f8f8ff' , justify = LEFT)
        self.welc.pack(side = 'top')
        self.rtitle = Label(self.tab1, text = "Rules:", width = 41, bg = '#26558B', fg = '#f8f8ff', font = ('System',20,'bold'), justify = LEFT)
        self.rtitle.pack(side = 'top')
        self.rules =  '1. The test measures your typing speed and accuracy by giving you 15-20 word prompts!\n2. You can either type the full prompt or a part of it but if you do not finish it, your accuracy will be low!\
                  \n3. Once you finish, hit submit and try again or view the the leaderboard! Only the 5 best get on there.\n4. While typing, hit reset to try again on the same prompt. Once you finish, hit submit.\n5. Return to this page anytime to change the user and click the Leaderboard tab to view scores!\n6. Enter your name below and start typing!\n'
        self.rls = Message(self.tab1, text = self.rules,  bg = '#26558B', fg = '#f8f8ff', font = ('System',12))
        self.rls.pack()

        self.n = StringVar()
        self.n.set("Click on new user!")
        self.ne = Entry(self.tab1, textvariable = self.n, bg = '#f8f8ff', fg = '#26558B',  width = 41, font = ('System',12,'bold'), justify = LEFT, state = DISABLED)
        self.ne.pack()

        self.btnF = Frame(self.tab1, width = 40, bd = 0)
        self.btnF.pack()
        self.newuse = Button(self.btnF, text = 'New User', width = 18, font = ('System',12,'bold'),  bg = '#9fbfdf', fg = '#A42D41', command = self.new_user)
        self.newuse.pack(side = 'left')
        self.subname = Button(self.btnF, text = "Submit User", width = 18, font = ('System',12,'bold'), bg = '#9fbfdf', fg = '#A42D41', command = self.sub_name, state = DISABLED)
        self.subname.pack(side = 'left')

        self.gs = Button(self.tab1, text = 'Start Typing',width = 37, font = ('System',12,'bold'),  bg = '#9fbfdf', fg = '#A42D41', command = lambda: self.change_tab(1))
        self.gs.pack()
        self.gs["state"] = DISABLED

        #Setting up TAB2 - Typing test

        self.ltx = StringVar()
        self.ltx.set("Welcome to the test!\nClick start to show your first prompt and\nclick submit to reveal your score!")
        self.lab = Label(self.tab2, textvariable = self.ltx,  bg = '#26558B', fg = '#f8f8ff', height = 8, width = 48, font = ('System',13,'bold'), justify = LEFT, padx = 0, pady = 1)
        self.lab.pack()

        self.test = Text(self.tab2, height = 8, width = 48, bg = '#f8f8ff', fg = '#26558B', font = ('System',12,'bold'))
        self.test.pack()
        self.test.insert(INSERT, "The timer will start when you start typing.\nHit enter or stop to submit.\nDon't worry about newlines when typing!")

        self.opf = Frame(self.tab2, width = 40, bd = 0)
        self.opf.pack()

        self.star = Button(self.opf, text = "Start", command = self.start_test,  font = ('System',16,'bold'), bg = '#9fbfdf', fg = '#A42D41', width = 13, height = 2)
        self.star.pack(side = 'left')

        self.stop = Button(self.opf, text = 'Stop', command = self.stop_test,   font = ('System',16,'bold'), bg = '#9fbfdf', fg = '#A42D41', width = 13, height = 2, state = DISABLED)
        self.stop.pack(side = 'left')

        self.reset = Button(self.opf, text = 'Reset', command = self.reset_test,   font = ('System',16,'bold'),  bg = '#9fbfdf', fg = '#A42D41', width = 13, height = 2, state = DISABLED)
        self.reset.pack(side = 'left')

        self.fs = type_strings[:]

        self.opf2 = Frame(self.tab2, width = 40, bd = 0)
        self.opf2.pack()

        self.master.bind('<Return>',self.stop_test)

        self.menu = Button(self.opf2, text = 'Main Menu', command = lambda: self.change_tab(0), bg = '#9fbfdf', fg = '#A42D41',  font = ('System',16,'bold'), width = 20, height = 2)
        self.menu.pack(side = 'left')
        self.ldr = Button(self.opf2, text = 'Leaderboard', command = lambda: self.change_tab(2), bg = '#9fbfdf', fg = '#A42D41', font = ('System',16,'bold'), width = 20, height = 2)
        self.ldr.pack(side = 'left')

        #Setting up TAB3 - Leaderboard type
        self.sc_l = Label(self.tab3, font = ('System',20,'bold'), text = 'LEADERBOARD: ', width = 40, height = 2, bg = '#26558B', fg = '#f8f8ff')
        self.sc_l.pack()
        self.sc_dis = Text(self.tab3, font = ('System',16,'bold'), width = 40, height = 6, state = 'disabled', bg = '#f8f8ff', fg = '#26558B')
        self.sc_dis.pack()

        self.f1 = Frame(self.tab3, width = 40, bd = 0)
        self.f1.pack()
        self.show_lbd = Button(self.f1, text = 'Update Leaderboard', font = ('System',18,'bold'), width = 40, height = 3, bg = '#9fbfdf', fg = '#A42D41', command = self.score_disp)
        self.show_lbd.pack()

        self.f2 = Frame(self.tab3, width = 40, bd = 0)
        self.f2.pack()
        self.m1 = Button(self.f2, text = 'Main Menu', command = lambda: self.change_tab(0),  bg = '#9fbfdf', fg = '#A42D41', font = ('System',16,'bold'), width = 20, height = 3)
        self.m1.pack(side = 'left')
        self.t1 = Button(self.f2, text = 'Typing Test', command = lambda: self.change_tab(1),   font = ('System',16,'bold'), width = 20, height = 3, bg = '#9fbfdf', fg = '#A42D41')
        self.t1.pack(side = 'left')

        self.f3 = Frame(self.tab3, width = 40, bd = 0)
        self.f3.pack()
        self.q = Button(self.f3, text = 'Quit Program', command = self.quit_prg, bg = '#9fbfdf', fg = '#A42D41',  font = ('System',16,'bold'), width = 40, height = 2)
        self.q.pack()

        self.tabs.tab(1, state = 'disabled')
        self.tabs.tab(2, state = 'disabled')

    def start_test(self):
        #initialises the testing tab
        self.star['state'] = DISABLED
        self.stop['state'] = NORMAL
        self.reset['state'] = NORMAL
        self.test.delete('1.0', END)
        self.tstring = self.choose_string()
        self.ltx.set(self.tstring)
        self.check_input()


    def check_input(self):
        #checks if the user has started typing
        if self.test.get('1.0',"end-1c") == '':
            self.master.after(100,self.check_input)
        else:
            self.start = time.time()

    def stop_test(self, event = None):
        #stop button
        self.star['state'] = NORMAL
        self.stop['state'] = DISABLED
        self.reset['state'] = DISABLED
        self.end = time.time()
        self.inp = self.test.get('1.0',"end-1c")
        try:
            self.t = abs(self.start - self.end)
            self.num_words = len(self.inp.split())
            self.test.delete('1.0', END)
            if self.num_words > 0:
                self.speed = '{:.2f}'.format((self.num_words/self.t) * 60)
                self.acc = str(fuzz.ratio(self.tstring,self.inp))
                self.sum = self.speed + self.acc
                self.res = 'Typing speed: {} wpm \nAccuracy: {}%'.format(self.speed,self.acc)
                self.cur.execute('Insert into Scores(name,wpm,accuracy,sum) VALUES (?,?,?,?)',(self.name,self.speed,self.acc,self.sum))
                self.test.insert(INSERT, "Click Start to try and improve your score!")
            else:
                self.res = 'You have not typed anything!'
            self.ltx.set(self.res)
        except NameError: #stopped without typing anything
            self.ltx.set("You have not typed anything!")
        except AttributeError:
            self.ltx.set("You have not typed anything!")
        self.conn.commit()


    def choose_string(self):
        #picks the string for the test
        self.ts = ''
        s = random.choice(self.fs)
        for c,w in enumerate(s.split()):
            if c%6 == 0:
                self.ts += '\n'
            self.ts = self.ts + ' ' + w
        self.fs.remove(s)
        return self.ts

    def reset_test(self):
        #reset the time and whatever has been typed
        self.test.delete('1.0', END)
        self.check_input()

    def score_disp(self):
        #display leaderboard values
        self.sc_dis.configure(state = 'normal')
        self.sc_dis.delete('1.0', END)
        self.cur.execute('SELECT name, wpm, accuracy from Scores ORDER BY sum DESC')
        self.rows = self.cur.fetchall()
        sc = ''
        for c, row in enumerate(self.rows):
            if c == 5:
                break
            sc += '{}. {}: Speed = {}, Accuracy = {}.'.format(c+1,*row)
            sc += '\n'
        self.sc_dis.insert(INSERT,sc)
        self.sc_dis.configure(state = 'disabled')


    def quit_prg(self):
        #quit prg
        sys.exit()

    def sub_name(self):
        #reset the typing test strings for diff user and then shuffle?
        self.gs["state"] = NORMAL
        self.name = self.n.get()
        self.n.set('Welcome {}! Click on start typing!'.format(self.name))
        self.ne["state"] = DISABLED
        self.fs = type_strings[:]
        self.ltx.set("Welcome to the test!\nClick start to show your first prompt and\nclick submit to reveal your score!")
        self.test.delete('1.0', END)
        self.test.insert(INSERT, "The timer will start when you start typing.\nHit enter or stop to submit.\nDon't worry about newlines when typing!")
        self.subname["state"] = DISABLED

    def new_user(self):
        #change the user name
        self.ne["state"] = NORMAL
        self.n.set('')
        self.subname["state"] = NORMAL

    def change_tab(self,t):
        #change the tab
        self.tabs.tab(1, state = 'normal')
        self.tabs.tab(2, state = 'normal')
        self.tabs.select(t)

def main():
    root = Tk()
    t_test = TypeTest(root)
    root.mainloop()

if __name__ == '__main__':
    main()
