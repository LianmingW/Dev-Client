from tkinter import *

def superuser():
    sup=Toplevel(win)
    sup.title("SuperUser Login")
    Label(sup,text="Username:").grid(row=0,column=0)
    Entry(sup,width=20).grid(row=0,column=1)
    Label(sup,text="Password:").grid(row=1,column=0,sticky=W)
    Entry(sup,show="*",width=20).grid(row=1,column=1)
    Button(sup,text="Login!",relief=GROOVE,command=sup.destroy).grid(row=2,column=1)
    
def client():
    cli=Toplevel(win)
    cli.title("Developer Login")
    Label(cli,text="Username:").grid(row=0,column=0)
    Entry(cli,width=20).grid(row=0,column=1)
    Label(cli,text="Password:").grid(row=1,column=0,sticky=W)
    Entry(cli,show="*",width=20).grid(row=1,column=1)
    Button(cli,text="Login!",relief=GROOVE,command=cli.destroy).grid(row=2,column=1)
  
    
def developer():
    dev=Toplevel(win)
    dev.title("Developer Login")
    Label(dev,text="Username:").grid(row=0,column=0)
    Entry(dev,width=20).grid(row=0,column=1)
    Label(dev,text="Password:").grid(row=1,column=0,sticky=W)
    Entry(dev,show="*",width=20).grid(row=1,column=1)
    Button(dev,text="Login!",relief=GROOVE,command=dev.destroy).grid(row=2,column=1)
    
def signup():
    sign=Toplevel(win)
    sign.title("Sign Up")
    Label(sign,text="Not Finsished Yet").grid(row=0,column=1)
    Button(sign,text="SuperUser",width=20,relief=GROOVE).grid(row=1,column=0) 
    Button(sign,text="Client",width=20,relief=GROOVE).grid(row=1,column=1)
    Button(sign,text="Developer",width=20,relief=GROOVE).grid(row=1,column=2)
    
    
    
      
win=Tk()
win.title("Welcome to our system!")
f=Frame(win) 
f.pack()





l = Label(f, text="Login Accordingly Pls")
l.pack(side=TOP)

Button(f, text="SuperUser",width=20,relief=GROOVE,command = superuser).pack(side=LEFT)
Button(f, text="Client",width=20,relief=GROOVE,command = client).pack(side=LEFT)
Button(f, text="Developer",width=20,relief=GROOVE,command = developer).pack(side=LEFT)
Button(win, text="Sign Up!",width=20,relief=GROOVE,command = signup).pack(side=BOTTOM)






scrollbar = Scrollbar(win)
scrollbar.pack(side=RIGHT, fill=Y)
mylist = Listbox(win,bd=10,width=20,yscrollcommand = scrollbar.set )
list1 =['The Top List: ',' ','top1 developer','top2 developer','top3 developer',' ','top1 client','top2 client','top3 client']
for line in range(len(list1)):
    mylist.insert(END,list1[line])

mylist.pack( side = BOTTOM, fill = BOTH )
scrollbar.config( command = mylist.yview )



mainloop()
