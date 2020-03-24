## https://www.simplifiedpython.net/python-gui-login/ codigo de referencia
## Estuardo Ureta
## Isabel Ortiz Naranjo 
from tkinter import *
import os
import psycopg2


def main_account_screen():

    global main_screen
    main_screen = Tk()   # create a GUI window
    main_screen.geometry("2000x1500") # set the configuration of GUI window
    main_screen.title("Account Login") # set the title of GUI window
    main_screen.configure(background = 'black')

    foto = PhotoImage(file = "header.png")
    label2 = Label(main_screen, image = foto)
    label2.place(x=90, y =0)

    # create a Form label
    Label(text="Login Or Register", bg="blue", width="160", height="2", fg='white',font=("Calibri", 13)).place(y=260)

    # create Login Button
    Button(text="Login", height="4", width="60",highlightbackground='magenta', fg='black',command = login).place(x=460, y=400)

    # create a register button
    Button(text="Register", bg='black', height="4", width="60", fg= 'black',highlightbackground='magenta', command = register).place(x=460,y=600)

    main_screen.mainloop() # start the GUI


def register_user():

    # get username and password
    username_info = username.get()
    password_info = password.get()

    # Open file in write mode
    file = open(username_info, "w")

    # write username and password information into file
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    # set a label for showing success information on screen
    Label(register_screen, text="Registration Success", fg="white",bg='black', font=("calibri", 11)).place(x=675,y=600)

# define login function
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("2000x1500")
    login_screen.configure(background = 'black')

    ## CREAR IMAGEN
    foto3 = PhotoImage(file = "header.png")
    label3 = Label(login_screen, image = foto3)
    label3.image =foto3
    label3.place(x=90, y =0)

    Label(login_screen, text="Please enter details below to login",width="160", height="2", bg="blue", fg='white').place(x=5,y=260)
    global username_login_entry
    global password__login_entry
    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()
    Label(login_screen, text="Username * ").place(x=675,y=320)
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.place(x=635,y=345)
    Label(login_screen, text="Password * ").place(x=675,y=385)
    password__login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password__login_entry.place(x=635,y=410)

    Button(login_screen, text="Login", width=10, height=1, command=login_verify).place(x=675,y=470)

def login_verification():
    print("working...")

def login_verify():
    #get username and password

    username1 = username_verify.get()
    password1 = password_verify.get()
    # this will delete the entry after login button is pressed
    username_login_entry.delete(0, END)
    password__login_entry.delete(0, END)

    #The method listdir() returns a list containing the names of the entries in the directory given by path.
    list_of_files = os.listdir()

    #defining verification's conditions
    if username1 in list_of_files:
        file1 = open(username1, "r")   # open the file in read mode
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
        else:
            password_not_recognised()

    else:
        user_not_found()


def login_sucess():
    global login_success_screen   # make login_success_screen global
    global cursor
    login_success_screen = Toplevel(login_screen)

    ## Connecion a base de datos
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "postgres",
                                      host = "localhost",
                                      port = "5432",
                                      database = "intento2")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")


        #Background Color
        login_success_screen.title('Bases de Datos')
        login_success_screen.configure(background = 'black')
        login_success_screen.geometry("2000x1500")

        ## CREAR IMAGEN
        foto = PhotoImage(file = "header.png")
        label2 = Label(login_success_screen, image = foto)
        label2.image =foto
        label2.place(x=90, y =0)

        #ingresar search
        global entry1
        entry1 = Entry(login_success_screen)
        entry1.place(x=120, y= 260)
        button1 = Button(login_success_screen, text="Search", command = searchmusic)
        button1.place(x =120, y= 290)
        button2 = Button(login_success_screen,text='Reportes interesantes', command= reportes)
        button2.place(x=1150, y=750)


        ##Botones para hacer search
        global var
        var = IntVar()
        Radiobutton(login_success_screen, text="Artist    ", variable=var, value=1,fg='white', bg='black').place(x=5, y=260)
        Radiobutton(login_success_screen, text="Genre   ", variable=var, value=2,fg='white' , bg='black').place(x=5, y=280)
        Radiobutton(login_success_screen, text="Canción", variable=var, value=3,fg='white', bg='black').place(x=5, y=300)
        Radiobutton(login_success_screen, text="Album   ", variable=var, value=5,fg='white', bg='black').place(x=5, y=320)


    except(Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

def reportes():
    global reportes_screen
    reportes_screen = Toplevel(login_screen)
    reportes_screen.title("Reportes")
    reportes_screen.geometry("2000x1500")
    reportes_screen.configure(background = 'black')

    Label1 = Label(reportes_screen,text="Los artistas con más álbumes publicados")
    Label1.pack(anchor= 'nw')
    querry = "SELECT artist.name, COUNT(*) AS numero_de_discos FROM album INNER JOIN artist ON album.artistid = artist.artistid GROUP BY album.artistid, artist.name ORDER BY COUNT(*) DESC LIMIT 5"
    postgreSQL_select_Query = querry
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    hola = ""
    for record in records:
        print(record[0],record[1])
        numero = str(record[1])
        hola = hola + record[0]+": "+numero +" albums\n"
        print(type(record))

    print(hola)
    records1=Label(reportes_screen, text=hola, fg = 'white', bg='black')
    records1.pack(anchor= 'nw')
    Label2 =Label(reportes_screen,text="Géneros con más canciones")
    Label2.pack(anchor= 'nw')
    querry2 = "SELECT genre.name, COUNT(*) AS numero_de_canciones FROM track INNER JOIN genre ON genre.genreid = track.genreid GROUP BY genre.name ORDER BY numero_de_canciones DESC LIMIT 5"
    postgreSQL_select_Query = querry2
    cursor.execute(postgreSQL_select_Query)
    records2 = cursor.fetchall()
    adios = ""
    for record in records2:
        print(record[0],record[1])
        numero = str(record[1])
        adios = adios + record[0]+": "+numero +" canciones\n"
        print(type(record))

    print(adios)
    records2=Label(reportes_screen, text=adios, fg = 'white', bg='black')
    records2.pack(anchor= 'nw')
    Label3 = Label(reportes_screen,text="Total de duración de cada playlist")
    Label3.pack(anchor= 'nw')
    querry3 ="SELECT playlist.name, SUM(track.milliseconds/60000) AS duracion_minutos FROM track INNER JOIN playlisttrack ON playlisttrack.trackid = track.trackid INNER JOIN playlist ON playlisttrack.playlistid = playlist.playlistid GROUP BY playlist.name ORDER BY duracion_minutos DESC"
    postgreSQL_select_Query = querry3
    cursor.execute(postgreSQL_select_Query)
    records3 = cursor.fetchall()
    what = ""
    for record in records3:
        print(record[0],record[1])
        numero = str(record[1])
        what = what + record[0]+": "+numero +" minutos\n"
        print(type(record))

    print(adios)
    records3=Label(reportes_screen, text=what, fg = 'white', bg='black')
    records3.pack(anchor= 'nw')

    Label4 = Label(reportes_screen,text="Canciones de mayor duración con la información de sus artistas")
    Label4.pack(anchor= 'nw')
    querry4= "SELECT track.name, artist.name, track.milliseconds/60000 AS duracion_minutos FROM track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid ORDER BY duracion_minutos DESC LIMIT 5"
    postgreSQL_select_Query = querry4
    cursor.execute(postgreSQL_select_Query)
    records4 = cursor.fetchall()
    who = ""
    for record in records4:
        print(record[0],record[1],record[2])
        numero = str(record[2])
        who = who + "Track: "+record[0]+" Artist: "+record[1]+" "+numero +" minutos\n"
        print(type(record))

    print(adios)
    records4=Label(reportes_screen, text=who, fg = 'white', bg='black')
    records4.pack(anchor= 'nw')

def register():
    global register_screen
    global username
    global password
    global username_entry
    global password_entry

    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("2000x1500")
    register_screen.configure(background = 'black')

    ## CREAR IMAGEN
    foto2 = PhotoImage(file = "header.png")
    label2 = Label(register_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)


    # Set text variables
    username = StringVar()
    password = StringVar()

    # Set label for user's instruction
    Label(register_screen, text="Please enter details below", bg="blue", fg='white',width="160", height="2").place(x=5,y=260)

    # Set username label
    username_lable3 = Label(register_screen, text="Username * ")
    username_lable3.place(x=675,y=320)

    # Set username entry
    # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.

    username_entry = Entry(register_screen, textvariable=username)
    username_entry.place(x=635,y=345)

    # Set password label
    password_lable4 = Label(register_screen, text="Password * ")
    password_lable4.place(x=675,y=385)

    # Set password entry
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.place(x=635,y=410)

    # Set register button
    Button(register_screen, text="Register", width=10, height=2, bg="blue", command =register_user).place(x=675,y=470)

