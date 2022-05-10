import os
from tkinter import *
from tkinter import messagebox as mb
os.system("color")


class App(Frame):
    def __init__(self,win):
        self.win=win
        self.win.title("Input dimensions")
        super().__init__(self.win)
        self.grid(padx=10, pady=10)
        self.saveVariable = IntVar()
        self.saveVariable.set(0)
        self.config(bg="black")
        self.win.config(bg="black")

        self.ui1()

    def ui1(self):
        self.width=IntVar()
        self.height=IntVar()
        self.x = Label(self, text="Level width: ", bg="black", fg="white", font=("consolas", 12, "normal"))
        self.x.grid(row=1,column=1)
        self.y = Label(self, text="Level height: ", bg="black", fg="white", font=("consolas", 12, "normal"))
        self.y.grid(row=2,column=1)
        self.inpx=Entry(self, textvariable=self.width,  bg="black", fg="white", font=("consolas", 12, "normal"))
        self.inpx.grid(row=1,column=2)
        self.inpy=Entry(self, textvariable=self.height,  bg="black", fg="white", font=("consolas", 12, "normal"))
        self.inpy.grid(row=2,column=2)
        self.conButton=Button(self, text="Confirm",command=self.confirm, bg="black", fg="white", font=("consolas", 12, "normal"))
        self.conButton.grid(row=3,column=1,columnspan=2,pady=10)
        self.temp=[self.x,self.y,self.inpx,self.inpy,self.conButton]

    def ui2(self):
        self.win.title("Creating level")        
        self.buttonList=[]
        self.textVarList=[]
     
        self.choices=[(' ',"white",''),('#',"white",''),('o', "#00ff00","\033[1;32;40m"),('o', "#ff00ff", "\033[1;35;40m"),('•', "#00ff00","\033[1;32;40m"),('•', "#ff00ff", "\033[1;35;40m"),('÷', "#00ff00","\033[1;32;40m"),('÷', "#ff00ff", "\033[1;35;40m"),('~',"red","\033[1;31;40m")]
        self.tC= StringVar()
        self.tC.set("{ } black {}")
        self.c=[]
        self.positions={'o':[-1,-1],'•':[-1,-1],'÷':[-1,-1]}
        for t in self.choices:
            self.c.append(Radiobutton(self, text=t[0], variable=self.tC, value=t, bg="black", fg=t[1], selectcolor="black", font=("consolas", 12, "normal")))
            self.c[self.choices.index(t)].grid(row=self.choices.index(t)+2,column=1)

        l1=Label(self, text="Select object:",bg="black", fg="white", font=("consolas", 12, "normal"))
        l1.grid(row=1,column=1,columnspan=2)
        
        self.field=[[]]
        for i in range(self.width.get()+2): self.field[0].append('#')
        for i in range(self.height.get()):
            row=['#']
            for j in range(self.width.get()): row.append(' ')
            row.append('#')
            self.field.append(row)
        self.field.append(self.field[0])


        for k in range(self.width.get()+2):
            b=Button(self, text='#', bg="black", fg="white", font=("consolas", 12, "normal"), state=DISABLED, width=1, height=1)
            b.grid(row=2, column=k+3)
            
        for x in range(self.height.get()):
            b=Button(self, text='#', bg="black", fg="white", font=("consolas", 12, "normal"), state=DISABLED, width=1, height=1)
            b.grid(row=x+3, column=3)
            for y in range(self.width.get()):
                t=StringVar()
                self.textVarList.append(t)
                butt=Button(self, textvariable=t, width=1, height=1, bg="black", font=("consolas", 12, "normal"), command=lambda p = len(self.buttonList): self.toggle(p))
                self.buttonList.append(butt)
                butt.grid(row=x+3, column=y+4)
            b=Button(self, text='#', bg="black", fg="white", font=("consolas", 12, "normal"), state=DISABLED, width=1, height=1)
            b.grid(row=x+3, column=self.width.get()+4)
            
        for k in range(self.width.get()+2):
            b=Button(self, text='#', bg="black", fg="white", font=("consolas", 12, "normal"), state=DISABLED, width=1, height=1)
            b.grid(row=self.height.get()+3, column=k+3)

        l2=Label(self,bg="black")
        l2.grid(row=self.height.get()+4,column=2)
        self.saveButton=Button(self, text="Save", bg="black", fg="white", font=("consolas", 12, "normal"), state=DISABLED, command=self.save)
        self.saveButton.grid(row=self.height.get()+5,column=int((self.width.get()+6)/2),columnspan=3)
                
        for i in self.temp: i.destroy()


    def confirm(self):
        try:
            if self.width.get()*self.height.get()>=4: self.ui2()
            else: mb.showerror("Dimensions too small", "The inputed dimensions are too small. Please try again.")
        except TclError:
            mb.showerror("Invalid input", "Please input only integers as dimensions.")

    def toggle(self, p):
        toggleTo=self.tC.get().replace("{ }",'').split(' ')
        if toggleTo[0]=='': toggleTo[0]=' '
        self.textVarList[p].set(toggleTo[0])
        self.buttonList[p].config(fg=toggleTo[1])
        
        currentCell=self.field[p//self.width.get()+1][p%self.width.get()+1]
        if 'm' in currentCell and currentCell[currentCell.find('m')+1] in self.positions: self.positions[currentCell[currentCell.find('m')+1]]["35" in currentCell]=-1
        if toggleTo[0] in self.positions:
            formerPos=self.positions[toggleTo[0]]["35" in toggleTo[2]]
            if formerPos!=-1:
                self.field[formerPos//self.width.get()+1][formerPos%self.width.get()+1]=' '
                self.textVarList[formerPos].set(' ')
            self.positions[toggleTo[0]]["35" in toggleTo[2]]=p
        self.field[p//self.width.get()+1][p%self.width.get()+1]=toggleTo[2]*int((len(toggleTo[2])-abs(len(toggleTo[2])-3)-1)/2)+toggleTo[0]+"\033[0;37;40m"*int((len(toggleTo[2])-abs(len(toggleTo[2])-3)-1)/2)
        if self.positions['o'][0]>-1 and self.positions['o'][1]>-1 and self.positions['÷'][0]>-1 and self.positions['÷'][1]>-1: self.saveButton.config(state=NORMAL, font=("consolas", 12, "bold"))
        else: self.saveButton.config(state=DISABLED, font=("consolas", 12, "normal"))

    def save(self):
        if mb.askyesno("Confirm save", "Are you sure you want to save the level?"): self.saveVariable.set(1)

    def getField(self):
        return self.field


##p=App(Tk())
##p.wait_variable(p.saveVariable)
##f=p.getField()
##p.win.destroy()
##for i in f:
##    for j in i:
##        print(j,end=' ')
##    print()
    
    
#Pitaj:
#resizing Entry
#showerror not defined
