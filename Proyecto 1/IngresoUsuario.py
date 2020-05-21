## https://www.simplifiedpython.net/python-gui-login/ codigo de referencia
## Estuardo Ureta
## Isabel Ortiz Naranjo 
from tkinter import *
from PIL import Image, ImageTk
import psycopg2
from tkinter import ttk
import os
import csv
import pymongo
from pymongo import MongoClient
from tkcalendar import *

def main_account_screen():

    global main_screen
    main_screen = Tk()   # create a GUI window
    main_screen.geometry("2000x1500") #set the configuration of GUI window
    main_screen.title("Login") # set the title of GUI window
    main_screen.configure(background = 'black')

    ## CREAR IMAGEN
    load = Image.open("header.png")
    foto = ImageTk.PhotoImage(load)
    label = Label(main_screen, image = foto)
    label.place(x=90, y =5)

    # form label
    Label(text="Login Or Register", bg="purple", width="100", height="2", fg='white',font=("Lucida Calligraphy", 18)).place(x=-60, y =300)

    # boton login
    Button(text="Login", height="4", width="60",highlightbackground='magenta', fg='black',command = login).place(x=560, y=400)

    # boton registro
    Button(text="Register", height="4", width="60", fg= 'black',highlightbackground='magenta', command = register).place(x=560,y=500)
    
    # Conexión a la base de datos 
    global cursor
    global connection
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

    except(Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

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
    load = Image.open("header.png")
    foto2 = ImageTk.PhotoImage(load)
    label2 = Label(register_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)


    # Set text variables
    global var2
    username = StringVar()
    password = StringVar()
    var2 = IntVar()

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

    username_info = username.get() # Obtener el user 
    password_info = password.get() # Obtener la contraseña
    select1 = var2.get()
    admin = 0
    if select1 == 0:
        admin = 0
    if select1 == 1:
        admin = 1

    sql = "INSERT INTO usuario (username, password, isAdmin) VALUES (%s, %s, %s)"
    val = (username_info,password_info,admin)
    try:
        cursor.execute(sql,val)
        connection.commit()
        print(cursor.rowcount,"record inserted")
        # set a label for showing success information on screen
        Label(register_screen, text="Registration Success", fg="white",bg='black', font=("calibri", 11)).place(x=675,y=600)
    except:
        print("No se pudo crear usuario")
        Label(register_screen,text="No se pudo generar usuario", fg='white', bg='black', font=('calibri',11)).place(x=675,y=600)

    username_entry.delete(0, END)
    password_entry.delete(0, END)


# define login function
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("2000x1500")
    login_screen.configure(background = 'black')

    ## CREAR IMAGEN
    load = Image.open("header.png")
    foto3 = ImageTk.PhotoImage(load)
    label3 = Label(login_screen, image = foto3)
    label3.image =foto3
    label3.place(x=90, y =0)

    Label(login_screen, text="Please enter details below to login",width="160", height="2", bg="blue", fg='white').place(x=150,y=260)
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

def login_verify():
        #get username and password
    global usuario
    username1 = username_verify.get()
    password1 = password_verify.get()
    # this will delete the entry after login button is pressed
    username_login_entry.delete(0, END)
    password__login_entry.delete(0, END)

    querryusuario = "SELECT username FROM usuario"
    postgreSQL_select_Query = querryusuario
    cursor.execute(postgreSQL_select_Query)
    recordsu = cursor.fetchall()
    lola = ""
    for record in recordsu:
        print(record[0])
        lola = lola + record[0]
        print(type(record))
    print(lola)
    if username1 in lola:
        print ("Se pudo")
        querryusuario = "SELECT username, password FROM usuario WHERE username = '"+username1+"' "
        postgreSQL_select_Query = querryusuario
        cursor.execute(postgreSQL_select_Query)
        recordspass = cursor.fetchall()
        lolo = ""
        for record in recordspass:
            print(record[0],record[1])
            lolo = lolo + record[0]+" "+record[1]
            print(type(record))
            if password1 in lolo:
                print("Sí se pudo")
                usuario = username1
                login_sucess()
            else:
                password_not_recognised()
    else:
        user_not_found()

def login_sucess():
    global login_success_screen  
    login_success_screen = Toplevel(login_screen)

    #Background Color
    login_success_screen.title('Música')
    login_success_screen.configure(background = 'black')
    login_success_screen.geometry("2000x1500")

    ## CREAR IMAGEN
    load = Image.open("header.png")
    foto2 = ImageTk.PhotoImage(load)
    label2 = Label(login_success_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    #ingresar a buscar
    global entry1
    entry1 = Entry(login_success_screen)
    entry1.place(x=120, y= 260)
    button1 = Button(login_success_screen, text="Buscar", command = searchmusic)
    button1.place(x =120, y= 290)
    button2 = Button(login_success_screen,text='Reportes', command= reportes)
    button2.place(x=1150, y=750)


    # Botones buscar
    global var
    var = IntVar()
    Radiobutton(login_success_screen, text="Artist    ", variable=var, value=1,fg='white', bg='black').place(x=5, y=260)
    Radiobutton(login_success_screen, text="Genre   ", variable=var, value=2,fg='white' , bg='black').place(x=5, y=280)
    Radiobutton(login_success_screen, text="Canción", variable=var, value=3,fg='white', bg='black').place(x=5, y=300)
    Radiobutton(login_success_screen, text="Album   ", variable=var, value=5,fg='white', bg='black').place(x=5, y=320)

##botones menu principal
    Buttonagregar = Button(login_success_screen,text='Agregar una nueva cancion,album o artista',width="30", height="1",command = agregarcancion).place(x=5,y=540)
    Butoonquitar = Button(login_success_screen,text="Quitar una cancion,album o artista",width="30", height="1", command = quitarcancion).place(x=5,y=565)
    Buttoneditar = Button(login_success_screen,text="Editar una cancion,album o artista",width="30", height="1", command= editarcancion).place(x=5,y=590)
    Buttonactivar = Button(login_success_screen,text="Activar o inactivar una cancion",width="30", height="1", command= activar).place(x=5,y=615)
    Bottonmongo = Button(login_success_screen, text= "Mongodb",width="30", height="1", command = mongoloco).place(x=5,y=640)
    Bottondebitacora = Button(login_success_screen, text= "Bitacora",width="30", height="1", command = debitacora).place(x=5,y=665)

#Bitacora implementada

def debitacora():
    bitacora_screen = Toplevel(login_screen)
    bitacora_screen.title("Bitacota")
    bitacora_screen.geometry("2000x1500")
    bitacora_screen.configure(background = 'black')

    foto2 = PhotoImage(file = "header.png")
    label2 = Label(bitacora_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)


#Connexion con MongoDB
def mongoloco():
    global cal1
    global mongo_screen

    mongo_screen = Toplevel(login_screen)
    mongo_screen.title("Mongodb")
    mongo_screen.geometry("2000x1500")
    mongo_screen.configure(background = 'black')

    foto2 = PhotoImage(file = "header.png")
    label2 = Label(mongo_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    label3 =Label(mongo_screen,text='Ingrese la fecha que para la que desea ver las compras:')
    label3.place(x=550,y=300)

    style = ttk.Style(mongo_screen)
    style.theme_use('clam')
    cal1 = Calendar(mongo_screen,selectmode='day',background="black", disabledbackground="black", bordercolor="black",
                    headersbackground="black", normalbackground="black", foreground='white',
                    normalforeground='white', headersforeground='white')
    cal1.config(background = 'black')
    cal1.place(x=600, y= 330)

    bottonclick = Button(mongo_screen, text='Seleccionar fecha',command = calval1)
    bottonclick.place(x=650, y=600)



def calval1():
    fecha_sel = cal1.get_date()
    labelFecha = Label(mongo_screen,text= "La fecha seleccionada es: "+ fecha_sel)
    labelFecha.place(x=600 ,y=535)

    ##intercambiable
    client = MongoClient('localhost', 27017)
    print(client)
    labelMongo = Label(mongo_screen, text=client).place(x=450,y=570)
    db = client['proyecto2']
    ventas = db['ventas']

def agregarcancion():
    agregar_screen = Toplevel(login_screen)
    agregar_screen.title("Agregar una nueva cancion,album o artista")
    agregar_screen.geometry("2000x1500")
    agregar_screen.configure(background = 'black')
    global var6
    global entryname
    global entrynamealb
    global entrynamesong
    global entrymilisec
    var6 = IntVar()

    #CREAR IMAGEN
    load = Image.open("header.png")
    foto2 = ImageTk.PhotoImage(load)
    label2 = Label(agregar_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    label3 =Label(agregar_screen,text='Ingrese el nombre del artista:')
    label3.place(x=200,y=260)
    entryname = Entry(agregar_screen)
    entryname.place(x=200, y=290)

    label3 =Label(agregar_screen,text='Ingrese el nombre del album del artista:')
    label3.place(x=425,y=260)
    entrynamealb = Entry(agregar_screen)
    entrynamealb.place(x=425, y=290)

    label3 =Label(agregar_screen,text='Ingrese el nombre de la cancion:')
    label3.place(x=700,y=260)
    entrynamesong = Entry(agregar_screen)
    entrynamesong.place(x=700, y=290)

    label3 =Label(agregar_screen,text='Ingrese el numero de milisegundos de la cancion:')
    label3.place(x=1000,y=260)
    entrymilisec = Entry(agregar_screen)
    entrymilisec.place(x=1000, y=290)

    button1 = Button(agregar_screen, text="Agregar", command = agregar)
    button1.place(x =1300, y= 700)

# Funcion para quitar 
def quitarcancion():
    quitar_screen = Toplevel(login_screen)
    quitar_screen.title("Quitar")
    quitar_screen.geometry("2000x1500")
    quitar_screen.configure(background = 'black')
    global var4
    global entryquit

    #CREAR IMAGEN
    load = Image.open("header.png")
    foto2 = ImageTk.PhotoImage(load)
    label2 = Label(quitar_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    var4 = IntVar()
    Radiobutton(quitar_screen, text="Artist    ", variable=var4, value=1,fg='white', bg='black').place(x=5, y=260)
    Radiobutton(quitar_screen, text="Album   ", variable=var4, value=2,fg='white' , bg='black').place(x=5, y=280)
    Radiobutton(quitar_screen, text="Canción", variable=var4, value=3,fg='white', bg='black').place(x=5, y=300)

    label3 =Label(quitar_screen,text='Ingrese lo que quiere quitar:')
    label3.place(x=500,y=260)
    entryquit = Entry(quitar_screen)
    entryquit.place(x=500, y=290)

    button1 = Button(quitar_screen, text="Eliminar",command =quitar)
    button1.place(x =1300, y= 700)

def quitar():
    global quitar_screen
    quitar_screen=Toplevel(login_screen)
    quitar_screen.title("Success")
    quitar_screen.geometry("150x100")
    select = var4.get()
    x5 = entryquit.get()

    if select == 1:
        #Guardamos en una variable el artistid
        querryidartist = "SELECT artist.artistid FROM artist WHERE artist.name = '"+x5+"'"
        postgreSQL_select_Query = querryidartist
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        saberwho = ""
        for i in intentos:
            numcaca = str(i[0])
            saberwho = saberwho + numcaca

        #Guardamos en una lista los albumid
        querryidalbum = "SELECT album.albumid FROM album WHERE album.artistid = '"+saberwho+"'"
        postgreSQL_select_Query = querryidalbum
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        saberwhat = ""
        saberwhatLIST = []
        for i in intentos:
            numcaca = str(i[0])
            saberwhatLIST.append(numcaca)
            saberwhat = saberwhat + numcaca
        #DELETE tracks del artista
        try:
            rati = "DELETE FROM track WHERE albumid IN (SELECT album.albumid FROM album WHERE album.artistid = '"+saberwho+"')"
            print(rati)
            cursor.execute(rati)
            connection.commit()
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(quitar_screen, text="Eliminado ").pack()
                Button(quitar_screen, text="OK", command=delete_quitar).pack()
        except:
            Label(quitar_screen, text="No se pudo eliminar ").pack()
            Button(quitar_screen, text="OK", command=delete_quitar).pack()
        #DELETE albums del artista
        try:
            rati = "DELETE FROM album WHERE artistid = '"+saberwho+"'"
            print(rati)
            cursor.execute(rati)
            connection.commit()
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(quitar_screen, text="Eliminado ").pack()
                Button(quitar_screen, text="OK", command=delete_quitar).pack()
        except:
            Label(quitar_screen, text="No se pudo eliminar ").pack()
            Button(quitar_screen, text="OK", command=delete_quitar).pack()
        #DELETE el artista
        try:
            rati = "DELETE FROM artist WHERE artistid = '"+saberwho+"'"
            print(rati)
            cursor.execute(rati)
            connection.commit()
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(quitar_screen, text="Eliminado ").pack()
                Button(quitar_screen, text="OK", command=delete_quitar).pack()
        except:
            Label(quitar_screen, text="No se pudo eliminar ").pack()
            Button(quitar_screen, text="OK", command=delete_quitar).pack()

    if select == 2:
        try:
            wodi = "DELETE FROM track WHERE albumid = (SELECT album.albumid FROM album WHERE album.title = '"+x5+"')"
            print(wodi)
            cursor.execute(wodi)
            connection.commit()
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(quitar_screen, text="Eliminado ").pack()
                Button(quitar_screen, text="OK", command=delete_quitar).pack()
        except:
            Label(quitar_screen, text="No se pudo eliminar ").pack()
            Button(quitar_screen, text="OK", command=delete_quitar).pack()
        try:
            k = "DELETE FROM album WHERE album.title = '"+x5+"'"
            print(k)
            cursor.execute(k)
            connection.commit()
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(quitar_screen, text="Eliminado ").pack()
                Button(quitar_screen, text="OK", command=delete_quitar).pack()
        except:
            Label(quitar_screen, text="No se pudo eliminar ").pack()
            Button(quitar_screen, text="OK", command=delete_quitar).pack()



    if select == 3:
        try:
            vo ="DELETE FROM track WHERE name = '"+x5+"'"
            print(vo)
            cursor.execute(vo)
            connection.commit()
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(quitar_screen, text="Eliminado ").pack()
                Button(quitar_screen, text="OK", command=delete_quitar).pack()
            else:
                Label(quitar_screen, text="No se encontro una cancion con ese nombre ").pack()
                Button(quitar_screen, text="OK", command=delete_quitar).pack()

        except:
            Label(quitar_screen, text="No se pudo eliminar ").pack()
            Button(quitar_screen, text="OK", command=delete_quitar).pack()


def editarcancion():
    editar_screen = Toplevel(login_screen)
    editar_screen.title("Editar")
    editar_screen.geometry("2000x1500")
    editar_screen.configure(background = 'black')

    ## CREAR IMAGEN
    load = Image.open("header.png")
    foto2 = ImageTk.PhotoImage(load)
    label2 = Label(editar_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)


    global entrynew
    global entryprim
    global var3
    var3 = IntVar()

    Radiobutton(editar_screen, text="Artist    ", variable=var3, value=1,fg='white', bg='black').place(x=5, y=260)
    Radiobutton(editar_screen, text="Album   ", variable=var3, value=2,fg='white' , bg='black').place(x=5, y=280)
    Radiobutton(editar_screen, text="Canción", variable=var3, value=3,fg='white', bg='black').place(x=5, y=300)

    label3 =Label(editar_screen,text='Ingrese el valor viejo:')
    label3.place(x=500,y=260)
    entryprim = Entry(editar_screen)
    entryprim.place(x=500, y=290)

    label3 =Label(editar_screen,text='Ingrese el valor nuevo:')
    label3.place(x=800,y=260)
    entrynew = Entry(editar_screen)
    entrynew.place(x=800, y= 290)
    button1 = Button(editar_screen, text="Modificar",command =modificar)
    button1.place(x =1300, y= 700)

def modificar():
    global modificar_screen
    modificar_screen = Toplevel(login_screen)
    modificar_screen.title("Success")
    modificar_screen.geometry("150x100")

    select2 = var3.get()
    x2 = entryprim.get()
    x3= entrynew.get()
    if select2 == 1:
        try:
            sql = "UPDATE artist SET name = '"+x3+"' WHERE name = '"+x2+"'"
            cursor.execute(sql)
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(modificar_screen, text="Modificado Correctamente ").pack()
                Button(modificar_screen, text="OK", command=delete_modificar).pack()
            else:
                Label(modificar_screen, text="No se encontro un artista con ese nombre ").pack()
                Button(modificar_screen, text="OK", command=delete_modificar).pack()
        except:
            Label(modificar_screen, text="No se pudo modificar ").pack()
            Button(modificar_screen, text="OK", command=delete_modificar).pack()
    if select2 == 2:
        try:
            sql = "UPDATE album SET title = '"+x3+"' WHERE title = '"+x2+"'"
            cursor.execute(sql)
            if cursor.rowcount >1:
                print(cursor.rowcount, "record(s) affected")
                Label(modificar_screen, text="Modificado Correctamente ").pack()
                Button(modificar_screen, text="OK", command=delete_modificar).pack()
            else:
                Label(modificar_screen, text="No se encontro un album con ese nombre ").pack()
                Button(modificar_screen, text="OK", command=delete_modificar).pack()
        except:
            Label(modificar_screen, text="No se pudo modificar ").pack()
            Button(modificar_screen, text="OK", command=delete_modificar).pack()
    if select2 == 3:
        try:
            sql = "UPDATE track SET name = '"+x3+"' WHERE name = '"+x2+"'"
            cursor.execute(sql)
            if cursor.rowcount >= 1:
                print(cursor.rowcount, "record(s) affected")
                Label(modificar_screen, text="Modificado Correctamente ").pack()
                Button(modificar_screen, text="OK", command=delete_modificar).pack()
            else:
                Label(modificar_screen, text="No se encontro una cancion con ese nombre ").pack()
                Button(modificar_screen, text="OK", command=delete_modificar).pack()
        except:
            Label(modificar_screen, text="No se pudo modificar ").pack()
            Button(modificar_screen, text="OK", command=delete_modificar).pack()

def agregar():
    global agregar1_screen
    agregar1_screen=Toplevel(login_screen)
    agregar1_screen.title("Success")
    agregar1_screen.geometry("150x100")
    x5 = entryname.get()
    x6 = entrynamealb.get()
    x7 = entrynamesong.get()
    x8 = entrymilisec.get()
    #INSERT artist
    querry = "SELECT * FROM artist WHERE artist.name = '"+x5+"'"
    postgreSQL_select_Query = querry
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    who = ""
    a = []
    for record in records:
        who = who + record[1]
        a.append(record)
        print(record[1])
        print(type(record))
    if not a:
        #Aqui se guarda en la variable varrIsa el id mas alto y se le suma uno para ser el nuevo id
        querryidartist = "SELECT MAX(artistid) FROM artist"
        postgreSQL_select_Query = querryidartist
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        varrIsa = ""
        for i in intentos:
            numcaca = str(i[0])
            varrIsa = varrIsa + numcaca
        varrIsa = int(varrIsa) + 1
        querry2 = "INSERT INTO artist(artistid, name) VALUES ('"+str(varrIsa)+"', '"+x5+"')"
        try:
            print(querry2)
            cursor.execute(querry2)
            connection.commit()
            print(cursor.rowcount,"record inserted")

        except:
            print("No se pudo crear usuario")
            Label(agregar1_screen, text="No se pudo agregar ").pack()
            Button(agregar1_screen, text="OK", command=delete_agregar).pack()
    #INSERT album
    # set a label for showing success information on screen
    querry3 = "SELECT album.title FROM album WHERE album.title ='"+x6+ "'"
    print(querry3)
    postgreSQL_select_Query = querry3
    cursor.execute(postgreSQL_select_Query)
    records2 = cursor.fetchall()
    what = ""
    b = []
    for r in records2:
        what = what + r[0]
        b.append(r)
        print(type(r))
    if not b:
        #Guardamos en una variable el id del album
        querryidalbum = "SELECT MAX(albumid) FROM album"
        postgreSQL_select_Query = querryidalbum
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        saberwho = ""
        for i in intentos:
            numcaca = str(i[0])
            saberwho = saberwho + numcaca
        saberwho = int(saberwho) + 1
        #Guardamos en una variable el id del artista
        querryidartist = "SELECT artist.artistid FROM artist WHERE artist.name = '"+x5+"'"
        postgreSQL_select_Query = querryidartist
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        varrIsa = ""
        for i in intentos:
            numcaca = str(i[0])
            varrIsa = varrIsa + numcaca
        #    print("SABERWHO:"+ saberwho)
        querry4 = "INSERT INTO album(albumid, title, artistid) VALUES ('"+str(saberwho)+"', '"+x6+"' , '"+str(varrIsa)+"')"
        try:
            print(querry4)
            cursor.execute(querry4)
            connection.commit()
            print(cursor.rowcount,"record inserted")
            Label(agregar1_screen, text="Se agrego ").pack()
            Button(agregar1_screen, text="OK", command=delete_agregar).pack()
            # set a label for showing success information on screen
        except:
            Label(agregar1_screen, text="No se pudo agregar ").pack()
            Button(agregar1_screen, text="OK", command=delete_agregar).pack()

    #INSERt track


    querry5= "SELECT track.name FROM track WHERE track.name = '"+x7+"'"
    postgreSQL_select_Query = querry5
    cursor.execute(postgreSQL_select_Query)
    records3 = cursor.fetchall()
    whow = ""
    c = []
    for re in records3:
        whow = whow + re[1]
        c.append(re)
        print(re[1])
        print(type(re))
    if not c:
        #Guardamos en una variable el id del track
        querryidalbum = "SELECT album.albumid FROM album WHERE album.title = '"+x6+"'"
        postgreSQL_select_Query = querryidalbum
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        varrIsa = ""
        for i in intentos:
            numcaca = str(i[0])
            varrIsa = varrIsa + numcaca
        querryMAX = "SELECT MAX(trackid) FROM track"
        postgreSQL_select_Query = querryMAX
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        max = ""
        for i in intentos:
            numcaca = str(i[0])
            max = max + numcaca
        max = int(max) + 1
        #print("MAX:"+ max)
        querry6 = "INSERT INTO track(trackid, name, albumid, mediatypeid, milliseconds, unitprice,useradd,activated) VALUES ('"+str(max)+"', '"+x7+"', '"+str(varrIsa)+"', '1', '"+x8+"', '0.99','"+usuario+"',1)"
        try:
            print(querry6)
            cursor.execute(querry6)
            connection.commit()
            print(cursor.rowcount,"record inserted")
            Label(agregar1_screen, text="Se agrego ").pack()
            Button(agregar1_screen, text="OK", command=delete_agregar).pack()
            # set a label for showing success information on screen
        except:
            Label(agregar1_screen, text="No se pudo agregar ").pack()
            Button(agregar1_screen, text="OK", command=delete_agregar).pack()

def activar():
    global activar_screen
    activar_screen = Toplevel(login_screen)
    activar_screen.title("Activar/Desactivar")
    activar_screen.geometry("2000x1500")
    activar_screen.configure(background = 'black')
    global var5
    global entryact


    ## CREAR IMAGEN
    load = Image.open("header.png")
    foto2 = ImageTk.PhotoImage(load)
    label2 = Label(activar_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    var5 = IntVar()
    Radiobutton(activar_screen, text="Activar    ", variable=var5, value=1,fg='white', bg='black').place(x=5, y=260)
    Radiobutton(activar_screen, text="Desactivar   ", variable=var5, value=0,fg='white' , bg='black').place(x=5, y=280)

    label3 =Label(activar_screen,text='Ingrese el nombre de la cancion que quiere activar/desactivar:')
    label3.place(x=500,y=260)
    entryact = Entry(activar_screen)
    entryact.place(x=500, y=290)

    button1 = Button(activar_screen, text="Activar/Desactivar",command =desactivacion)
    button1.place(x =1300, y= 700)

def desactivacion():
    global desactivacion_screen
    desactivacion_screen = Toplevel(login_screen)
    desactivacion_screen.title("Activacion/Desactivacion")
    desactivacion_screen.geometry("150x100")

    select2 = var5.get()
    x1 =entryact.get()

    if select2 == 1:
        try:
            sql = "SELECT track.activated FROM track WHERE track.name = '"+x1+"'"
            postgreSQL_select_Query = sql
            print(sql)
            cursor.execute(postgreSQL_select_Query)
            records = cursor.fetchall()
            variabls = ""
            for record in records:
                numero = str(record[0])
                variabls = variabls + numero
                print(type(record))
            variabls2 =int(variabls)
            print(variabls2)
            if 1 == variabls2:
                Label(desactivacion_screen, text="Ya esta activada ").pack()
                Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()
            else:
                try:
                    sql = "UPDATE track SET activated = 1 WHERE name = '"+x1+"'"
                    cursor.execute(sql)
                    if cursor.rowcount >= 1:
                        print(cursor.rowcount, "record(s) affected")
                        Label(desactivacion_screen, text="Activado Correctamente ").pack()
                        Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()
                except:
                    Label(desactivacion_screen, text="No se logro activar correctamente ").pack()
                    Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()
        except:
            print("No se encontro una cancion con este nombre")
            Label(desactivacion_screen, text="No se encontro una cancion con este nombre").pack()
            Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()

    if select2 == 0:
        try:
            sql = "SELECT track.activated FROM track WHERE track.name = '"+x1+"'"
            postgreSQL_select_Query = sql
            print(sql)
            cursor.execute(postgreSQL_select_Query)
            records = cursor.fetchall()
            variabls3 = ""
            for record in records:
                numero = str(record[0])
                variabls3 = variabls3 + numero
                print(type(record))
            variabls4 =int(variabls3)
            print(variabls4)
            if 0 == variabls4:
                Label(desactivacion_screen, text="desactivada ").pack()
                Button(desactivacion_screen, text="okay", command=delete_desactivacion).pack()
            else:
                try:
                    sql = "UPDATE track SET activated = 0 WHERE name = '"+x1+"'"
                    cursor.execute(sql)
                    if cursor.rowcount >= 1:
                        print(cursor.rowcount, "record(s) affected")
                        Label(desactivacion_screen, text="Desactivado ").pack()
                        Button(desactivacion_screen, text="okay", command=delete_desactivacion).pack()
                except:
                    Label(desactivacion_screen, text="No se logro desactivar correctamente ").pack()
                    Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()
        except:
            print("No se encontro una cancion con este nombre")
            Label(desactivacion_screen, text="No se encontro una cancion con este nombre").pack()
            Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()

# Funcion para realizar los reportes
def reportes():
    global reportes_screen
    reportes_screen = Toplevel(login_screen)
    reportes_screen.title("Reportes")
    reportes_screen.geometry("2000x1500")
    reportes_screen.configure(background = 'black')


#Primer reporte
    Label1 = Label(reportes_screen,text="Los artistas con más álbumes publicados")
    Label1.pack(anchor= 'nw')
    querry = "SELECT artist.name, COUNT(*) AS numero_de_discos FROM album INNER JOIN artist ON album.artistid = artist.artistid GROUP BY album.artistid, artist.name ORDER BY COUNT(*) DESC LIMIT 5"
    postgreSQL_select_Query = querry
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    variabls = ""
    for record in records:
        print(record[0],record[1])
        numero = str(record[1])
        variabls = variabls + record[0]+": "+numero +" albums\n"
        print(type(record))

    print(variabls)
    records1=Label(reportes_screen, text=variabls, fg = 'white', bg='black')
    records1.pack(anchor= 'nw')
    #CSV primer reporte
    Button(reportes_screen, text="Generar CSV de reporte 1", command=generate_CVS1).place(x=1150, y=575)

#Segundo reporte
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
    ##CSV REporte2
    Button(reportes_screen, text="Generar CSV de reporte 2", command=generate_CVS2).place(x=1150, y=600)

#REporte 3
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
    #CSV reporte 3
    Button(reportes_screen, text="Generar CSV de reporte 3", command=generate_CVS3).place(x=1150, y=625)

#Reporte 4
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

    #CSV reporte 4
    Button(reportes_screen, text="Generar CSV de reporte 4", command=generate_CVS4).place(x=1150, y=650)


#Reporte 5

##@ TODO
    Label5 = Label(reportes_screen,text="5. Usuarios que han registrado más canciones")
    Label5.place(x= 550, y=0)
    querry5 = "SELECT useradd AS usuario, COUNT(*) AS canciones_agregadas FROM track WHERE useradd IS NOT NULL GROUP BY usuario ORDER BY canciones_agregadas DESC"
    postgreSQL_select_Query = querry5
    cursor.execute(postgreSQL_select_Query)
    records6 = cursor.fetchall()
    coso = ""
    for record in records6:
        print(record[0],record[1])
        numero = str(record[1])
        coso = coso +record[0]+": "+numero +" canciones\n"
        print(type(record))

    print(coso)
    records5=Label(reportes_screen, text=coso, fg = 'white', bg='black')
    records5.place(x=550, y=25)
    #CSV reporte 5
    Button(reportes_screen, text="Generar CSV de reporte 5", command=generate_CVS5).place(x=1150, y=675)

#Reporte 6
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
    #CSV Reporte 6
    Button(reportes_screen, text="Generar CSV de reporte 6", command=generate_CVS6).place(x=1150, y=700)

#Reporte 7
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

    Button(reportes_screen, text="Generar CSV de reporte 7", command=generate_CVS7).place(x=1150, y=725)


#Reporte 8
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
    #CSV reporte 8
    Button(reportes_screen, text="Generar CSV de reporte 8", command=generate_CVS8).place(x=1150, y=750)

    #Boton amplicaion de reporteria fechas
    Button(reportes_screen, text="Amplicación de reporteria", command=ampliacion_reporteria).place(x=1150, y=550)

def ampliacion_reporteria():
    global ampliacion_reportes_screen
    ampliacion_reportes_screen = Toplevel(login_screen)
    ampliacion_reportes_screen.title("Ampliacion de reportes")
    ampliacion_reportes_screen.geometry("2000x1500")
    ampliacion_reportes_screen.configure(background = 'black')

    ## @TODO Hay que preguntar al usuario que fechas quiere ingresar##
    ## 1er reporte
    Label1 = Label(ampliacion_reportes_screen,text="1. Total de ventas por semana")
    Label1.pack(anchor= 'nw')
    querry9 = "@@TODO"
    postgreSQL_select_Query = querry9
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    hola = ""
    for record in records:
        print(record[0],record[1])
        numero = str(record[1])
        artista = str(record[0])
        hola = hola + record[0]+": "+numero +" albums\n"
        print(type(record))

    print(hola)
    records1=Label(ampliacion_reportes_screen, text=hola, fg = 'white', bg='black')
    records1.pack(anchor= 'nw')

    Button(ampliacion_reportes_screen, text="Generar CSV de reporte 1", command=generate_CVS1).place(x=1150, y=600)





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

        variabls = ""
        for record in records:
            print(record[0],record[1])
            variabls = variabls + record[0]+": "+record[1]+"\n"
            print(type(record))

        print(variabls)
        records1=Label(login_success_screen, text=variabls, fg = 'white', bg='black')
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

        variabls = ""
        for record in records:
            print(record[0],record[1],record[2])
            variabls = variabls + record[0]+": "+record[1]+" "+record[2]+"\n"
            print(type(record))

        print(variabls)
        records1=Label(login_success_screen, text=variabls, fg = 'white', bg='black')
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

        variabls = ""
        for record in records:
            print(record[0],record[1])
            variabls = variabls + record[0]+": "+record[1]+"\n"
            print(type(record))

        print(variabls)
        records1=Label(login_success_screen, text=variabls, fg = 'white', bg='black')
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

        variabls = ""
        for record in records:
            print(record[0],record[1])
            variabls = variabls + record[0]+": "+record[1]+"\n"
            print(type(record))

        print(variabls)
        records1=Label(login_success_screen, text=variabls, fg = 'white', bg='black')
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


def delete_modificar():
    modificar_screen.destroy()

def delete_quitar():
    quitar_screen.destroy()

def delete_desactivacion():
    desactivacion_screen.destroy()

def delete_agregar():
    agregar1_screen.destroy()

def generate_CVS1():
    querry = "SELECT artist.name, COUNT(*) AS numero_de_discos FROM album INNER JOIN artist ON album.artistid = artist.artistid GROUP BY album.artistid, artist.name ORDER BY COUNT(*) DESC LIMIT 5"
    postgreSQL_select_Query = querry
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    reporte1 = open('artista_mas_albums_publicados','w')
    with reporte1:
        myFields = ['Artist_name','count']
        writer = csv.DictWriter(reporte1,fieldnames=myFields)
        writer.writeheader()
        for record in records:
            numero = str(record[1])
            artista = str(record[0])
            writer.writerow({'Artist_name': artista,'count':numero})

def generate_CVS2():
    querry2 = "SELECT genre.name, COUNT(*) AS numero_de_canciones FROM track INNER JOIN genre ON genre.genreid = track.genreid GROUP BY genre.name ORDER BY numero_de_canciones DESC LIMIT 5"
    postgreSQL_select_Query = querry2
    cursor.execute(postgreSQL_select_Query)
    records2 = cursor.fetchall()
    reporte2 = open('generos_mas_canciones','w')
    with reporte2:
        fields2 = ['genre','count']
        writer = csv.DictWriter(reporte2,fieldnames=fields2)
        writer.writeheader()
        for record in records2:
            numero = str(record[1])
            genero = str(record[0])
            writer.writerow({'genre': genero,'count':numero})


def generate_CVS3():
    querry3 ="SELECT playlist.name, SUM(track.milliseconds/60000) AS duracion_minutos FROM track INNER JOIN playlisttrack ON playlisttrack.trackid = track.trackid INNER JOIN playlist ON playlisttrack.playlistid = playlist.playlistid GROUP BY playlist.name ORDER BY duracion_minutos DESC"
    postgreSQL_select_Query = querry3
    cursor.execute(postgreSQL_select_Query)
    records3 = cursor.fetchall()
    reporte3 = open('duracion_playlist','w')
    with reporte3:
        fields3 = ['Playlist','duracion']
        writer = csv.DictWriter(reporte3,fieldnames=fields3)
        writer.writeheader()
        for record in records3:
            numero = str(record[1])
            playlist = str(record[0])
            writer.writerow({'Playlist': playlist,'duracion':numero})

def generate_CVS4():
    querry4= "SELECT track.name, artist.name, track.milliseconds/60000 AS duracion_minutos FROM track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid ORDER BY duracion_minutos DESC LIMIT 5"
    postgreSQL_select_Query = querry4
    cursor.execute(postgreSQL_select_Query)
    records4 = cursor.fetchall()
    reporte4 = open('canciones_mas_duracion_info_artista','w')
    with reporte4:
        fields4 = ['Cancion','Artista','Duracion']
        writer = csv.DictWriter(reporte4,fieldnames=fields4)
        writer.writeheader()
        for record in records4:
            numero = str(record[2])
            nombre_cancion = str(record[0])
            nombre_artista = str(record[1])
            writer.writerow({'Cancion': nombre_cancion,'Artista':nombre_artista,'Duracion': numero})

def generate_CVS5():
    querry5 = "SELECT useradd AS usuario, COUNT(*) AS canciones_agregadas FROM track WHERE useradd IS NOT NULL GROUP BY usuario ORDER BY canciones_agregadas DESC"
    postgreSQL_select_Query = querry5
    cursor.execute(postgreSQL_select_Query)
    records6 = cursor.fetchall()
    reporte5 = open('Canciones_agg_por_usuarios','w')
    with reporte5:
        fields5 = ['Usuario','Canciones_agg']
        writer = csv.DictWriter(reporte5,fieldnames=fields5)
        writer.writeheader()
        for record in records6:
            user = str(record[0])
            numero = str(record[1])
            writer.writerow({'Usuario': user,'Canciones_agg':numero})

def generate_CVS6():
    querry6 = "SELECT genre.name, AVG(track.milliseconds/60000) AS promedio_duracion_minutos FROM track INNER JOIN genre ON genre.genreid = track.genreid GROUP BY genre.name ORDER BY promedio_duracion_minutos DESC"
    postgreSQL_select_Query = querry6
    cursor.execute(postgreSQL_select_Query)
    records6 = cursor.fetchall()
    reporte6 = open('Duracion_promedio_genero','w')
    with reporte6:
        fields6 = ['Genre','promedio_min']
        writer = csv.DictWriter(reporte6,fieldnames=fields6)
        writer.writeheader()
        for record in records6:
            genre = str(record[0])
            numero = str(record[1])
            writer.writerow({'Genre': genre,'promedio_min':numero})

def generate_CVS7():
    querry7 = "SELECT playlist.name, COUNT(DISTINCT artist.name) AS numero_artistas FROM track INNER JOIN album ON track.albumid=album.albumid INNER JOIN artist ON artist.artistid = album.artistid INNER JOIN playlisttrack ON playlisttrack.trackid = track.trackid INNER JOIN playlist ON playlist.playlistid = playlisttrack.playlistid GROUP BY playlist.name ORDER BY numero_artistas DESC"
    postgreSQL_select_Query = querry7
    cursor.execute(postgreSQL_select_Query)
    records7 = cursor.fetchall()
    reporte7 = open('artistas_por_playlist','w')
    with reporte7:
        fields7 = ['playlist','numero_artistas']
        writer = csv.DictWriter(reporte7,fieldnames=fields7)
        writer.writeheader()
        for record in records7:
            playlist = str(record[0])
            numero = str(record[1])
            writer.writerow({'playlist': playlist,'numero_artistas':numero})


def generate_CVS8():
    querry8 ="SELECT artist.name, COUNT(DISTINCT genre.name) AS numero_generos FROM track JOIN album ON album.albumid = track.albumid JOIN artist ON album.artistid = artist.artistid JOIN genre ON track.genreid = genre.genreid GROUP BY artist.name ORDER BY numero_generos DESC LIMIT 5"
    postgreSQL_select_Query = querry8
    cursor.execute(postgreSQL_select_Query)
    records8 = cursor.fetchall()
    reporte8 = open('artistas_diversidad','w')
    with reporte8:
        fields8 = ['artista','cantidad']
        writer = csv.DictWriter(reporte8,fieldnames=fields8)
        writer.writeheader()
        for record in records8:
            artista = str(record[0])
            numero = str(record[1])
            writer.writerow({'artista': artista,'cantidad':numero})



main_account_screen() # call the main_account_screen() function
