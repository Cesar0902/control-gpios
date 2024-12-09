# Developer: Universidad
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from tkinter import Frame
import os
import time
import mysql.connector as sql

#----------------------------------------------------GPIO TEMPLATE----------------------------------------------------
class GPIOController:
    def __init__(self, gpio_number, frame, img_on, img_off, password="1234567"):
        self.gpio_number = gpio_number
        self.frame = frame
        self.img_on = img_on
        self.img_off = img_off
        self.password = password

        # Archivos y scripts
        self.estado_path = f"/home/cesar/estado{gpio_number}.txt"
        self.on_script = f"/home/cesar/on{gpio_number}.sh"
        self.off_script = f"/home/cesar/off{gpio_number}.sh"
        self.email_on_script = f"/home/cesar/sendEmailOn{gpio_number}.sh"
        self.email_off_script = f"/home/cesar/sendEmailOff{gpio_number}.sh"
        self.inbox_script = f"/home/cesar/lecturaInbox{gpio_number}.sh"

        # Variables para controles
        self.check_var = StringVar()
        self.radio_var = StringVar()
        self.combo_var = StringVar()
        self.receive_email_var = StringVar()
        self.send_email_var = StringVar()

        self.crear_interfaz()

        # Actualizaciones automaticas.
        self.actualiza_estado_label()
        self.actualiza_estado_boton()

    def crear_interfaz(self):
        # Título
        Label(self.frame, text=f"CONTROL GPIO {self.gpio_number}", font=text2, fg="blue", bg="ghostwhite").place(x=120, y=10)

        # Botones de encendido y apagado
        Button(self.frame, text="ON", command=self.encender_gpio, fg="white", bg="green").place(x=88, y=75)
        Button(self.frame, text="OFF", command=self.apagar_gpio, fg="white", bg="red").place(x=85, y=110)

        # CheckBox ON/OFF
        ttk.Checkbutton(self.frame, text="ON/OFF", variable=self.check_var, command=self.evaluar_checkbox).place(x=10, y=150)

        # RadioButtons
        ttk.Radiobutton(self.frame, text="ON", variable=self.radio_var, value="1", command=self.evaluar_radiobutton).place(x=10, y=180)
        ttk.Radiobutton(self.frame, text="OFF", variable=self.radio_var, value="0", command=self.evaluar_radiobutton).place(x=60, y=180)

        # Combobox
        ttk.Combobox(self.frame, textvariable=self.combo_var, values=["ON", "OFF"]).place(x=150, y=215)
        Button(self.frame, text=">>", command=self.evaluar_combobox, bg="darkcyan").place(x=330, y=210)

        # Checkbox para recibir email
        ttk.Checkbutton(self.frame, text="Enable/Disable Receive Email", variable=self.receive_email_var, command=self.evaluar_email).place(x=0, y=280)

        # Checkbox para enviar email
        ttk.Checkbutton(self.frame, text="Enable/Disable Send Email", variable=self.send_email_var, command=self.enviar_email).place(x=150, y=245)

        # Botón para programar tiempo
        Button(self.frame, text="Tiempo", command=self.dialogo_tiempo, bg="green", fg="beige").place(x=0, y=90)

    def encender_gpio(self):
        print(f"Encendido GPIO{self.gpio_number}")
        os.system(f"echo {self.password}|sudo -S sudo {self.on_script}")
        VaciarDatos()
        LlenarTabla()
    
    def apagar_gpio(self):
        print(f"Apagado GPIO{self.gpio_number}")
        os.system(f"echo {self.password}|sudo -S sudo {self.off_script}")
        VaciarDatos()
        LlenarTabla()
    
    def actualiza_estado_label(self):
        with open(self.estado_path, "r") as pf:
            for linea in pf:
                campo = linea.strip()
                if campo == "1":
                    Label(self.frame, text="1", font=text1).place(x=160, y=60)
                elif campo == "0":
                    Label(self.frame, text="0", font=text1).place(x=160, y=60)
        self.frame.after(1000, self.actualiza_estado_label)

    def actualiza_estado_boton(self):
        with open(self.estado_path, "r") as pf:
            for linea in pf:
                campo = linea.strip()
                if campo == "1":
                    Button(self.frame, image=self.img_on).place(x=250, y=60)
                elif campo == "0":
                    Button(self.frame, image=self.img_off).place(x=250, y=60)
        self.frame.after(1000, self.actualiza_estado_boton)
    
    def salvar_tiempo(self, horai, minini, horaf, minf):
        print(f"Registrando Tiempo GPIO{self.gpio_number}")
        hi = horai.get()
        mi = minini.get()
        hf = horaf.get()
        mf = minf.get()
        tab = " "
        dia = "*"
        mes = "*"
        ism = "*"
        user = "root"
        path1 = self.on_script
        path2 = self.off_script

        # Generar las cadenas para las tareas de cron
        cadena1 = f"{mi} {hi} {dia} {mes} {ism} {user} {path1}"
        cadena2 = f"{mf} {hf} {dia} {mes} {ism} {user} {path2}"

        # Asignar permisos completos para escritura
        os.system(f"echo {self.password}|sudo -S chmod -R 777 /etc/cron.d/tarea{self.gpio_number}_1")
        os.system(f"echo {self.password}|sudo -S chmod -R 777 /etc/cron.d/tarea{self.gpio_number}_2")

        # Escribir las tareas de cron
        with open(f"/etc/cron.d/tarea{self.gpio_number}_1", "w") as pf1:
            pf1.write(cadena1 + "\n")
        with open(f"/etc/cron.d/tarea{self.gpio_number}_2", "w") as pf2:
            pf2.write(cadena2 + "\n")

        # Pausa estratégica
        time.sleep(0.1)

        # Revertir permisos
        os.system(f"echo {self.password}|sudo -S chmod -R 755 /etc/cron.d/tarea{self.gpio_number}_1")
        os.system(f"echo {self.password}|sudo -S chmod -R 755 /etc/cron.d/tarea{self.gpio_number}_2")

        # Reiniciar el servicio cron
        os.system(f"echo {self.password}|sudo -S /etc/init.d/cron restart")

        # Limpiar las entradas
        self.clean(horai, minini, horaf, minf)
    
    def clean(self, horai, minini, horaf, minf):
        horai.set("")
        minini.set("")
        horaf.set("")
        minf.set("")
    
    def dialogo_tiempo(self):
        def salvar():
            self.salvar_tiempo(horai, minini, horaf, minf)

        v1 = Toplevel()
        v1.title(f"Temporizador GPIO{self.gpio_number}")
        v1.geometry("310x200")

        text3 = font.Font(family="Arial", size=12)

        # Etiquetas
        Label(v1, text="--- TEMPORIZADOR ---", font=text3).place(x=10, y=5)
        Label(v1, text="Hora Encendido:", font=text3).place(x=10, y=50)
        Label(v1, text="Minuto Encendido:", font=text3).place(x=10, y=90)
        Label(v1, text="Hora Apagado:", font=text3).place(x=10, y=130)
        Label(v1, text="Minuto Apagado:", font=text3).place(x=10, y=170)

        # Variables de entrada
        horai = StringVar()
        minini = StringVar()
        horaf = StringVar()
        minf = StringVar()

        # Entradas
        Entry(v1, textvariable=horai, width=10).place(x=150, y=50)
        Entry(v1, textvariable=minini, width=10).place(x=150, y=90)
        Entry(v1, textvariable=horaf, width=10).place(x=150, y=130)
        Entry(v1, textvariable=minf, width=10).place(x=150, y=170)

        # Botón para guardar
        Button(v1, text="SAVE", command=salvar).place(x=240, y=100)
        v1.mainloop()

    def evaluar_checkbox(self):
            if self.check_var.get() == "1":
                self.encender_gpio()
            else:
                self.apagar_gpio()
    
    def evaluar_radiobutton(self):
        if self.radio_var.get() == "1":
            self.encender_gpio()
        else:
            self.apagar_gpio()
    
    def evaluar_combobox(self):
        if self.combo_var.get() == "ON":
            self.encender_gpio()
            os.system(f"echo {self.password}|sudo -S sudo {self.email_on_script}")
        elif self.combo_var.get() == "OFF":
            self.apagar_gpio()
            os.system(f"echo {self.password}|sudo -S sudo {self.email_off_script}")
    
    def evaluar_email(self):
        if self.receive_email_var.get() == "1":
            os.system(f"echo {self.password}|sudo -S sudo {self.inbox_script} &")
            messagebox.showinfo("Save", f"Email Receive Service GPIO{self.gpio_number} --enabled--")
        else:
            os.system(f"echo {self.password}|sudo -S sudo pkill -f {self.inbox_script}")
            VaciarDatos()
            LlenarTabla()
            messagebox.showinfo("Save", f"Email Receive Service GPIO{self.gpio_number} --disabled--")
    
    def enviar_email(self):
        if self.send_email_var.get() == "1":
            messagebox.showinfo("Save", f"Email Send Service GPIO{self.gpio_number} --enabled--")
        else:
            messagebox.showinfo("Save", f"Email Send Service GPIO{self.gpio_number} --disabled--")

#-----------------------------------------Creando Ventana con las GPIOs-----------------------------------------
v0=Tk()
v0.title("Controles GPIO")
v0.geometry("1575x560+200+200")
fr1=ttk.Frame(v0,height="300",width="500")
fr2=ttk.Frame(v0,height="300",width="500")
fr3=ttk.Frame(v0,height="300",width="500")

table_data=ttk.Treeview(v0, columns=("col0","col1","col2","col3"),show="headings")

fr1.grid(row=0,column=0,padx=10,pady=20)
fr2.grid(row=0,column=1,padx=10,pady=20)
fr3.grid(row=0,column=2,padx=10,pady=20)

table_data.grid(row=1,column=0,sticky=E+W,columnspan=4)

scrollbar = ttk.Scrollbar(v0, orient=VERTICAL, command=table_data.yview)
table_data.configure(yscroll=scrollbar.set)
scrollbar.grid(row=1, column=3, sticky='ns')

#texto
text1=font.Font(family="Arial", size=80)
text2=font.Font(family="Arial",size=16)

#imagenes
img_on=PhotoImage(file="/home/cesar/on.png").subsample(4)
img_off=PhotoImage(file="/home/cesar/off.png").subsample(4)

gpio17 = GPIOController(17, fr1, img_on, img_off)
gpio22 = GPIOController(22, fr2, img_on, img_off)
gpio27 = GPIOController(27, fr3, img_on, img_off)

#-----------------------------------------Mostrar informacion de la BD-----------------------------------------
def VaciarDatos():                   
    informacion=table_data.get_children()                  
    
    for cant in informacion:
        table_data.delete(cant)                

def LlenarTabla():
    conexion=sql.connect(host="localhost",user="developer",
        password="Developer",database="arquitectura")

    consulta=StringVar()
    consulta="SELECT * FROM proyecto_final"
    
    cursor=conexion.cursor()
    cursor.execute(consulta)
    resultado=cursor.fetchall()                  
    
    for valor in resultado:
        table_data.insert("","0",values=valor)

    conexion.close()

table_data.column("#0",width=0,anchor=CENTER)
table_data.column("col0",width=100,anchor=CENTER)
table_data.column("col1",width=140,anchor=CENTER)
table_data.column("col2",width=140,anchor=CENTER)
table_data.column("col3",width=140,anchor=CENTER)

table_data.heading("col0",text="Id",anchor=CENTER)
table_data.heading("col1",text="Descripcion",anchor=CENTER)
table_data.heading("col2",text="Estado",anchor=CENTER)
table_data.heading("col3",text="Fecha",anchor=CENTER)

LlenarTabla()