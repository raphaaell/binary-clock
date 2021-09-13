import datetime, time, sched, threading
from tkinter import Tk, Label, StringVar, Button, Toplevel
from tkinter.ttk import Combobox

class Fenetre:
    
    def __init__(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.fenetre = Tk()
        
        self.fenetre.title("Horloge")
        
        positionRight = int(self.fenetre.winfo_screenmmwidth()/2 - self.fenetre.winfo_reqwidth()/2)
        positionDown = int(self.fenetre.winfo_screenmmheight()/2 - self.fenetre.winfo_reqheight()/2)
        
        self.fenetre.geometry("+{}+{}".format(positionRight, positionDown))
        
        
        self.fenetre.geometry("500x150")
        self.fenetre.resizable(False, False)
        
        self.text = StringVar()
        
        self.label = Label(self.fenetre, textvariable=self.text, font=("Arial", 20, "bold"))
        self.label.place(relx = 0.5, rely = 0.5, anchor = 'center')
        
        self.but = Button(self.fenetre, text="⚙️", fg="black", borderwidth=0, highlightthickness=0, width=5, height=3, font=("Arial", 10))
        self.but.place(relx = 0.1, rely = 0, anchor = 'ne')
        self.but.configure(command=lambda:self.command())
        
        self.choix = "bin"
        
    def command(self):
        
        self.popup = Toplevel()
        self.popup.title("Configuration")
        self.popup.geometry("200x100")
        
        self.comboBox = Combobox(self.popup, values=["Binary", "Hexadecimal", "Decimal", "BCD"], state="readonly")
        self.comboBox.current(0)
        self.comboBox.place(relx=0.5, rely=0.2, anchor="center")
        self.butConfirm = Button(self.popup, text="Confirm", fg="black", borderwidth=0, highlightthickness=0, width=5, height=3, font=("Arial", 10))
        self.butConfirm.place(relx=0.9, rely=0.95, anchor="se")
        self.butConfirm.configure(command=lambda:self.confirm())
        self.butCancel = Button(self.popup, text="Cancel", fg="black", borderwidth=0, highlightthickness=0, width=5, height=3, font=("Arial", 10))
        self.butCancel.place(relx=0.25, rely=0.95, anchor="se")
        self.butCancel.configure(command=self.popup.destroy)
        
    def confirm(self):
        choix = self.comboBox.current()
        if choix == 0:
            self.choix = "bin"
        elif choix == 1:
            self.choix = "hex"
        elif choix == 2:
            self.choix = "dec"
        elif choix == 3:
            self.choix = "bcd"
        
        self.popup.destroy()
    def start(self):
        t1 = threading.Thread(target=self.schedd)
        t1.start()
        self.fenetre.mainloop()
        
    def schedd(self):
        self.s.enter(0, 1, self.a, (self.s,))
        self.s.run()
        
    
    def a(self, sc):
        second = datetime.datetime.now().time().second
        minute = datetime.datetime.now().time().minute
        hour = datetime.datetime.now().time().hour
        
        if self.choix == "bin":
            hour = bin(hour).replace('0','',1).replace('b','')
            minute = bin(minute).replace('0','',1).replace('b','')
            second = bin(second).replace('0','',1).replace('b','')
            
            
            while len(hour) != 6:
                hour = "0" + hour
            while len(minute) != 6:
                minute = "0" + minute
            while len(second) != 6:
                second = "0" + second
        
        elif self.choix == "hex":
            hour = hex(hour).replace('0','',1).replace('x','')
            minute = hex(minute).replace('0','',1).replace('x','')
            second = hex(second).replace('0','',1).replace('x','')
            
        elif self.choix == "bcd":
            digitsH=[]
            digitsM=[]
            digitsS=[]
            nH = self.count_digits(hour, digitsH)
            nM = self.count_digits(minute, digitsM)
            nS = self.count_digits(second, digitsS)
            digitsH.reverse()
            digitsM.reverse()
            digitsS.reverse()
            bcdH=[]
            bcdM=[]
            bcdS=[]
            for i in range(4*nH):
                bcdH.append(0)
            for i in range(4*nM):
                bcdM.append(0)
            for i in range(4*nS):
                bcdS.append(0)
            self.dec_to_bcd(digitsH,bcdH,nH)
            self.dec_to_bcd(digitsM,bcdM,nM)
            self.dec_to_bcd(digitsS,bcdS,nS)
            
            hour = ""
            minute = ""
            second = ""
            
            for i in range(4*nH):
                hour += str(bcdH[i])
                if i%4 == 3:
                    hour += " "
            for i in range(4*nM):
                minute += str(bcdM[i])
                if i%4 == 3:
                    minute += " "
            for i in range(4*nS):
                second += str(bcdS[i])
                if i%4 == 3:
                    second += " "
                    
                    
            while len(hour) != 10:
                if len(hour) == 5:
                    hour = " " + hour
                else:
                    hour = "0" + hour
            while len(minute) != 10:
                if len(minute) == 5:
                    minute = " " + minute
                else:
                    minute = "0" + minute
            while len(second) != 10:
                if len(second) == 5:
                    second = " " + second
                else:
                    second = "0" + second
            
            
            
        elif self.choix == "dec":
            hour = str(hour)
            minute = str(minute)
            second = str(second)
        
        txt = hour + " : " + minute + " : " + second
        self.text.set(txt)
        
        self.s.enter(1, 1, self.a, (sc,))
        
        
    def count_digits(self, number,digits):
        i=0
        while(number!=0):
            temp= number%10       
            digits.append(temp)
            i=i+1
            number=number//10
        return i

    def dec_to_bcd(self, digits,bcd,n):
        for i in range(n):
            bcd[(4*i)]=((digits[i] >> 3) & 1)
            bcd[(4*i)+1]=((digits[i] >> 2) & 1)
            bcd[(4*i)+2]=((digits[i] >> 1) & 1)
            bcd[(4*i)+3]=(digits[i] & 1)
        return bcd 

main = Fenetre()
main.start()