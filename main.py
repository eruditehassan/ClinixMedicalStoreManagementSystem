#We have imported all the functions, that we have used in our program here.
from Scrapper import *
from exporting_excel import*
from xlwt import *
import requests
from bs4 import BeautifulSoup
from random import *
from pickle import *
from edit_med import *
import os
from fpdf import FPDF
import datetime
pdf = FPDF()
from pickle import *
from re import *
import PIL
from PIL import ImageTk, Image
import pyzbar.pyzbar as pbar
import requests
import cv2
import matplotlib as plt
title =Image.open("clinix logo.png")
import numpy as np
from tkinter import *
import tkinter.messagebox;x=1
while x:
    class Everything:
        #This class generate a label along with three entries so that whenever we replace a value in a quantity
        #then it automatically generate a label for price.
        def __init__(self,med,counter,lis):
            self.name = lis[med][0]
            self.name = self.name.split(" ")
            self.name = self.name[0]

            label = Label(text=self.name)
            label.place(x=10 , y=30*(counter+1)+280)
            
            self.unit_price = lis[med][1]
            self.stock = lis[med][2]
            
            self.qty = StringVar()
            self.qty.set("0")

            self.disc = StringVar()
            self.disc.set("0")

            self.disc_percent = StringVar()
            self.disc_percent.set("0")

            self.price = StringVar()
            self.label_price = Label(textvariable=self.price)

            self.value = counter
            self.qty_entry = Entry(width=4, textvariable=self.qty)
            self.qty_entry.place(x=150,y=30*(self.value+1)+280)

            self.disc_entry = Entry(width=4, textvariable=self.disc)
            self.disc_entry.place(x=200,y=30*(self.value+1)+280)

            self.disc_entry_percent = Entry(width=4, textvariable=self.disc_percent)
            self.disc_entry_percent .place(x=250,y=30*(self.value+1)+280)

            self.qty_entry.bind("<Return>", lambda x:self.quantity())
            self.disc_entry.bind("<Return>", lambda y:self.discount())
            self.disc_entry_percent.bind("<Return>", lambda z:self.discount_percent())

        def quantity(self):
            if self.qty.get().isnumeric():
                self.price.set((float(self.qty.get())*self.unit_price)-float(self.disc.get()))
                self.label_price.place(x=300,y=30*(self.value+1)+280)
            else:
                tkinter.messagebox.showerror(title="invalid input",message="Enter a number",parent=master)

        def discount(self):
            if self.disc.get().isnumeric() or  ((self.disc.get()).replace(".","")).isnumeric():
                self.price.set(self.unit_price*float(self.qty.get())-float(self.disc.get()))
                self.disc_percent.set((float(self.disc.get())/(float(self.qty.get())*self.unit_price))*100)
            else:
                tkinter.messagebox.showerror(title="invalid input",message="Enter a number",parent=master)

        def discount_percent(self):
            if (self.disc_percent.get().isnumeric()or  ((self.disc_percent.get()).replace(".","")).isnumeric()) and (self.disc.get().isnumeric() or ((self.qty.get()).replace(".","")).isnumeric()):
                self.disc.set(str(self.unit_price*float(self.qty.get())*float(self.disc_percent.get())/100))
                self.price.set(self.unit_price*int(self.qty.get())-float((float(self.disc_percent.get())/100)*(float(self.qty.get())*self.unit_price)))
            else:
                tkinter.messagebox.showerror(title="invalid input",message="Enter a number",parent=master)

    def Quit():
        global x
        x=0
        if counter==0:
            global master
            master.destroy()

    master = Tk()
    quit = Button(master,text="Quit" , command=Quit , bg="red" , fg="white")
    quit.place(x=350 , y=150)


    counter = 0;event_list = []

    master.configure(bg="white")
    master.geometry("400x700")
    search_entry = Entry(master,bg="lavender")
    search_entry.place(x=150,y=150)
    search_entry.focus_set()
    lis=[]

    # This module will enable the medical store empolyes to search medicines by image.
    def code_image():
        def by_image(event):
            if os.path.isfile(entry.get()):
                path = entry.get()
                test = cv2.imread(path,cv2.IMREAD_REDUCED_GRAYSCALE_8)
                threshold = cv2.adaptiveThreshold(test,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,10)
                kernel = np.ones((2,2),np.float32)/2
                smooth = cv2.filter2D(threshold,-1,kernel)
                cv2.imshow("test",threshold)
                cv2.imshow("test1",test)
                cv2.imshow("test 3",smooth)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                import pyzbar.pyzbar as pbar
                data = pbar.decode(test)
                # This module code above scans the image and provides a bar code number
                barcode = str(data[0].data)
                barcode = barcode.replace("b","")
                barcode = barcode.replace("'","")
                source = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc='+barcode)
                # We have used an API to fetch results from UPC Item Database
                data = source.json()
                # The obtained data is in JSON coding, so we use method to convert it into a python dictionary
                name=(data['items'][0]['title']).split(" ")
                print(name)
                callback_bar(name[0])
                # The data is first enclosed in a dictionary, which is in a list, and the list is in a dictionary.


        Image = Toplevel(master)
        label = Label(Image,text="specify the path of the image")
        entry = Entry(Image)
        label.pack()
        entry.pack()
        entry.bind("<Return>",by_image)

    def code_mobile():
        #It decodes the barcode from mobile cam.
        def by_mobile(event):
            while True:
                im_res = requests.get(url.get()+"/shot.jpg")
                im_array = np.array(bytearray(im_res.content) , dtype=np.uint8)
                im = cv2.imdecode(im_array , -1)
                cv2.imshow("nothing" , im)
                decode = pbar.decode(im)
                if cv2.waitKey(1) == 27:
                    cv2.destroyAllWindows()
                if decode:
                    break
                    cv2.destroyAllWindows()
            barcode = str(decode[0].data)
            barcode = barcode.replace("b","")
            barcode = barcode.replace("'","")
            source = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc='+barcode)
            data = source.json()
            name=(data['items'][0]['title']).split(" ")
            print(name)
            callback_bar(name[0])
        url = StringVar()
        url.set("http://10.7.12.5:8080")
        mobile = Toplevel(master)
        label = Label(mobile,text="specify the ip you see on your mobile screen")
        entry = Entry(mobile,textvariable=url)
        label.pack()
        entry.pack()
        entry.bind("<Return>",by_mobile)

    def callback_bar(name):
    #We called the file which stored our data in pickle format. This increases the efficiency of our program.
            global lis
            medicine = name
            print(medicine)
            pickle_in = open("medicine_pickle.pickle", "rb")
            pickle_file = load(pickle_in)
            lis = []
            medicine = medicine.casefold()
            for items in range(len(pickle_file)):
                if medicine in pickle_file[items][0]:
                    lis.append(pickle_file[items])
            if len(lis) == 0:
                tkinter.messagebox.showinfo(title="no result",message="no results were found for your requested search")
            else:
                search = Toplevel()
                search.title("search")
                search_entry.delete(0,'end')

    def search_by_barcode():
        Barcode=Toplevel(master)
        image=Button(Barcode,text="Search by Image",command=code_image)
        image.pack()
        mobile=Button(Barcode,text="Search by Mobile",command=code_mobile)
        mobile.pack()

    barcode = Button(master,text="Search by Barcode", bg="white" ,command=search_by_barcode)
    barcode.place(x=25, y=210)
    label=Label(master, text="Name                                      Qty        Discount    %age          price")
    label.place(x=0, y=280)

    def bill():
        # This module will bill the purchased items and provide an invoice.
        total = 0
        for index in range(len(event_list)):
            total += float(event_list[index].price.get())
        total_price = Label(text=str(total))
        total_price.place(x=150,y=630)
        New = Toplevel()
        confirm = Label(New,text="Do you want to create a new bill")

        def new():
            master.destroy()
            pdf.add_page()
            pdf.image('clinix logo.png', x=75, y=0, w=50, h=20, type='PNG',)

            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0,30,"name\t\t\t\t\tprice per unit\t\t\t\t\tquantity\t\t\t\t\tprice")
            for elements in event_list:
                pdf.multi_cell(0,5 , elements.name + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+str(elements.unit_price)+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+elements.qty.get()+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+elements.price.get())
            pdf.multi_cell(0,5 ,"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"   "total="+str(total))
            name = str(datetime.datetime.now());name="c"+name;name=name.replace("-","");name=name.replace(".","");name=name.replace(":","")
            pdf.multi_cell(0,5 ,"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"   "TID="+name)
            pdf.output((name+".pdf"))
        Yes = Button(New,text="yes",command=new)
        NO = Button(New,text="no",command=New.destroy)
        confirm.pack()
        Yes.pack()
        NO.pack()
        New.mainloop()
    def callback(event):

            global lis
            # This is search entry.
            medicine= search_entry.get()
            # The medicine list has been imported.
            pickle_in =open("medicine_pickle.pickle", "rb")
            # it is being imported as a python list.
            l = load(pickle_in)
            lis=[]
            medicine=medicine.casefold()
            for items in range(len(l)):
                if medicine in l[items][0].casefold():
                    lis.append(l[items])
                    # If searched medicine is in the list, then it will store that in an empty list for
                    # futher processing.
            if len(lis)==0:
                tkinter.messagebox.showinfo(title="no result",message="no results were found for your requested search")
            else:
                search = Toplevel()
                search.title("search")
                search_entry.delete(0,'end')

            def entry(med):
                search.destroy()
                global event_list , counter
                event_list.append(0)
                event_list[counter] = Everything(med,counter,lis)
                counter += 1

            for med in range(len(lis)):
                button=(Button(search, text=lis[med][0],bg="orange", fg="white", command=lambda med=med: entry(med)))
                button.pack(side="top")

    def Update_med():

        scrapper()
        exporting_excel()

    canvas=Canvas(master, height=150, width=400)
    basewidth = 300
    title = title.resize((400, 150), PIL.Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(title)
    item4 = canvas.create_image(200,100, image=photo)
    edit=Button(master,text="Edit Medicine", bg="white" ,command=edit_medicine)
    edit.place(x=300,y=210)
    canvas.place(x=0,y=0)
    update=Button(master,text="UPDATE", bg="white" , command=Update_med)
    update.place(x=175,y=210)
    search_entry.bind("<Return>", callback)
    search_button = Button(master, text="Search",bd=0.5, bg="white" , command=lambda : callback("<Return>"))
    search_button.place(x=175,y=175)
    finalize=Button(master,text="bill", bg="white" , command=bill)
    finalize.place(x=150,y=650)
    master.mainloop()
