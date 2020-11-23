from flask import Flask, render_template, request, json, session, render_template
from flaskext.mysql import MySQL
import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

app = Flask(__name__)

app.secret_key ='matangalachanga'

app.config["DEBUG"] = True
app.config['MYSQL_DATABASE_USER'] = 'sepherot_jennifer'
app.config['MYSQL_DATABASE_PASSWORD'] = 'AW4ur5mHBR'
app.config['MYSQL_DATABASE_DB'] = 'sepherot_jenniferBD'
app.config['MYSQL_DATABASE_HOST'] = 'nemonico.com.mx'
mysql = MySQL(app)
mysql.init_app(app)

def PDF(_n, _em, _ed, _d, _c, _p, _a, _s, _t, _f, _r):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        asp = cursor.execute('SELECT * FROM estado WHERE nombre = %s;',  (_n))
        _urline="./Contrato.pdf"
        doc = SimpleDocTemplate(_urline, pagesize=letter,
                                rightMargin=60, leftMargin=60,
                                topMargin=40, bottomMargin=40)
        Story = []
        _urline="./static/go.png"
        logotipo = _urline
        #datos del aspirante
        nombre = _n
        empresa = _em
        edad = _ed
        domicilio = _d
        correo = _c
        puesto = _p
        area = _a
        sueldo = _s
        tipo = _t
        fecha = _f
        reclutador = _r
        #datos de la foto 
        imagen = Image(logotipo, 2 * inch, 2 * inch)
        Story.append(imagen)
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        # Creacion del correo
        Story.append(Spacer(1, 12))
        texto = 'A quien corresponda:'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 12))

        texto = 'Nos gustaría darle la bienvenida al nuevo miembro:  %s  \
                que empezará a trabajar en la empresa %s con todo lo que corresponda.  \
                Se le designarán ciertas actividades dependiendo de sus conocimientos  \
                y aptitudes. El nuevo miebro se debe de comprometer con cada una de estas  \
                actividades. El nuevo miebro se debe de comprometer a siempre tratar con  \
                respeto, tanto a sus superiores como a sus compañeros de trabajo.  \
                El nuevo miembro se compromete a nunca compartir información importante  \
                con personas externas, ya sean familiares, amigos o conocidos.  \
                Este documento oficial valida los datos del contratado son los siquientes:  \
                Persona fisicia con la edad de %s que habita en %s con el correo %s \
                Entrará en el puesto de %s en el area de %s como asi quedo estipulado\
                Recibirá un sueldo de  de %s pesos al mes. \
                definiendo que su contrato es de  %s hasta el momento \
                Fecha de ingreso %s por el reclutador %s. \
                Validando que estos datos que se nos han proporcionado son los correctos y \
                sin más por el momento, le damos una grata bienvendida. \
                \
                DECLARACIONES \
                CLÁUSULA PRIMERA: Que está en desempleo e inscrito en el acuerdo de \
                Servicios Públicos del país. \
                CLÁUSULA SEGUNDA: Que tiene un contrato establecido con la empresa \
                con un tiempo de validez de  tres meses con descanso exclusivamente \
                los fines de semana. Días feriados serán laborables. \
                CLÁUSULA TERCERA: Consciente de que la jornada laboral será a tiempo completo. \
                La jornada se regirá por 12 horas días laboradas. \
                CLÁUSULA CUARTA: Al finalizar el contrato el empleado NO recibirá indemnización \
                económica por el periodo trabajado con la empresa. \
                Será solo tres meses de gestión institucional.' % (nombre, empresa, edad, domicilio, correo, puesto, area, sueldo, tipo, fecha, reclutador)
        
        Story.append(Paragraph(texto, estilos["Justify"]))
        Story.append(Spacer(1, 48))


        texto = 'Firma del director,'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 48))
        texto = '________________________.'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 12))
        texto = 'Elisa Rivera'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 12))
        doc.build(Story)
        asp = cursor.fetchall()
    finally:
        cursor.close()   