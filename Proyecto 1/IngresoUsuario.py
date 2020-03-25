## https://www.simplifiedpython.net/python-gui-login/ codigo de referencia
## Estuardo Ureta
## Isabel Ortiz Naranjo 
from tkinter import *
from PIL import Image, ImageTk
import os
import psycopg2

## codigo para el login tomado de https://www.simplifiedpython.net/python-gui-login/

def main_account_screen():

    global main_screen
    main_screen = Tk()   # create a GUI window
    main_screen.geometry("2000x1500") #set the configuration of GUI window
    main_screen.title("Login") # set the title of GUI window
    main_screen.configure(background = 'pink')

    ## CREAR IMAGEN
    load = Image.open("Logo.jpg")
    foto = ImageTk.PhotoImage(load)
    label = Label(main_screen, image = foto)
    label.place(x=750, y =50)

    # create a Form label
    Label(text="Login Or Register", bg="white", width="160", height="2", fg='white',font=("Calibri", 13)).place(y=260)

    # create Login Button
    Button(text="Login", height="4", width="60",highlightbackground='magenta', fg='black',command = login).place(x=460, y=400)

    # create a register button
    Button(text="Register", bg='black', height="4", width="60", fg= 'black',highlightbackground='magenta', command = register).place(x=460,y=600)

    main_screen.mainloop() # start the GUI

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
    load = Image.open("Logo.jpg")
    foto2 = ImageTk.PhotoImage(load)
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
    load = Image.open("Logo.jpg")
    foto3 = ImageTk.PhotoImage(load)
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
                                      password = "Delvalle2018",
                                      host = "localhost",
                                      port = "5433",
                                      database = "proyecto")

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
        load = Image.open("Logo.jpg")
        foto = ImageTk.PhotoImage(load)
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

##@ TODO
    Label5 = Label(reportes_screen,text="Usuarios que han registrado más canciones")
    Label5.place(x= 550, y=0)


    Label6 = Label(reportes_screen,text="Promedio de duración de canciones por género")
    Label6.place(x=550,y=300)
    querry6 = "SELECT genre.name, AVG(track.milliseconds/60000) AS promedio_duracion_minutos FROM track INNER JOIN genre ON genre.genreid = track.genreid GROUP BY genre.name ORDER BY promedio_duracion_minutos DESC"
    postgreSQL_select_Query = querry6
    cursor.execute(postgreSQL_select_Query)
    records6 = cursor.fetchall()
    ask = ""
    for record in records6:
        print(record[0],record[1])
        numero = str(record[1])
        ask = ask +record[0]+" "+numero +" minutos\n"
        print(type(record))

    print(ask)
    records6=Label(reportes_screen, text=ask, fg = 'white', bg='black')
    records6.place(x= 550, y=320)


    Label7 = Label(reportes_screen,text="Cantidad de artistas diferentes por playlist")
    Label7.place(x=1150, y=0)
    querry7 = "SELECT playlist.name, COUNT(DISTINCT artist.name) AS numero_artistas FROM track INNER JOIN album ON track.albumid=album.albumid INNER JOIN artist ON artist.artistid = album.artistid INNER JOIN playlisttrack ON playlisttrack.trackid = track.trackid INNER JOIN playlist ON playlist.playlistid = playlisttrack.playlistid GROUP BY playlist.name ORDER BY numero_artistas DESC"
    postgreSQL_select_Query = querry7
    cursor.execute(postgreSQL_select_Query)
    records7 = cursor.fetchall()
    loco = ""
    for record in records7:
        print(record[0],record[1])
        numero = str(record[1])
        loco = loco +record[0]+" "+numero +" minutos\n"
        print(type(record))

    print(loco)
    records7=Label(reportes_screen, text=loco, fg = 'white', bg='black')
    records7.place(x=1150, y=25)

    Label8 = Label(reportes_screen,text="Los artistas con más diversidad de géneros musicales")
    Label8.place(x=1100,y= 400)
    querry8 ="SELECT artist.name, COUNT(DISTINCT genre.name) AS numero_generos FROM track JOIN album ON album.albumid = track.albumid JOIN artist ON album.artistid = artist.artistid JOIN genre ON track.genreid = genre.genreid GROUP BY artist.name ORDER BY numero_generos DESC LIMIT 5"
    postgreSQL_select_Query = querry8
    cursor.execute(postgreSQL_select_Query)
    records8 = cursor.fetchall()
    palabra = ""
    for record in records8:
        print(record[0],record[1])
        numero = str(record[1])
        palabra = palabra +record[0]+" "+numero +" minutos\n"
        print(type(record))

    print(palabra)
    records8=Label(reportes_screen, text=palabra, fg = 'white', bg='black')
    records8.place(x=1150, y=425)


def searchmusic ():
    select = var.get()
    x1 = entry1.get()
    x2 = 'artist.name, track.name'
    whereclause = ''
    if select == 1:
        selection = 'track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        whereclause = "artist.name='"+x1+"'"
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+" LIMIT 10"
        querry =str(querry)
        print(querry)
        postgreSQL_select_Query = querry
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()

        hola = ""
        for record in records:
            print(record[0],record[1])
            hola = hola + record[0]+": "+record[1]+"\n"
            print(type(record))

        print(hola)
        records1=Label(login_success_screen, text=hola, fg = 'white', bg='black')
        records1.place(x= 500, y = 300)
    if select == 2:
        selection = 'track INNER JOIN genre ON genre.genreid = track.genreid INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        whereclause = "genre.name='" +x1+ "'"
        x2 = 'genre.name, artist.name, track.name'
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+" LIMIT 10"
        querry =str(querry)
        print(querry)
        postgreSQL_select_Query = querry
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()

        hola = ""
        for record in records:
            print(record[0],record[1],record[2])
            hola = hola + record[0]+": "+record[1]+" "+record[2]+"\n"
            print(type(record))

        print(hola)
        records1=Label(login_success_screen, text=hola, fg = 'white', bg='black')
        records1.place(x= 500, y = 300)
    if select == 3:
        selection = 'track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        whereclause = "track.name='"+x1+ "'"
        x2= 'artist.name, track.name, album.title'
        records = cursor.fetchall()
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+" LIMIT 10"
        querry =str(querry)
        print(querry)
        postgreSQL_select_Query = querry
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()

        hola = ""
        for record in records:
            print(record[0],record[1])
            hola = hola + record[0]+": "+record[1]+"\n"
            print(type(record))

        print(hola)
        records1=Label(login_success_screen, text=hola, fg = 'white', bg='black')
        records1.place(x= 500, y = 300)
    if select == 5:
        selection = 'track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        whereclause = " album.title='"+x1+"'"
        records = cursor.fetchall()
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+" LIMIT 10"
        querry =str(querry)
        print(querry)
        postgreSQL_select_Query = querry
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()

        hola = ""
        for record in records:
            print(record[0],record[1])
            hola = hola + record[0]+": "+record[1]+"\n"
            print(type(record))

        print(hola)
        records1=Label(login_success_screen, text=hola, fg = 'white', bg='black')
        records1.place(x= 500, y = 300)



def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

def delete_user_not_found_screen():
    user_not_found_screen.destroy()

main_account_screen() # call the main_account_screen() function