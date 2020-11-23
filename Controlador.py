from flask import Flask, render_template, request, json, url_for, session, redirect, g, jsonify
import requests
from flaskext.mysql import MySQL
import bcrypt
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
import os
import Modelo as Modelo
import ModeloContrato as ModeloContrato
import imaplib
import email
import time
from bs4 import BeautifulSoup
import re
import jinja2
import ctypes


app = Flask(__name__)

#contraseña super secreta
app.secret_key ='matangalachanga'

#conectar a la base de datos
app.config['MYSQL_DATABASE_USER'] = 'sepherot_jennifer'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AW4ur5mHBR'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_jenniferBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL()
mysql.init_app(app)

#abrir los archivos
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] ='gofaster'
app.config['UPLOAD_FOLDER2'] ='./static/comprobante'
app.config['UPLOAD_FOLDER3'] ='./static'
app.config['UPLOAD_EXTENSIONS'] = '.pdf', '.png' , '.jpeg'
app.config['SESSION_TYPE'] = 'filesystem'

#AQUI EMPIEZA LO DIFICIL
class About:
    def __init__(self, numero):
        self.numero     = numero
        self.nombre     = None

    def setNumero(self, numero):
        self.Numero = numero
    def getNumero(self):
        return self.Numero
        
    def setNombre(self, diccionario):
        self.Nombre = diccionario
    def getNombre(self):
        return self.Nombre

    def setEmpresa(self, diccionario):
        self.Empresa = diccionario
    def getEmpresa(self):
        return self.Empresa

    def setEdad(self, edad):
        self.Edad = edad
    def getEdad(self):
        return self.Edad
    
    def setDomicilio(self, domicilio):
        self.Domicilio = domicilio
    def getDomicilio(self):
        return self.Domicilio
    
    def setCorreo(self, correo):
        self.Correo = correo
    def getCorreo(self):
        return self.Correo
    
    def setPuesto(self, puesto):
        self.Puesto = puesto
    def getPuesto(self):
        return self.Puesto

    def setArea(self, area):
        self.Area = area
    def getArea(self):
        return self.Area
    
    def setSueldo(self, sueldo):
        self.Sueldo = sueldo
    def getSueldo(self):
        return self.Sueldo
    
    def setTipo(self, tipo):
        self.Tipo = tipo
    def getTipo(self):
        return self.Tipo
    
    def setFecha(self, fecha):
        self.Fecha = fecha
    def getFecha(self):
        return self.Fecha
    
    def setReclutador(self, reclutador):
        self.Reclutador = reclutador
    def getReclutador(self):
        return self.Reclutador

    def setImagen(self, imagen):
        self.Imagen= imagen
    def getImagen(self):
        return self.Imagen


#para guardar el usuario
@app.before_request
def before_request():
   g.user = None
   if 'name' in session:
      g.user = Modelo.buscarU(session['name'])

#pagina inicial
@app.route("/")
def index():
    return render_template("login.html")

#pagina de registro, solo para mi.
@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method == "POST":
        _n = request.form['Name']
        _l = request.form['Lastname']
        _e = request.form['Email']
        _p = request.form['Password'].encode('utf-8')
        hash_p = bcrypt.hashpw(_p, bcrypt.gensalt())
        
        if _n and _l and _e and hash_p:
            Modelo.registro(_n, _l, _e, hash_p)
            return redirect(url_for('login'))

        #validar que no exista
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM USERS WHERE email=%s', (_e))
        val = cur.fetchone()
        print(val)
        cur.close()
        #si el usuario existe
        if len(val) is not 0:
            if _e == val[3]:
                Modelo.entidades(_e,'REGISTER.FAIL', 'registro fallido')
                return 'Error: Usuario ya existente'
        #si el usuario no existe
        else:
            Modelo.registro(_n, _l, _e, _p)
            session['name'] = val[1]
            session['email'] = val[3]
            Modelo.entidades(session['email'],'REGISTER', 'registro exitoso')
            return render_template('Login.html')      
    else:
        return render_template('Register.html')

#pagina de iniciar sesion
@app.route('/login', methods=['GET','POST'])
def login():
    if g.user:
        return redirect(url_for('aspirantes'))
    if request.method == 'POST':
        _e = request.form['Email']
        _p = request.form['Password']

        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM USERS WHERE email=%s', (_e))
        user = cur.fetchone()
        cur.close()
        if len(user) > 0:
            if _p == user[4]:                
                session['name']=user[1]
                session['correo'] =user[3]
                Modelo.entidades(session['correo'],'LOGIN', 'login exitoso')
                return redirect(url_for('aspirantes'))
        else:
            Modelo.entidades(session['correo'],'LOGIN.FAIL', 'login fallido')
            return render_template('error2.html')
    else:
        Modelo.entidades(session['correo'],'LOGIN.FAIL', 'login fallido')
        return render_template('error2.html')
    return render_template('Login.html')

#pagina para recuperar contraseña si se olvida
@app.route("/recuperar",methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        _e = request.form['Email']
        Modelo.Recuperar(_e)
        Modelo.entidades(_e,'RECUPERAR CONTRASEÑA', 'solicitó recuperar su contraseña')
        time.sleep(.5)
        return redirect(url_for('index'))
    return render_template("recuperar.html")


#pagina donde se ven todos los aspirantes
@app.route('/inicio', methods=['GET', 'POST'])
def aspirantes():
    consulta = Modelo.select()
    Modelo.entidades(session['correo'],'MOSTRAR ASPIRANTES', 'mostrar aspirantes exitoso')
    return render_template("index.html", eventos=consulta)    

@app.route('/ranking', methods=['GET', 'POST'])
def ranking():
    consulta = Modelo.select2()
    Modelo.entidades(session['correo'],'MOSTRAR ASPIRANTES', 'mostrar aspirantes exitoso')
    return render_template("reclutadores.html", eventos=consulta)  
             

#ingresar INE
@app.route('/Ine',methods= ['POST','GET'])
def Ine():
        #para comprobar que sea la misma persona
        busqueda= Modelo.buscarU2(session['id'])
        #aqui se abre el documento
        files = request.files.getlist('files[]')
        errors = {}
        success = False

        for file in files:
         if file:
            filename = secure_filename(file.filename)
            _nombrearchivo=filename
            #se llama a la funcion que hara el parseo de la foto
            Modelo.INE(busqueda,_nombrearchivo)  
            file.save(os.path.join(app.config['UPLOAD_FOLDER3'], filename))
            success = True

        if success:
            resp = json.jsonify({'message' : 'Files successfully uploaded'})
            _nombrearchivo=filename
            _urline="./static/INE\\"+filename
            Modelo.ImagenATextoINE(busqueda,_urline)
            resp.status_code = 201
            Modelo.entidades(session['email'],'CARGAR INE', 'carga de INE exitoso')
            return resp
            #return redirect(url_for('verificados'))
        #else:
            #Modelo.entidades(session['email'],'CARGAR INE.FAIL', 'carga de INE fallido')
            #return redirect(url_for('nonval'))

#ingresar COMPROBANTE
@app.route('/COMPROBANTE',methods= ['POST','GET'])
def COMPROBANTE():
        #para comprobar que sea la misma persona
        busqueda= Modelo.buscarU2(session['id'])
        #aqui se abre el documento
        files = request.files.getlist('files[]')
        errors = {}
        success = False
        for file in files:
         if file:
            filename = secure_filename(file.filename)
            _nombrearchivo=filename
            #se llama a la funcion que hara el parseo de la foto
            Modelo.COMPROBANTE(busqueda,_nombrearchivo)  
            file.save(os.path.join(app.config['UPLOAD_FOLDER3'], filename))
            success = True

        if success:
            resp = json.jsonify({'message' : 'Files successfully uploaded'})
            _nombrearchivo=filename
            _urline="./static/"+filename
            Modelo.ImagenATextoCOMPROBANTE(busqueda,_urline)
            resp.status_code = 201
            Modelo.entidades(session['email'],'CARGAR COMPROBANTE', 'carga de COMPROBANTE exitoso')
            return resp
            return redirect(url_for('verificados'))
        else:
            Modelo.entidades(session['email'],'CARGAR COMPROBANTE.FAIL', 'carga de COMPROBANTE fallido')
            return redirect(url_for('nonval'))
       #return render_template("validar.html")


#ingresar ESCOLARIDAD
@app.route('/ESCOLARIDAD',methods= ['POST','GET'])
def ESCOLARIDAD():
        #para comprobar que sea la misma persona
        busqueda= Modelo.buscarU2(session['id'])
        #aqui se abre el documento
        files = request.files.getlist('files[]')
        errors = {}
        success = False
        for file in files:
         if file:
            filename = secure_filename(file.filename)
            _nombrearchivo=filename
            #se llama a la funcion que hara el parseo de la foto
            Modelo.ESCOLARIDAD(busqueda,_nombrearchivo)  
            file.save(os.path.join(app.config['UPLOAD_FOLDER4'], filename))
            success = True

        if success:
            resp = json.jsonify({'message' : 'Files successfully uploaded'})
            _nombrearchivo=filename
            _urline="./static/"+filename
            Modelo.ImagenATextoESCOLARIDAD(busqueda,_urline)
            resp.status_code = 201
            Modelo.entidades(session['email'],'CARGAR CERTIFICADO', 'carga de CERTIFICADO exitoso')
            return resp
            return redirect(url_for('verificados'))
        else:
            Modelo.entidades(session['email'],'CARGAR CERTIFICADO.FAIL', 'carga de CERTIFICADO fallido')
            return redirect(url_for('nonval'))
       #return render_template("validar.html")
       
        
#pagina donde se crea el PDF
@app.route('/contrato', methods=['GET', 'POST'])
def contrato():
    if request.method == 'POST':
        _n = request.form['Nombre']
        _em = request.form['Empresa']
        _ed = request.form['Edad']
        _d = request.form['Domicilio']
        _c = request.form['Correo']
        _p = request.form['Puesto']
        _a = request.form['Area']
        _s = request.form['Sueldo']
        _t = request.form['Tipo']
        _f = request.form['Fecha']
        _r = request.form['Reclutador']
        
        if (_n and _em and _ed and _d and _c and _p and _a and _s and _t and _f and _r):
            ModeloContrato.PDF(_n, _em, _ed, _d, _c, _p, _a, _s, _t, _f, _r)
            time.sleep(.5)
            Modelo.entidades(session['email'],'CREAR PDF', 'creación del PDF exitosa')
            return redirect(url_for('aspirantes'))
        else:
            Modelo.entidades(session['email'],'CREAR PDF.FAIL', 'creación del PDF fallida')
            return redirect(url_for('error'))

#pagina para mandar el PDF por correo
@app.route('/email')
def emaild():
    Modelo.entidades(session['email'],'ENVIAR PDF', 'envió del PDF exitoso')
    Modelo.Firma()
    return redirect(url_for('aspirantes'))


@app.route('/borrar', methods=['GET','POST'])
def borrar():
    if request.method == 'POST':
        Modelo.entidades(session['email'],'VALIDAR', 'Validar exitoso')
        data=request.get_json()
        borrid=data['borrid']
        _borrarticket = Modelo.borrarticket(borrid)
        print(_borrarticket)
        if _borrarticket:
            return json.dumps(True)
        return json.dumps("algo")

@app.route('/borrar2', methods=['GET','POST'])
def borrar2():
    if request.method == 'POST':
        Modelo.entidades(session['email'],'VALIDAR', 'Validar exitoso')
        data=request.get_json()
        borrid=data['borrid2']
        _borrarticket = Modelo.borrarticket2(borrid)
        print(_borrarticket)
        if _borrarticket:
            return json.dumps(True)
        return json.dumps("algo")

@app.route('/borrar3', methods=['GET','POST'])
def borrar3():
    if request.method == 'POST':
        data=request.get_json()
        borrid=data['borrid3']
        _borrarticket = Modelo.borrarticket3(borrid)
        print(_borrarticket)
        if _borrarticket:
            return json.dumps(True)
        return json.dumps("algo")
        Modelo.entidades(session['email'],'VALIDAR', 'Validar exitoso')

@app.route('/borrar4', methods=['GET','POST'])
def borrar4():
    if request.method == 'POST':
        Modelo.Firma()
        Modelo.entidades(session['email'],'VALIDAR', 'Validar exitoso')
        data=request.get_json()
        borrid=data['borrid4']
        _borrarticket = Modelo.borrarticket4(borrid)
        print(_borrarticket)
        if _borrarticket:
            return json.dumps(True)
        return json.dumps("algo")