from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox, filedialog
import pymysql
import pandas
# Functionality Part


def toplevel_data(titles, button_text, commands):
    global idEntry, nameEntry, mobileEntry, emailEntry, addressEntry, genderEntry, dobEntry, screen
    screen = Toplevel()
    screen.title(titles)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    mobileLabel = Label(screen, text='Mobile No.', font=('times new roman', 20, 'bold'))
    mobileLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    mobileEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    mobileEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='Email ID', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=commands)
    student_button.grid(row=7, columnspan=2, pady=15)

    if titles == 'Update Student':
        indexing = studentTable.focus()
        content = studentTable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        nameEntry.insert(0, listdata[1])
        mobileEntry.insert(0, listdata[2])
        emailEntry.insert(0, listdata[3])
        addressEntry.insert(0, listdata[4])
        genderEntry.insert(0, listdata[5])
        dobEntry.insert(0, listdata[6])


def iexit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        datalist = content['values']
        newlist.append(datalist)

    table = pandas.DataFrame(newlist, columns=['ID', 'Name', 'Mobile No.', 'Email ID', 'Address', 'Gender', 'D.O.B',
                                               'Added Date', 'Added Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is saved successfully')


def update_data():
    query = ('update student set name=%s, mobile_no=%s, email_id=%s, address=%s, gender=%s, d_o_b=%s, added_date=%s, '
             'added_time=%s where id=%s')
    mycursor.execute(query, (nameEntry.get(), mobileEntry.get(), emailEntry.get(), addressEntry.get(),
                             genderEntry.get(), dobEntry.get(), date, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully',
                        parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing = studentTable.focus()
    print(indexing)
    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully')
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def search_data():
    query = ('select * from student where id=%s or name=%s or mobile_no=%s or email_id=%s or address=%s or gender=%s '
             'or d_o_b=%s')
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), mobileEntry.get(), emailEntry.get(), addressEntry.get(),
                             genderEntry.get(), dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def add_data():
    if (idEntry.get() == '' or nameEntry.get() == '' or mobileEntry.get() == '' or emailEntry.get() == '' or
            addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == ''):
        messagebox.showerror('Error', 'All Fields Are Required', parent=screen)
    else:
        try:
            query = 'insert into student values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            mycursor.execute(query, (idEntry.get(), nameEntry.get(), mobileEntry.get(), emailEntry.get(),
                                     addressEntry.get(), genderEntry.get(), dobEntry.get(), date, currenttime))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data Added Successfully. Do you want to clean the form?',
                                         parent=screen)
            if result:
                idEntry.delete(0, END)
                nameEntry.delete(0, END)
                mobileEntry.delete(0, END)
                emailEntry.delete(0, END)
                addressEntry.delete(0, END)
                genderEntry.delete(0, END)
                dobEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Id Cannot Be Repeated', parent=screen)
            return

        query = 'select * from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', END, values=data)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            # con = pymysql.connect(host='localhost', user='root', password='kiit')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return
        try:
            query = 'create database studentmanagementsystem'
            mycursor.execute(query)
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
            query = ('create table student(ID int not null primary key, Name varchar(30), Mobile_No varchar(30),'
                     'Email_ID varchar(30), Address varchar(100), Gender varchar(20), D_O_B varchar(20),'
                     'Added_Date varchar(50), Added_Time varchar(50))')
            mycursor.execute(query)
        except:
            query = 'use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'Database Connection Is Successful', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False, False)

    hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    hostEntry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)


count = 0
text = ''


def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(300, slider)


def clock():
    global date, currenttime
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)


# GUI Port
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(False, False)
root.title('Student Management System')

datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()
s = 'Student Management System'  # s[count] = t (when count is 1)
sliderLabel = Label(root, font=('arial', 28, 'italic bold'), foreground='green', width=30)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='Connect To Database', command=connect_database)
connectButton.place(x=980, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_image = PhotoImage(file='image/student.png')
logo_label = Label(leftFrame, image=logo_image)
logo_label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, state=DISABLED,
                              command=lambda: toplevel_data('Add Student Info', 'ADD', add_data))
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Search Student', 'SEARCH', search_data))
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25, state=DISABLED, command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25, state=DISABLED,
                                 command=lambda: toplevel_data('Update Student', 'UPDATE', update_data))
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25, state=DISABLED, command=show_student)
showstudentButton.grid(row=5, column=0, pady=20)

exportstudentButton = ttk.Button(leftFrame, text='Export Data', width=25, state=DISABLED, command=export_data)
exportstudentButton.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='Exit', width=25, command=iexit)
exitButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('ID', 'Name', 'Mobile No.', 'Email ID', 'Address', 'Gender', 'D.O.B',
                            'Added Date', 'Added Time'), xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)

studentTable.heading('ID', text='ID')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile No.', text='Mobile No.')
studentTable.heading('Email ID', text='Email ID')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

studentTable.column('ID', width=50, anchor=CENTER)
studentTable.column('Name', width=200, anchor=CENTER)
studentTable.column('Mobile No.', width=150, anchor=CENTER)
studentTable.column('Email ID', width=200, anchor=CENTER)
studentTable.column('Address', width=200, anchor=CENTER)
studentTable.column('Gender', width=120, anchor=CENTER)
studentTable.column('D.O.B', width=180, anchor=CENTER)
studentTable.column('Added Date', width=150, anchor=CENTER)
studentTable.column('Added Time', width=150, anchor=CENTER)

style = ttk.Style()
style.configure('Treeview', rowheight=40, font=('arial', 12, 'bold'), foreground='black', background='yellow',
                fieldbackground='yellow')
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='red')

studentTable.config(show='headings')

root.mainloop()
