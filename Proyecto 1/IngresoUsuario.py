## https://www.simplifiedpython.net/python-gui-login/ codigo de referencia
## Estuardo Ureta
## Isabel Ortiz Naranjo
import csv
import random
from tkinter import *
from tkinter import ttk
import itertools
import psycopg2
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkcalendar import *


## codigo para el login tomado de https://www.simplifiedpython.net/python-gui-login/

def main_account_screen():

    global main_screen
    main_screen = Tk()   # create a GUI window
    main_screen.geometry("2000x1500") # set the configuration of GUI window
    main_screen.title("Account Login") # set the title of GUI window
    main_screen.configure(background = 'black')

    ## CREAR IMAGEN
    foto = PhotoImage(file = "header.png")
    label2 = Label(main_screen, image = foto)
    label2.place(x=90, y =0)

    # create a Form label
    Label(text="Login Or Register", bg="blue", width="160", height="2", fg='white',font=("Calibri", 13)).place(y=260)

    # create Login Button
    Button(text="Login", height="4", width="60",highlightbackground='magenta', fg='black',command = login).place(x=460, y=400)

    # create a register button
    Button(text="Register", height="4", width="60", fg= 'black',highlightbackground='magenta', command = register).place(x=460,y=600)

    global cursor
    global connection
    ## Connecion a base de datos
    ## intercambiable
    try:
        connection = psycopg2.connect(user = "postgres",
                                      password = "Pancho14",
                                      host = "localhost",
                                      port = "5432",
                                      database = "ProyectoBD")

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
    foto2 = PhotoImage(file = "header.png")
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

    Radiobutton(register_screen, text="Admin", variable=var2, value=1,fg='navy', bg='black').place(x=900, y=400)
    Radiobutton(register_screen, text="Normal", variable=var2, value=0,fg='navy', bg='black').place(x=900, y=420)

    # Set register button
    Button(register_screen, text="Register", width=10, height=2, bg="blue", command =register_user).place(x=675,y=470)


def register_user():

    # get username and password
    username_info = username.get()
    password_info = password.get()
    select1 = var2.get()
    admin = 0
    if select1 == 0:
        admin = 0
    if select1 == 1:
        admin = 1


    #agregar un usario a la base de datos
    querry_customer_id = "select customerid from customer order by customerid desc limit 1"
    print(querry_customer_id)
    cursor.execute(querry_customer_id)
    customer_ids = cursor.fetchall()
    ultimoid = 0
    for id in customer_ids:
        ultimoid = id[0]
    ultimoid = ultimoid + 1
    ids = str(ultimoid)
    querry_insertCustomer ="INSERT INTO Customer (CustomerId, FirstName, LastName,  Email) VALUES ("+ids+",'"+username_info+"','A','A.@')"
    print(querry_insertCustomer)


    sql = "INSERT INTO usuario (username, password, isAdmin) VALUES (%s, %s, %s)"
    val = (username_info,password_info,admin)
    try:
        print("LOBOS")
        cursor.execute(sql,val)
        connection.commit()
        print(cursor.rowcount,"record inserted")
        cursor.execute(querry_insertCustomer)
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
        print ("entro")
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
                print("entro X2")
                usuario = username1
                borrar_carrito = "delete from carrito"
                cursor.execute(borrar_carrito)
                connection.commit()
                login_sucess()
            else:
                password_not_recognised()
    else:
        user_not_found()


def login_sucess():
    global login_success_screen   # make login_success_screen global
    login_success_screen = Toplevel(login_screen)


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
    Radiobutton(login_success_screen, text="Artist    ", variable=var, value=1,fg='navy', bg='black').place(x=5, y=260)
    Radiobutton(login_success_screen, text="Genre   ", variable=var, value=2,fg='navy' , bg='black').place(x=5, y=280)
    Radiobutton(login_success_screen, text="Canción", variable=var, value=3,fg='navy', bg='black').place(x=5, y=300)
    Radiobutton(login_success_screen, text="Album   ", variable=var, value=5,fg='navy', bg='black').place(x=5, y=320)

    Buttonagregar = Button(login_success_screen,text='Agregar una nueva cancion,album o artista',width="30", height="1",command = agregarcancion).place(x=5,y=540)
    Butoonquitar = Button(login_success_screen,text="Quitar una cancion,album o artista",width="30", height="1", command = quitarcancion).place(x=5,y=565)
    Buttoneditar = Button(login_success_screen,text="Editar una cancion,album o artista",width="30", height="1", command= editarcancion).place(x=5,y=590)
    Buttonactivar = Button(login_success_screen,text="Activar o inactivar una cancion",width="30", height="1", command= activar).place(x=5,y=615)
    Bottondebitacora = Button(login_success_screen, text= "Bitacora",width="30", height="1", command = debitacora).place(x=5,y=640)
    Bottondesimulaciones = Button(login_success_screen, text= "Simulaciones",width="30", height="1", command = simulaciones).place(x=5,y=665)
    BotonCompra = Button(login_success_screen,text = "Compra", width ='30', height = '1', command = compras).place(x=5,y=690)
    Bottonmongo = Button(login_success_screen, text= "Mongodb",width="30", height="1", command = mongoloco).place(x=5,y=715)


def compras():
    global compras_screen
    compras_screen = Toplevel(login_screen)
    compras_screen.title("Compras")
    compras_screen.geometry("2000x1500")
    compras_screen.configure(background = 'black')

    foto2 = PhotoImage(file = "header.png")
    label2 = Label(compras_screen, image = foto2)

    label2.image =foto2
    label2.place(x=90, y =0)

    global entry2
    entry2 = Entry(compras_screen)
    entry2.place(x=250, y= 260)

    button1 = Button(compras_screen, text="Search", command = buscarmus)
    button1.place(x =250, y= 290)
    global var3
    var3 = IntVar()

    Radiobutton(compras_screen, text="Buscar por el artista", variable=var3, value=1,fg='navy', bg='black').place(x=5, y=260)
    Radiobutton(compras_screen, text="Buscar por el nombre de la cancion", variable=var3, value=2,fg='navy' , bg='black').place(x=5, y=280)

    BottonCarrito = Button(compras_screen,text='Agregar a carrito', command = add_cart).place(x=1200,y=670)
    BottonCheckout =Button(compras_screen,text= "Ir a checkout", command = checkout).place(x=1200,y=700)

def checkout():
    global checkout_screen
    global treecheck
    global totalcompra
    checkout_screen = Toplevel(login_screen)
    checkout_screen.title("Compras")
    checkout_screen.geometry("2000x1500")
    checkout_screen.configure(background = 'black')

    foto2 = PhotoImage(file = "header.png")
    label2 = Label(checkout_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    treecheck = ttk.Treeview(checkout_screen, selectmode ='browse')
    treecheck["columns"]=("Track", 'Artist','Precio','Usuario',"ID")

    treecheck.column("#0", width = 0)
    treecheck.column("Track", width = 300)
    treecheck.heading("Track",text="Track" )
    treecheck.column("Artist", width = 300)
    treecheck.heading("Artist",text="Artist")
    treecheck.column("Precio", width = 300)
    treecheck.heading("Precio",text="Precio")
    treecheck.column("Usuario", width = 300)
    treecheck.heading("Usuario",text="Usuario")
    treecheck.column("ID", width = 100)
    treecheck.heading("ID",text="ID")

    querrycarro = "Select * from carrito"
    postgreSQL_select_Query = querrycarro
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    totalcompra = 0
    for record in records:
        treecheck.insert("", END, text="", values=(record[0],record[1],record[2],record[3],record[4]))
        subtotal = float(record[2])
        print(str(subtotal))
        totalcompra = totalcompra + subtotal


    print(str(totalcompra))

    treecheck.place(x=50, y = 300)


    treecheck.bind('<<TreeviewSelect>>',delete_selected)

    label_total = Label(checkout_screen,text= "Total de compra:"+str(totalcompra)+"").place(x=800,y=550)

    buttonborrar = Button(checkout_screen, text = "Borrar el track seleccionado", command = borrarlo).place(x=1100,y=600)

    buttoncompras = Button(checkout_screen,text= "Seguir con la compra", command = continuacion_compra).place(x=1100, y=630)

    botonrefresh = Button(checkout_screen, text = "Refresh Screen", command = refresh).place(x=1100,y=660)

def continuacion_compra():
    rata = False
    def grouper(iterable, n):
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args)

    def export_to_pdf(data):
        c = canvas.Canvas("recibo-compra.pdf", pagesize=A4)
        c.drawImage("header.PNG", 120, 700,width=350, height=100)
        c.line(50, 680, 530, 680)
        c.drawString(50, 640, "DETALLE DE COMPRA")
        c.drawString(50, 625, "Cliente: "+usuario+"")
        w, h = A4
        max_rows_per_page = 45
        # Margin.
        x_offset = 50
        y_offset = 225
        # Space between rows.
        padding = 15

        xlist = [x + x_offset for x in [0, 150, 300, 400, 480,]]
        ylist = [h - y_offset - i*padding for i in range(max_rows_per_page + 1)]

        for rows in grouper(data, max_rows_per_page):
            rows = tuple(filter(bool, rows))
            c.grid(xlist, ylist[:len(rows) + 1])
            for y, row in zip(ylist[:-1], rows):
                for x, cell in zip(xlist, row):
                    c.drawString(x + 2, y - padding + 3, str(cell))
            c.showPage()

        c.save()
    data = [("Cancion", "Artista", "Precio", "Estado")]

    querrycarro = "Select * from carrito"
    postgreSQL_select_Query = querrycarro
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    contador = 0
    for record in records:
        contador = contador + 1

    querrycustomerid = "select customerid from customer where firstname='"+usuario+"'"
    cursor.execute(querrycustomerid)
    custumero = cursor.fetchall()
    id_este = 0
    for cus in custumero:
        id_este= cus[0]
    idlol = str(id_este)
    print(idlol)
    querryinvoice_id = "select invoiceid from invoice order by invoiceid desc limit 1"
    cursor.execute(querryinvoice_id)
    invoices_id = cursor.fetchall()
    for o in invoices_id:
        ultimo_invoice_id = o[0]
    ultimo_invoice_id = ultimo_invoice_id + 1
    querry_insert_invoice = "INSERT INTO Invoice (InvoiceId, CustomerId, InvoiceDate, Total) VALUES ("+str(ultimo_invoice_id)+","+idlol+", NOW(), "+str(totalcompra)+")"
    print(querry_insert_invoice)
    cursor.execute(querry_insert_invoice)
    connection.commit()
    print(cursor.rowcount,"record inserted")
    if cursor.rowcount >= 1:
        print("SE LOGRO JEJE")


    for record in records:
        artistak = record[1]
        trackk = record[0]
        preciok=str(record[2])
        usuariok = record[3]
        idtrack = str(record[4])
        state= "Vendida"
        data.append((trackk, artistak,preciok, state))
        querryinvoice_line = "select invoicelineid from invoiceline order by invoicelineid desc limit 1"
        cursor.execute(querryinvoice_line)
        invoice_line_id = cursor.fetchall()
        for w in invoice_line_id:
            ultimo_invoice_line = w[0]
        ultimo_invoice_line = ultimo_invoice_line + 1
        querrycarrito = "insert into invoiceline(invoicelineid,invoiceid,trackid,unitprice,quantity) values ("+str(ultimo_invoice_line)+","+str(ultimo_invoice_id)+","+idtrack+","+preciok+",1)"
        print(querrycarrito)
        cursor.execute(querrycarrito)
        connection.commit()
        print(cursor.rowcount,"record inserted")
        if cursor.rowcount >= 1:
            rata = True
            print("SE LOGRO WOW")

    if rata == True:
        export_to_pdf(data)
        agregadoinvoice_invoiceline()


def agregadoinvoice_invoiceline():
    global agregado_inscreen
    agregado_inscreen = Toplevel(login_screen)
    agregado_inscreen.title("Success")
    agregado_inscreen.geometry("500x100")
    Label(agregado_inscreen, text="Se creo una confirmacion de su compra en pdf exitosamente ").pack()

    borrar_carrito = "delete from carrito"
    cursor.execute(borrar_carrito)
    connection.commit()

    Button(agregado_inscreen, text="OK", command=delete_invoiceconfirm).pack()



def delete_invoiceconfirm():
    agregado_inscreen.destroy()




def refresh():
    checkout_screen.destroy()
    checkout()


def delete_selected(event):
    global seleccionado
    global preciocancion2
    global nombrecancion2
    global nombreartista2
    seleccionado = treecheck.selection()
    for i in seleccionado:
        nombreartista2 = treecheck.item(i)['values'][1]
        nombrecancion2= treecheck.item(i)['values'][0]
        preciocancion2 = treecheck.item(i)['values'][2]

def borrarlo():
    querrydelete = "DELETE FROM carrito WHERE track = '"+nombrecancion2+"'"
    print(querrydelete)
    cursor.execute(querrydelete)
    connection.commit()
    print(cursor.rowcount,"record deleted")
    if cursor.rowcount >= 1:
        borradocarrito()


def borradocarrito():
    global borrado_screen
    borrado_screen = Toplevel(login_screen)
    borrado_screen.title("Success")
    borrado_screen.geometry("150x100")
    Label(borrado_screen, text="Se borro ").pack()
    Button(borrado_screen, text="OK", command=delete_carrito).pack()




def buscarmus():
    global compras_screen
    global treebus
    select = var3.get()
    x1 = entry2.get()
    x2 = 'artist.name, track.name, track.unitprice, track.trackid'
    whereclause = ''
    if select == 1:
        selection = 'track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        whereclause = "artist.name='"+x1+"'"
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+"AND track.activated = 1"
        querry =str(querry)
        print(querry)
        postgreSQL_select_Query = querry
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()
        treebus = ttk.Treeview(compras_screen, selectmode ='browse')
        treebus["columns"]=("Artist Name", 'Track Name','Precio','ID')
        treebus.column("#0", width = 0)
        treebus.column("Artist Name", width = 300)
        treebus.heading("Artist Name",text="Artist Name" )
        treebus.column("Track Name", width = 300)
        treebus.heading("Track Name", text = 'Track Name')
        treebus.column('Precio',width =100)
        treebus.heading('Precio',text= 'Precio')
        treebus.column('ID',width =100)
        treebus.heading('ID',text= 'ID')
        for record in records:
            treebus.insert("", END, text="", values=(record[0],record[1],record[2],record[3]))

        treebus.place(x=500, y = 300)

        treebus.bind('<<TreeviewSelect>>',callback)

    if select == 2:
        selection = 'track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        whereclause = "track.name='"+x1+ "'"
        x2= 'artist.name, track.name, track.unitprice, track.trackid'
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+"AND track.activated = 1"
        querry =str(querry)
        print(querry)
        postgreSQL_select_Query = querry
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()
        treebus = ttk.Treeview(compras_screen, selectmode ='browse')
        treebus["columns"]=("Artist Name", 'Track Name','Precio','ID')
        treebus.column("#0", width = 0)
        treebus.column("Artist Name", width = 300)
        treebus.heading("Artist Name",text="Artist Name" )
        treebus.column("Track Name", width = 300)
        treebus.heading("Track Name", text = 'Track Name')
        treebus.column('Precio',width =100)
        treebus.heading('Precio',text= 'Precio')
        treebus.column('ID',width =100)
        treebus.heading('ID',text= 'ID')

        for record in records:
            treebus.insert("", END, text="", values=(record[0],record[1],record[2],record[3]))

        treebus.place(x=500, y = 300)

        treebus.bind('<<TreeviewSelect>>',callback)


def callback(event):
    global selected
    global preciocancion
    global nombrecancion
    global nombreartista
    global idcancion

    selected = treebus.selection()
    for i in selected:
        nombreartista = treebus.item(i)['values'][0]
        nombrecancion= treebus.item(i)['values'][1]
        preciocancion = treebus.item(i)['values'][2]
        idcancion= str(treebus.item(i)['values'][3])

        print(nombrecancion)

def add_cart():##insert en carrito
    querrycarrito = "insert into carrito(track,artist,precio,usuario,trackid) values ('"+nombrecancion+"','"+nombreartista+"',"+preciocancion+",'"+usuario+"',"+idcancion+")"
    print(querrycarrito)
    cursor.execute(querrycarrito)
    connection.commit()
    print(cursor.rowcount,"record inserted")
    if cursor.rowcount >= 1:
        agregadocarrito()

def agregadocarrito():
    global agregado_screen
    agregado_screen = Toplevel(login_screen)
    agregado_screen.title("Success")
    agregado_screen.geometry("150x100")
    Label(agregado_screen, text="Se agrego ").pack()
    Button(agregado_screen, text="OK", command=delete_compras).pack()


def simulaciones():
    global simulacion_screen
    global cal1
    global cantidad_de_sim
    simulacion_screen = Toplevel(login_screen)
    simulacion_screen.title("Simulacion")
    simulacion_screen.geometry("2000x1500")
    simulacion_screen.configure(background = 'black')

    foto2 = PhotoImage(file = "header.png")
    label2 = Label(simulacion_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)


    label3 =Label(simulacion_screen,text='Ingrese la fecha que para la que desea ver las compras:')
    label3.place(x=550,y=270)

    style = ttk.Style(simulacion_screen)
    style.theme_use('clam')
    cal1 = Calendar(simulacion_screen,selectmode='day',background="black", disabledbackground="black", bordercolor="black",
                    headersbackground="black", normalbackground="black", foreground='white',
                    normalforeground='white', headersforeground='white')
    cal1.config(background = 'black')
    cal1.place(x=600, y= 300)

    bottonclick = Button(simulacion_screen, text='Hacer la simulacion...',command = calval1)
    bottonclick.place(x=650, y=750)


    labelcantidad = Label(simulacion_screen, text="Ingrese la cantidad de compras simuladas que quiere hacer:").place(x=570,y=500)
    cantidad_de_sim = Entry(simulacion_screen)
    cantidad_de_sim.place(x=625, y=530)



def calval1():
    fecha_sel = cal1.get_date()
    cantidad_jiji = cantidad_de_sim.get()
    cantidadjo = int(cantidad_jiji)

    ##encontrar el max id de track
    idmax='SELECT trackid from track ORDER BY trackid DESC LIMIT 1' #este va en range
    postgreSQL_select_Query = idmax
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    id = 0
    for record in records:
        id =int(record[0])

    ##encontrar el max id de customer
    idmaxcus='SELECT customerid from customer ORDER BY customerid DESC LIMIT 1' #este va en range
    cursor.execute(idmaxcus)
    records2 = cursor.fetchall()
    idcus = 0
    for record in records2:
        idcus =int(record[0])

    ## hacer algo con esta fecha buscar ventas o generar idk
    Label(simulacion_screen, text="Reproducciones").place(x=180,y=470)
    Label(simulacion_screen, text="Ventas").place(x=1150,y=470)

    tree = ttk.Treeview(simulacion_screen, selectmode ='browse')
    tree["columns"]=("Fecha", 'CustomerID','SongID','Cantidad de Rep')
    tree.column("#0", width = 0)
    tree.column("Fecha", width = 80)
    tree.heading("Fecha",text="Fecha" )
    tree.column("CustomerID", width = 80)
    tree.heading("CustomerID",text="CustomerID" )
    tree.column("SongID", width = 80)
    tree.heading("SongID",text="SongID" )
    tree.column("Cantidad de Rep", width = 80)
    tree.heading("Cantidad de Rep",text="Cantidad de Rep" )

    tree2 = ttk.Treeview(simulacion_screen, selectmode ='browse')
    tree2["columns"]=("Fecha", 'CustomerName',"TrackName",'Cantidad de Ventas','Total de Ventas')
    tree2.column("#0", width = 0)
    tree2.column("Fecha", width = 80)
    tree2.heading("Fecha",text="Fecha" )
    tree2.column("CustomerName", width = 80)
    tree2.heading("CustomerName",text="CustomerName" )
    tree2.column("TrackName", width = 80)
    tree2.heading("TrackName",text="TrackName" )
    tree2.column("Cantidad de Ventas", width = 50)
    tree2.heading("Cantidad de Ventas",text="Cantidad" )
    tree2.column("Total de Ventas", width = 120)
    tree2.heading("Total de Ventas",text="Total de Ventas" )


    for x in range(cantidadjo):
        track= str(random.randint(1,id))
        print('el track id es: ',track)
        buscar_rola="SELECT name,unitprice,trackid FROM track WHERE trackid= "+track+""
        postgreSQL_select_Query = buscar_rola
        cursor.execute(postgreSQL_select_Query)
        recordsu = cursor.fetchall()
        customer= str(random.randint(1,idcus))
        print('customer id: ',customer)
        buscar_cliente="SELECT firstname,customerid FROM customer WHERE customerid="+customer+""
        postgreSQL_select_Query = buscar_cliente
        cursor.execute(postgreSQL_select_Query)
        recordscliente = cursor.fetchall()
        for i in recordsu:
            print(i[0])
            for k in recordscliente:
                print(k[0],k[1])
                tree2.insert("", END, text="", values=(fecha_sel,k[0],i[0],1,i[1]))

                querryinvoice_id = "select invoiceid from invoice order by invoiceid desc limit 1"
                cursor.execute(querryinvoice_id)
                invoices_id = cursor.fetchall()
                for o in invoices_id:
                    ultimo_invoice_id = o[0]
                    ultimo_invoice_id = ultimo_invoice_id + 1
                    querry_insert_invoice = "INSERT INTO Invoice (InvoiceId, CustomerId, InvoiceDate, Total) VALUES ("+str(ultimo_invoice_id)+","+str(k[1])+", '"+fecha_sel+"', "+str(i[1])+")"
                    print(querry_insert_invoice)
                    cursor.execute(querry_insert_invoice)
                    connection.commit()
                    print(cursor.rowcount,"record inserted")
                    if cursor.rowcount >= 1:
                        print("SE LOGRO JEJE")

                querryinvoice_line = "select invoicelineid from invoiceline order by invoicelineid desc limit 1"
                cursor.execute(querryinvoice_line)
                invoice_line_id = cursor.fetchall()
                for w in invoice_line_id:
                    ultimo_invoice_line = w[0]
                    ultimo_invoice_line = ultimo_invoice_line + 1
                    querrycarrito = "insert into invoiceline(invoicelineid,invoiceid,trackid,unitprice,quantity) values ("+str(ultimo_invoice_line)+","+str(ultimo_invoice_id)+","+str(i[2])+","+str(i[1])+",1)"
                    print(querrycarrito)
                    cursor.execute(querrycarrito)
                    connection.commit()
                    print(cursor.rowcount,"record inserted")
                    if cursor.rowcount >= 1:
                        print("SE LOGRO WOW")

    for x in range(cantidadjo):
        ##hacer simulacion de reproducciones
        max_invoice_id = "select invoiceid from invoice order by invoiceid desc limit 1"
        cursor.execute(max_invoice_id)
        max_invoices_id = cursor.fetchall()
        maximoid = 0
        for i in max_invoices_id:
            maximoid = i[0]
        #random para tracks
        random_sock= str(random.randint(1,maximoid))
        info_rep = "select trackid,invoicelineid,customerid from invoiceline JOIN invoice ON invoiceline.invoiceid=invoice.invoiceid where invoiceline.invoiceid="+random_sock+" limit 1"
        cursor.execute(info_rep)
        random_tracks = cursor.fetchall()
        for m in random_tracks:
            random_reps= str(random.randint(1,400))
            tree.insert("", END, text="", values=(fecha_sel,str(m[2]),str(m[0]),random_reps))
            query_insert_rep = "INSERT INTO reproducciones (fecha ,customerid ,songid ,cant_rep )values('"+fecha_sel+"',"+str(m[2])+","+str(m[0])+","+str(random_reps)+")"
            print(query_insert_rep)
            cursor.execute(query_insert_rep)
            connection.commit()
            print(cursor.rowcount,"record inserted")
            if cursor.rowcount >= 1:
                print("SE LOGRO WOW")



    ## Insertar valores  a el tree de alguna manera aqui

    tree.place(x=65, y=500)
    tree2.place(x=1000,y=500)



def debitacora():
    bitacora_screen = Toplevel(login_screen)
    bitacora_screen.title("Bitacora")
    bitacora_screen.geometry("2000x1500")
    bitacora_screen.configure(background = 'black')

    foto2 = PhotoImage(file = "header.png")
    label2 = Label(bitacora_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)


    querrybit = "SELECT * FROM bitacora"
    postgreSQL_select_Query = querrybit
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()

    tree = ttk.Treeview(bitacora_screen, selectmode ='browse')
    tree["columns"]=("Username","Fecha","Tipo",'Accion','NombreActual','NombreViejo','GenreOriginal','GenreNuevo','DuracionVieja','DuracionActual','PrecioAntes','PrecioActual','AlbumIDActual','AlbumIDViejo')
    tree.column("#0", width = 0)
    tree.column("Username", width = 60)
    tree.heading("Username",text="Username" )
    tree.heading("Fecha", text="Fecha")
    tree.column("Fecha", width = 90)
    tree.heading("Tipo", text="Tipo")
    tree.column("Tipo", width = 60)
    tree.heading("Accion", text="Accion")
    tree.column("Accion", width = 80)
    tree.heading("NombreActual", text="NombreActual")
    tree.column("NombreActual", width = 100)
    tree.heading('NombreViejo', text='NombreViejo')
    tree.column("NombreViejo", width = 100)
    tree.heading('GenreOriginal', text='GenreOriginal')
    tree.column("GenreOriginal", width = 100)
    tree.heading('GenreNuevo', text='GenreNuevo')
    tree.column('GenreNuevo', width = 100)
    tree.heading('DuracionVieja', text='DuracionVieja')
    tree.column('DuracionVieja', width = 100)
    tree.heading('DuracionActual', text='DuracionActual')
    tree.column('DuracionActual', width = 100)
    tree.heading('PrecioAntes', text='PrecioAntes')
    tree.column('PrecioAntes', width = 100)
    tree.heading('PrecioActual', text='PrecioActual')
    tree.column('PrecioActual', width = 100)
    tree.heading('AlbumIDActual', text='AlbumIDActual')
    tree.column('AlbumIDActual', width = 100)
    tree.heading('AlbumIDViejo', text='AlbumIDViejo')
    tree.column('AlbumIDViejo', width = 100)





    for record in records:
        date = str(record[1])
        print(record)
        tree.insert("", END, text="", values=(record[0],date,record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11],record[12],record[12],record[13]))



    ##labelbit =Label(bitacora_screen,text=b + "").place(x=500,y=300)
    tree.place(x=65, y=270)

##Estuardo
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



##fecha_sel = cal1.get_date()


def agregarcancion():
    agregar_screen = Toplevel(login_screen)
    agregar_screen.title("Agregar")
    agregar_screen.geometry("2000x1500")
    agregar_screen.configure(background = 'black')
    global var6
    global entryname
    global entrynamealb
    global entrynamesong
    global entrymilisec
    var6 = IntVar()

    #CREAR IMAGEN
    foto2 = PhotoImage(file = "header.png")
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
        #Aqui se guarda en la variable saberwhat el id mas alto y se le suma uno para ser el nuevo id
        querryidartist = "SELECT MAX(artistid) FROM artist"
        postgreSQL_select_Query = querryidartist
        cursor.execute(postgreSQL_select_Query)
        intentos = cursor.fetchall()
        saberwhat = ""
        for i in intentos:
            numcaca = str(i[0])
            saberwhat = saberwhat + numcaca
        saberwhat = int(saberwhat) + 1
        #print("SABERWHAT:"+ str(saberwhat))
        querry2 = "INSERT INTO artist(artistid, name,user_edit) VALUES ('"+str(saberwhat)+"', '"+x5+"','"+usuario+"')"
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
    querry3 = "SELECT album.title FROM album WHERE album.title ='"+x6+"'"
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
        saberwhat = ""
        for i in intentos:
            numcaca = str(i[0])
            saberwhat = saberwhat + numcaca
        #    print("SABERWHO:"+ saberwho)
        #querry4= "INSERT INTO album(albumid, title, artistid) VALUES ('"+str(saberwho)+"', '"+x6+"' , '"+str(saberwhat)+"')"

        querry4 = "INSERT INTO album(albumid, title, artistid,user_edit) VALUES ('"+str(saberwho)+"', '"+x6+"' , '"+str(saberwhat)+"', '"+usuario+"')"
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
        saberwhat = ""
        for i in intentos:
            numcaca = str(i[0])
            saberwhat = saberwhat + numcaca
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
        querry6 = "INSERT INTO track(trackid, name, albumid, mediatypeid, milliseconds, unitprice,useradd ,activated, genreid) VALUES ('"+str(max)+"', '"+x7+"', '"+str(saberwhat)+"', '1', '"+x8+"', '0.99','"+usuario+"',1,1)"
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



def quitarcancion():
    quitar_screen = Toplevel(login_screen)
    quitar_screen.title("Quitar")
    quitar_screen.geometry("2000x1500")
    quitar_screen.configure(background = 'black')
    global var4
    global entryquit

    #CREAR IMAGEN
    foto2 = PhotoImage(file = "header.png")
    label2 = Label(quitar_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    var4 = IntVar()
    Radiobutton(quitar_screen, text="Artist    ", variable=var4, value=1,fg='navy', bg='black').place(x=5, y=260)
    Radiobutton(quitar_screen, text="Album   ", variable=var4, value=2,fg='navy' , bg='black').place(x=5, y=280)
    Radiobutton(quitar_screen, text="Canción", variable=var4, value=3,fg='navy', bg='black').place(x=5, y=300)

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
            up = "UPDATE artist SET name = '"+saberwho+"', user_edit='"+usuario+"' WHERE name = '"+saberwho+"'"
            rati = "DELETE FROM artist WHERE artistid = '"+saberwho+"'"
            print(rati)
            cursor.execute(up)
            connection.commit()
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
            up= "UPDATE album SET title = '"+x5+"', user_edit='"+usuario+"' WHERE title = '"+x5+"'"
            k = "DELETE FROM album WHERE album.title = '"+x5+"'"
            print(k)
            cursor.execute(up)
            connection.commit()
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
            up="UPDATE track SET name = '"+x5+"', user_edit='"+usuario+"' WHERE name = '"+x5+"'"
            vo ="DELETE FROM track WHERE name = '"+x5+"'"
            print(vo)
            cursor.execute(up)
            connection.commit()
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
    foto2 = PhotoImage(file = "header.png")
    label2 = Label(editar_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    BotonArtista = Button(editar_screen, text="Artist    " ,width ='60' ,height='4' ,command =artistedit).place(x=500, y=280)
    BotonAlbum = Button(editar_screen, text="Album   ",width ='60' ,height='4' , command = albumedit).place(x=500, y=350)
    BotonCancion = Button(editar_screen, text="Canción",width ='60' ,height='4' , command = cancionedit).place(x=500, y=420)

def cancionedit():
    global cancionedit_screen
    cancionedit_screen = Toplevel(login_screen)
    cancionedit_screen.title("Edit Cancion")
    cancionedit_screen.geometry("2000x1500")
    cancionedit_screen.configure(background = 'black')

    ## CREAR IMAGEN
    foto2 = PhotoImage(file = "header.png")
    label2 = Label(cancionedit_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    ## CREAR IMAGEN
    foto4 = PhotoImage(file = "genre1.png")
    label4 = Label(cancionedit_screen, image = foto4)
    label4.image =foto4
    label4.place(x=75, y =300)

    ## CREAR IMAGEN
    foto3 = PhotoImage(file = "genre2.png")
    label3 = Label(cancionedit_screen, image = foto3)
    label3.image =foto3
    label3.place(x=350, y =600)

    global entrynew3
    global entryprim3
    global entrynew4
    global entrynew5
    global entrynew6
    global entrynew7

    label3 =Label(cancionedit_screen,text='Ingrese el nombre actual de la cancion :')
    label3.place(x=500,y=260)
    entryprim3 = Entry(cancionedit_screen)
    entryprim3.place(x=500, y=290)

    label3 =Label(cancionedit_screen,text='Ingrese el valor nuevo del nombre:')
    label3.place(x=800,y=260)
    entrynew3 = Entry(cancionedit_screen)
    entrynew3.place(x=800, y= 290)

    label3 =Label(cancionedit_screen,text='Ingrese el genero nuevo (el numero) :')
    label3.place(x=800,y=330)
    entrynew4 = Entry(cancionedit_screen)
    entrynew4.place(x=800, y=360)

    label3 =Label(cancionedit_screen,text='Ingrese la nueva duracion:')
    label3.place(x=800,y=400)
    entrynew5 = Entry(cancionedit_screen)
    entrynew5.place(x=800, y= 430)

    label3 =Label(cancionedit_screen,text='Ingrese el nombre del album nuevo:')
    label3.place(x=800,y=460)
    entrynew6 = Entry(cancionedit_screen)
    entrynew6.place(x=800, y= 490)

    label3 =Label(cancionedit_screen,text='Ingrese el nuevo precio:')
    label3.place(x=800,y=520)
    entrynew7 = Entry(cancionedit_screen)
    entrynew7.place(x=800, y= 550)

    button1 = Button(cancionedit_screen, text="Modificar",command =modificartrack)
    button1.place(x =1300, y= 700)



def albumedit():
    global albumedit_screen
    albumedit_screen = Toplevel(login_screen)
    albumedit_screen.title("Edit Album")
    albumedit_screen.geometry("2000x1500")
    albumedit_screen.configure(background = 'black')

    ## CREAR IMAGEN
    foto2 = PhotoImage(file = "header.png")
    label2 = Label(albumedit_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    global entrynew2
    global entryprim2

    label3 =Label(albumedit_screen,text='Ingrese el nombre actual del album :')
    label3.place(x=500,y=260)
    entryprim2 = Entry(albumedit_screen)
    entryprim2.place(x=500, y=290)

    label3 =Label(albumedit_screen,text='Ingrese el valor nuevo:')
    label3.place(x=800,y=260)
    entrynew2 = Entry(albumedit_screen)
    entrynew2.place(x=800, y= 290)

    button1 = Button(albumedit_screen, text="Modificar",command =modificaralb)
    button1.place(x =1300, y= 700)


def artistedit():
    global artistedit_screen
    artistedit_screen = Toplevel(login_screen)
    artistedit_screen.title("Edit Artista")
    artistedit_screen.geometry("2000x1500")
    artistedit_screen.configure(background = 'black')

    ## CREAR IMAGEN
    foto2 = PhotoImage(file = "header.png")
    label2 = Label(artistedit_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    global entrynew1
    global entryprim1


    label3 =Label(artistedit_screen,text='Ingrese el nombre actual del artista :')
    label3.place(x=500,y=260)
    entryprim1 = Entry(artistedit_screen)
    entryprim1.place(x=500, y=290)

    label3 =Label(artistedit_screen,text='Ingrese el valor nuevo:')
    label3.place(x=800,y=260)
    entrynew1 = Entry(artistedit_screen)
    entrynew1.place(x=800, y= 290)

    button1 = Button(artistedit_screen, text="Modificar",command =modificara)
    button1.place(x =1300, y= 700)


def modificara():
    global modificar_screen
    modificar_screen = Toplevel(login_screen)
    modificar_screen.title("Success")
    modificar_screen.geometry("150x100")


    x2 = entryprim1.get()
    x3= entrynew1.get()
    try:
        sql = "UPDATE artist SET name = '"+x3+"', user_edit='"+usuario+"' WHERE name = '"+x2+"'"
        print(sql)
        cursor.execute(sql)
        connection.commit()
        print(cursor.rowcount, "record(s) affected")
        Label(modificar_screen, text="Modificado Correctamente ").pack()
        Button(modificar_screen, text="OK", command=delete_modificar).pack()

    except:
        Label(modificar_screen, text="No se pudo modificar ").pack()
        Button(modificar_screen, text="OK", command=delete_modificar).pack()


def modificaralb():

    global modificar_screen
    modificar_screen = Toplevel(login_screen)
    modificar_screen.title("Success")
    modificar_screen.geometry("150x100")


    x2 = entryprim2.get()
    x3= entrynew2.get()
    try:
        sql = "UPDATE album SET title = '"+x3+"', user_edit='"+usuario+"' WHERE title = '"+x2+"'"
        cursor.execute(sql)
        connection.commit()
        print(cursor.rowcount, "record(s) affected")
        Label(modificar_screen, text="Modificado Correctamente ").pack()
        Button(modificar_screen, text="OK", command=delete_modificar).pack()

    except:
        Label(modificar_screen, text="No se pudo modificar ").pack()
        Button(modificar_screen, text="OK", command=delete_modificar).pack()

def modificartrack():
    global modificar_screen
    modificar_screen = Toplevel(login_screen)
    modificar_screen.title("Success")
    modificar_screen.geometry("150x100")

    x2 = entryprim3.get()
    x3= entrynew3.get()
    x4= entrynew4.get()
    x5 = entrynew5.get()
    x6 = entrynew6.get()
    x7 = entrynew7.get()

    print(x2,x3,x4,x5,x6,x7)


    ratuvelo = ""
    busquedaquerry = "SELECT name,genreid, milliseconds, albumid, unitprice from track WHERE name = '"+x2+"'"
    postgreSQL_select_Query = busquedaquerry
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    nombre_original= ""
    genre_original= ""
    milliseconds_original = ""
    album_original = ""
    unitprice_original= ""
    for record in records:
        nombre_original = record[0]
        genre_original = record[1]
        milliseconds_original = record[2]
        album_original= record[3]
        unitprice_original=record[4]


    print(type(genre_original))

    print(nombre_original, genre_original, milliseconds_original, album_original, unitprice_original)
    if x3 == "":
        x3 = nombre_original
    if x4 == "" and genre_original != None:
        x4 = str(genre_original)
        print('entro2')
    if x4 == "" and genre_original == None:
        print('entro1')
        x4 = '26'
    if x5 == "" and milliseconds_original != None:
        x5 = str(milliseconds_original)
    if x6 == "":
        x6 = str(album_original)
    if x7 == "":
        x7 = str(unitprice_original)


    try:
        sql = "UPDATE track SET name = '"+x3+"', user_edit='"+usuario+"',genreid=(SELECT '"+x4+"':: int),milliseconds=(SELECT '"+x5+"' ::int), albumid =(SELECT  '"+x6+"' :: int),unitprice=(SELECT '"+x7+"':: numeric) WHERE name = '"+x2+"'"
        print(sql)
        cursor.execute(sql)
        connection.commit()
        print(cursor.rowcount, "record(s) affected")
        Label(modificar_screen, text="Modificado Correctamente ").pack()
        Button(modificar_screen, text="OK", command=delete_modificar).pack()

    except:
        Label(modificar_screen, text="No se pudo modificar ").pack()
        Button(modificar_screen, text="OK", command=delete_modificar).pack()

def activar():
    global activar_screen
    activar_screen = Toplevel(login_screen)
    activar_screen.title("Activar/Desactivar")
    activar_screen.geometry("2000x1500")
    activar_screen.configure(background = 'black')
    global var5
    global entryact


    ## CREAR IMAGEN
    foto2 = PhotoImage(file = "header.png")
    label2 = Label(activar_screen, image = foto2)
    label2.image =foto2
    label2.place(x=90, y =0)

    var5 = IntVar()
    Radiobutton(activar_screen, text="Activar    ", variable=var5, value=1,fg='navy', bg='black').place(x=5, y=260)
    Radiobutton(activar_screen, text="Desactivar   ", variable=var5, value=0,fg='navy' , bg='black').place(x=5, y=280)

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
            hola = ""
            for record in records:
                numero = str(record[0])
                hola = hola + numero
                print(type(record))
            hola2 =int(hola)
            print(hola2)
            if 1 == hola2:
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
            hola3 = ""
            for record in records:
                numero = str(record[0])
                hola3 = hola3 + numero
                print(type(record))
            hola4 =int(hola3)
            print(hola4)
            if 0 == hola4:
                Label(desactivacion_screen, text="Ya esta desactivada ").pack()
                Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()
            else:
                try:
                    sql = "UPDATE track SET activated = 0 WHERE name = '"+x1+"'"
                    cursor.execute(sql)
                    if cursor.rowcount >= 1:
                        print(cursor.rowcount, "record(s) affected")
                        Label(desactivacion_screen, text="Desactivado Correctamente ").pack()
                        Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()
                except:
                    Label(desactivacion_screen, text="No se logro desactivar correctamente ").pack()
                    Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()
        except:
            print("No se encontro una cancion con este nombre")
            Label(desactivacion_screen, text="No se encontro una cancion con este nombre").pack()
            Button(desactivacion_screen, text="OK", command=delete_desactivacion).pack()



def reportes():
    global reportes_screen
    reportes_screen = Toplevel(login_screen)
    reportes_screen.title("Reportes")
    reportes_screen.geometry("2000x1500")
    reportes_screen.configure(background = 'black')

    ## ampliacion de reporteria boton
    Button(reportes_screen,text='Ampliacion de reporteria', command= ampliacion_reporteria).place(x=1150, y=560)

    ## 1er reporte

    Label1 = Label(reportes_screen,text="1. Los artistas con más álbumes publicados")
    Label1.pack(anchor= 'nw')
    querry = "SELECT artist.name, COUNT(*) AS numero_de_discos FROM album INNER JOIN artist ON album.artistid = artist.artistid GROUP BY album.artistid, artist.name ORDER BY COUNT(*) DESC LIMIT 5"
    postgreSQL_select_Query = querry
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
    records1=Label(reportes_screen, text=hola, fg = 'white', bg='black')
    records1.pack(anchor= 'nw')

    Button(reportes_screen, text="Generar CSV de reporte 1", command=generate_CVS1).place(x=1150, y=600)



    ## segundo reporte

    Label2 =Label(reportes_screen,text="2. Géneros con más canciones")
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

    Button(reportes_screen, text="Generar CSV de reporte 2", command=generate_CVS2).place(x=1150, y=625)



    ## 3er reporte

    Label3 = Label(reportes_screen,text="3. Total de duración de cada playlist")
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


    Button(reportes_screen, text="Generar CSV de reporte 3", command=generate_CVS3).place(x=1150, y=650)



    ## 4to reporte

    Label4 = Label(reportes_screen,text="4. Canciones de mayor duración con la información de sus artistas")
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


    Button(reportes_screen, text="Generar CSV de reporte 4", command=generate_CVS4).place(x=1150, y=675)


    ##reporte 5

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

    Button(reportes_screen, text="Generar CSV de reporte 5", command=generate_CVS5).place(x=1150, y=700)


    ## reporte 6

    Label6 = Label(reportes_screen,text="6. Promedio de duración de canciones por género")
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

    Button(reportes_screen, text="Generar CSV de reporte 6", command=generate_CVS6).place(x=1150, y=725)


    ## reporte 7

    Label7 = Label(reportes_screen,text="7. Cantidad de artistas diferentes por playlist")
    Label7.place(x=1150, y=0)
    querry7 = "SELECT playlist.name, COUNT(DISTINCT artist.name) AS numero_artistas FROM track INNER JOIN album ON track.albumid=album.albumid INNER JOIN artist ON artist.artistid = album.artistid INNER JOIN playlisttrack ON playlisttrack.trackid = track.trackid INNER JOIN playlist ON playlist.playlistid = playlisttrack.playlistid GROUP BY playlist.name ORDER BY numero_artistas DESC"
    postgreSQL_select_Query = querry7
    cursor.execute(postgreSQL_select_Query)
    records7 = cursor.fetchall()
    loco = ""
    for record in records7:
        print(record[0],record[1])
        numero = str(record[1])
        loco = loco +record[0]+" "+numero +" artistas\n"
        print(type(record))

    print(loco)
    records7=Label(reportes_screen, text=loco, fg = 'white', bg='black')
    records7.place(x=1150, y=25)

    Button(reportes_screen, text="Generar CSV de reporte 7", command=generate_CVS7).place(x=1150, y=750)



    ##reporte 8

    Label8 = Label(reportes_screen,text="8. Los artistas con más diversidad de géneros musicales")
    Label8.place(x=1050,y= 400)
    querry8 ="SELECT artist.name, COUNT(DISTINCT genre.name) AS numero_generos FROM track JOIN album ON album.albumid = track.albumid JOIN artist ON album.artistid = artist.artistid JOIN genre ON track.genreid = genre.genreid GROUP BY artist.name ORDER BY numero_generos DESC LIMIT 5"
    postgreSQL_select_Query = querry8
    cursor.execute(postgreSQL_select_Query)
    records8 = cursor.fetchall()
    palabra = ""
    for record in records8:
        print(record[0],record[1])
        numero = str(record[1])
        palabra = palabra +record[0]+" "+numero +" generos\n"
        print(type(record))

    print(palabra)
    records8=Label(reportes_screen, text=palabra, fg = 'white', bg='black')
    records8.place(x=1150, y=425)

    Button(reportes_screen, text="Generar CSV de reporte 8", command=generate_CVS8).place(x=1150, y=775)


def ampliacion_reporteria():
    global cal2
    global cal3
    global ampliacion_reportes_screen
    ampliacion_reportes_screen = Toplevel(login_screen)
    ampliacion_reportes_screen.title("Ampliacion de reportes")
    ampliacion_reportes_screen.geometry("2000x1500")
    ampliacion_reportes_screen.configure(background = 'black')

    ## @TODO Hay que preguntar al usuario que fechas quiere ingresar##
    ## 1er reporte
    Label1 = Label(ampliacion_reportes_screen,text="1. Total de ventas por semana")
    Label1.place(x=100,y=0)
    #Segundo Reporte
    Label2 = Label(ampliacion_reportes_screen,text="2. Los N artistas con las mayores ventas")
    Label2.place(x=300,y=0)
    #Tercer Reporte
    Label3 = Label(ampliacion_reportes_screen,text="3. Total de ventas por género ")
    Label3.place(x=650,y=0)
    #Cuarto Reporte
    Label4 = Label(ampliacion_reportes_screen,text="4. Las N canciones con más reproducciones para un artista a ser ingresado por el usuario.")
    Label4.place(x=800,y=0)

    style = ttk.Style(ampliacion_reportes_screen)
    style.theme_use('clam')

    primer_date = Label(ampliacion_reportes_screen, text = "Ingrese primera fecha").place(x=5,y=40)
    cal2 = DateEntry(ampliacion_reportes_screen,background="black", disabledbackground="black", bordercolor="black",
                     headersbackground="black", normalbackground="black", foreground='navy',normalforeground='navy', headersforeground='navy')
    cal2.config(background = 'black')
    cal2.place(x=10, y= 70)

    segundo_date = Label(ampliacion_reportes_screen, text = "Ingrese segunda fecha").place(x=5,y=100)
    cal3 = DateEntry(ampliacion_reportes_screen,background="black", disabledbackground="black", bordercolor="black",
                     headersbackground="black", normalbackground="black", foreground='navy',normalforeground='navy', headersforeground='navy')
    cal3.config(background = 'black')
    cal3.place(x=10, y= 130)


    bottonclick = Button(ampliacion_reportes_screen, text='Seleccionar rango de fechas',command = calval2)
    bottonclick.place(x=10, y=170)

    #Button(ampliacion_reportes_screen, text="Generar CSV de reporte 1", command=generate_CVS9).place(x=1150, y=600)


def calval2():
    fecha_select = cal2.get_date()
    querry9="select name, sum(total) FROM ventas_por_artista WHERE invoicedate > (fecha_select) AND invoicedate < (fecha_select) GROUP BY name ORDER BY sum(total) DESC LIMIT (fecha_select)"
    querry10="select name, sum(total) FROM ventas_por_genero WHERE invoicedate > (fecha_select) AND invoicedate < (fecha_select) GROUP BY name ORDER BY sum(total) DESC"
    querry11="select artist.name, track.name, sum(cant_rep) FROM reprod_por_artista WHERE artist.name = (fecha_select) GROUP BY track.name LIMIT (fecha_select)"
    postgreSQL_select_Query = querry9
    cursor.execute(postgreSQL_select_Query)
    records9 = cursor.fetchall()
    hola = ""
    for record in records9:
        print(record[0],record[1])
        numero = str(record[1])
        palabra = palabra +record[0]+" "+numero +" artistas\n"
        print(type(record))
    print(hola)
    records9=Label(reportes_screen, text=hola, fg = 'white', bg='white')
    records9.place(x=300,y=100)
    records9.pack(anchor= 'nw')




def searchmusic ():
    select = var.get()
    x1 = entry1.get()
    x2 = 'artist.name, track.name'
    whereclause = ''
    if select == 1:
        selection = 'track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        whereclause = "artist.name='"+x1+"'"
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+"AND track.activated = 1 LIMIT 10"
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
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+"AND track.activated = 1 LIMIT 10"
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
        querry= "select " +x2+" from "+selection+" WHERE "+whereclause+"AND track.activated = 1 LIMIT 10"
        querry =str(querry)
        print(querry)
        postgreSQL_select_Query = querry
        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()

        hola = ""
        for record in records:
            print(record[0],record[1])
            hola = hola + record[0]+": cancion: "+record[1]+ " album: "+record[2] +"\n"
            print(type(record))

        print(hola)
        records1=Label(login_success_screen, text=hola, fg = 'white', bg='black')
        records1.place(x= 500, y = 300)
    if select == 5:
        selection = 'track INNER JOIN album ON track.albumid = album.albumid INNER JOIN artist ON album.artistid = artist.artistid'
        x2= 'artist.name, track.name, album.title'
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
            hola = hola + record[0]+": cancion: "+record[1]+ " album: "+record[2] +"\n"
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

def delete_modificar():
    modificar_screen.destroy()

def delete_quitar():
    quitar_screen.destroy()

def delete_carrito():
    borrado_screen.destroy()

def delete_compras():
    agregado_screen.destroy()

def delete_desactivacion():
    desactivacion_screen.destroy()

def delete_agregar():
    agregar1_screen.destroy()

def generate_CVS1():
    querry = "SELECT artist.name, COUNT(*) AS numero_de_discos FROM album INNER JOIN artist ON album.artistid = artist.artistid GROUP BY album.artistid, artist.name ORDER BY COUNT(*) DESC LIMIT 5"
    postgreSQL_select_Query = querry
    cursor.execute(postgreSQL_select_Query)
    records = cursor.fetchall()
    reporte1 = open('artista_mas_albums_publicados.csv','w')
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
    reporte2 = open('generos_mas_canciones.csv','w')
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
    reporte3 = open('duracion_playlist.csv','w')
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
    reporte4 = open('canciones_mas_duracion_info_artista.csv','w')
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
    reporte5 = open('Canciones_agg_por_usuarios.csv','w')
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
    reporte6 = open('Duracion_promedio_genero.csv','w')
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
    reporte7 = open('artistas_por_playlist.csv','w')
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
    reporte8 = open('artistas_diversidad.csv','w')
    with reporte8:
        fields8 = ['artista','cantidad']
        writer = csv.DictWriter(reporte8,fieldnames=fields8)
        writer.writeheader()
        for record in records8:
            artista = str(record[0])
            numero = str(record[1])
            writer.writerow({'artista': artista,'cantidad':numero})



main_account_screen() # call the main_account_screen() function

