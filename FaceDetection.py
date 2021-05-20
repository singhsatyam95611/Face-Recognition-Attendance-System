import os
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import cv2
import face_recognition
import numpy as np
import pandas as pd
from tkvideo import tkvideo

root = Tk()

root.title("Face Detection Attendance System")
root.geometry("700x500")
root.configure(bg="black")
root.iconbitmap('C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\logo.ico')

can = Canvas(root,width=700,height=500,bg="white")
can.pack(expand=YES,fill=BOTH) 
path = PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\back.png')
can.create_image(0,0,anchor=NW,image=path)


def Scan():
# Scanning faces
# Change the path as per your code

    path = "C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\DataSet"
    images = []
    classnames = []
    mylist = os.listdir(path)

    for cl in mylist:
        curimg = cv2.imread(f'{path}/{cl}')
        images.append(curimg)
        classnames.append(os.path.splitext(cl)[0])

    def FindEncodings(images):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist

    encodelistknown = FindEncodings(images)

    cap = cv2.VideoCapture(0)

    while True:
        sucess ,img = cap.read()
        imgs = cv2.resize(img, (0,0), None,0.25,0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        facesincurframe =face_recognition.face_locations(imgs)
        encodecurframe = face_recognition.face_encodings(imgs,facesincurframe)

        for encodeface , faceloc in zip(encodecurframe, facesincurframe):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis =  face_recognition.face_distance(encodelistknown, encodeface)
            matchindex = np.argmin(facedis)

            if matches[matchindex]:
                name = classnames[matchindex].upper()
                y1,x2,y2,x1 = faceloc
                y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4 
                cv2.rectangle(img ,(x1,y1), (x2,y2), (0,255,0),2)
                cv2.rectangle(img ,(x1,y2-35), (x2,y2), (0,255,0),cv2.FILLED)
                cv2.putText(img, name, (x1 + 6,y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
        

            def attendance (name):
                with open("C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\attendance.csv","r+") as f:
                    mydatalist = f.readlines()
                    namelist = []

                    for line in mydatalist:
                        entry = line.split(".")
                        namelist.append(entry[0])                        

                    if name not in namelist:
                        now = datetime.now()
                        date = now.strftime('%d/%m/%y')
                        time = now.strftime('%I:%M %p')
                        f.writelines(f'\n{name}. {date} {time}')
                    f.close()
                        
                        
            attendance(name)
        if cv2.waitKey(10) == ord ("q"):
            cv2.destroyAllWindows()            
            cap.release()
            break
        
        cv2.imshow('Face Detection Attendance System(SCANNER)',img)  


def files1():
# Attendance File
# Change the path as per your code

    path = 'C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\attendance.csv'
    
    new = Toplevel(root)
    new.title("Face Detection Attendance System(RECORDS)")
    new.geometry('700x550')
    new.iconbitmap('C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\logo.ico')

    cols=("Name","Surname","Date","Time","")
    
    lis = ttk.Treeview(new,height=30,column =cols,show="headings")
    lis.column('Name',width=180,anchor=CENTER)
    lis.column('Surname',width=180,anchor=CENTER)
    lis.column('Date',width=120,anchor=CENTER)
    lis.column('Time',width=100,anchor=CENTER)
    lis.column('',width=20,anchor=CENTER)
    

    lis.heading('Name',text='Name ')
    lis.heading('Surname',text='Surname')
    lis.heading('Date',text='Date')
    lis.heading('Time',text='Time')
    lis.heading('',text='')

    try:
        attenfile = open(path,"r")
        data = attenfile.readlines()
        for i in data:
            lis.insert('','end',values = i)
        
    except Exception as e:
        print(e)

    lis.pack(side=BOTTOM,fill=BOTH)


    
def tutorial ():
#Tutorial Video

    new = Toplevel(root)
    new.title('Face Detection Attendance System(TUTORIAL)')
    new.geometry('520x700')
    new.configure(bg="black")
    new.iconbitmap('C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\logo.ico')

    """vid = Label(new)
    vid.pack(pady=50)
    play = tkvideo("C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\birds.mp4", vid,loop =1,size=(500,680))
    play.play()"""



def infor():
#Information about Company
# Change the path as per your code

    new = Toplevel(root)
    new.title('Face Detection Attendance System(INFORMATION)')
    new.geometry("650x500")
    new.configure(bg="black")
    new.iconbitmap('C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\logo.ico')

    vid = Label(new)
    vid.pack(pady=8)
    play = tkvideo('C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\clogo.mp4', vid,loop=1,size=(290,190))
    play.play()
    scl=Label(new,text=" S²  SOFTWARE ",font=("Berlin Sans FB","24"),fg="black",bg="light blue")
    scl.place(x=121,y=211)
    scl=Label(new,text="  SOLUTIONS   ",font=("Berlin Sans FB","24"),fg="black",bg="yellow")
    scl.place(x=342,y=216)

    cont= Label(new,text="Contact us :",font=("Berlin Sans FB","18"),fg="black",bg="orange")
    cont.place(x=20,y=265)

    call = Label(new,text=" Call On   : ",font=("Berlin Sans FB","16"),bg="black",fg="orange")
    call.place(x=40,y=315)
    num =Label(new,text=" 9561127729 ",font=("Berlin Sans FB","16"),bg="black",fg="cyan")
    num.place(x=140,y=315)

    email = Label(new,text=" Email     : ",font=("Berlin Sans FB","16"),bg="black",fg="orange")
    email.place(x=40,y=365)
    eid =Label(new,text=" satyam95611@gmail.com ",font=("Berlin Sans FB","16"),bg="black",fg="cyan")
    eid.place(x=140,y=365)

    web = Label(new,text=" Website  : ",font=("Berlin Sans FB","16"),bg="black",fg="orange")
    web.place(x=40,y=415)
    webs =Label(new,text="www.S²SoftwareSolutions.com",font=("Berlin Sans FB","16"),bg="black",fg="cyan")
    webs.place(x=140,y=415)


def save():
# Save CSV file
# Change the path as per your code

    filesize = os.path.getsize('C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\attendance.csv')
    if filesize == 0:
        messagebox.showerror("Face Detection Attendance System","File is empty..!")
    else:

        read_file=0
        path="C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\attendance.csv"
        read_file = pd.read_csv(path)

        fpath = filedialog.asksaveasfilename(defaultextension='.xlsx')
        read_file.to_excel(fpath , index = None , header =True)
        messagebox.showinfo("Face Detection Attendance System ","File Saved Sucessfully")


def clear():
#Clear ALL Records
# Change the path as per your code

    with open("C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face Detection\\attendance.csv",'r+') as f:
        
        ans =messagebox.askquestion('Face Detection Attendance System','Do you want to clear Attandance records..?')
        if ans== 'yes':
            f.truncate(0)
        f.close()


def logout():
#LOGOUT
# Change the path as per your code

    res = messagebox.askquestion('Face Detection Attendance System','Do you really want to LogOut...?\nAll the records would be deleted')
    if res == 'yes':
        with open("C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face Detection\\attendance.csv",'r+') as f:
            f.truncate(0)
            f.close()
        root.destroy()
    


scanbt= PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\scan.png')
scan =Button(image=scanbt,relief=RAISED,cursor="hand2",bd=8,command=Scan)
scan.place(x=80,y=80,width=125,height=115)
scl=Label(text="SCAN",font=("Berlin Sans FB","16"),fg="white",bg="grey",padx="5",pady="5",relief=SUNKEN)
scl.place(x=80,y=200,width=115)

flbt= PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\files.png')
file1 =Button(image=flbt,relief=RAISED,cursor="hand2",bd=8,command = files1)
file1.place(x=300,y=80,width=115,height=115)
fil=Label(text="ATTENDANCE FILE",font=("Berlin Sans FB","15"),fg="white",bg="grey",padx="5",pady="5",relief=SUNKEN)
fil.place(x=262,y=200,width=180,height=40)

tubt = PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\tut.png')
tut =Button(image=tubt,relief=RAISED,bd=8,cursor="hand2",command=tutorial)
tut.place(x=530,y=80,width=125,height=115)
tuto=Label(text="VIDEO TUTORIAL",font=("Berlin Sans FB","16"),fg="white",bg="grey",padx="5",pady="5",relief=SUNKEN)
tuto.place(x=495,y=200,width=170)

savebt= PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\save.png')
save = Button(image=savebt,relief=RAISED,cursor="hand2",bd=8,command=save)
save.place(x=80,y=300,width=115,height=115)
savel=Label(text="SAVE",font=("Berlin Sans FB","16"),fg="white",bg="grey",padx="5",pady="5",relief=SUNKEN)
savel.place(x=80,y=420,width=115)

clbt= PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\clear.png')
clear =Button(image=clbt,relief=RAISED,bd=8,cursor="hand2",command=clear)
clear.place(x=300,y=300,width=115,height=115)
cll=Label(text="CLEAR ",font=("Berlin Sans FB","16"),fg="white",bg="grey",padx="5",pady="5",relief=SUNKEN)
cll.place(x=300,y=420,width=115)

logbt = PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\logout.png')
log =Button(image=logbt,relief=RAISED,bd=8,command=logout,cursor="hand2")
log.place(x=530,y=300,width=115,height=115)
logl=Label(text="LOGOUT",font=("Berlin Sans FB","16"),fg="red",bg="grey",padx="5",pady="5",relief=SUNKEN)
logl.place(x=530,y=420,width=115)


info = PhotoImage(file='C:\\Users\\Satyam Singh\\OneDrive\\Desktop\\Python\\Face detection\\Images\\info.png')
infobt =Button(image=info,cursor="hand2",command=infor)
infobt.place(x=652,y=5,width=45,height=45)


root.mainloop()
