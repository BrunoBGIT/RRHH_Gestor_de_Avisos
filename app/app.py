from asyncio.windows_events import NULL
from glob import glob
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from flask.templating import render_template
import datetime

app=Flask(__name__)

# CONEXION MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='bruno'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='rrhh_avisos'
conexion = MySQL(app) 


#mysql=MySQL()

@app.route('/')
def principal():
    return render_template('index.html')


@app.route('/Formulario_Aviso') #PERMITE INGRESAR EL NRO DE LEGAJO A BUSCAR
def solicitudes():
    return render_template('Formulario_Busca_Leg.html')

@app.route('/Formulario_Carga_Aviso', methods=['POST']) #TRAE LOS DATOS DEL LEGAJO E IMPRIME
def carga_datos_leg():
   
        if request.method=='POST':
            global legajo
            legajo=request.form['legajo_form']
            
            cursor=conexion.connection.cursor()
                #sql=('SELECT * FROM nomina WHERE legajo=%s', legajo)
                #cursor.execute(sql)
           
            cursor.execute("SELECT * FROM nomina WHERE legajo=%s", (legajo,))
            persona_evento=cursor.fetchone()
            if persona_evento is None:
                return render_template('legajo_no_encontrado.html')
                
            global nombre
            global sector
            nombre=persona_evento[1]
            sector=persona_evento[2]
            

        return render_template('Formulario_Carga_Aviso.html', persona=persona_evento)


    
@app.route('/aviso_cargado_exitosamente', methods=['POST']) #REGISTRA AVISO EN BD
def carga_aviso():
   
        if request.method=='POST': 
            dia_evento= request.form['dia_evento']

            #dia_evento_ddmmyy=datetime.datetime.strptime(dia_evento,'%Y-%m-%d')
            #dia_evento_ddmmyy= dia_evento
            #print("Fecha y Formato de Fecha")
            #print(dia_evento)
            #print(type(dia_evento))
            #print(dia_evento_ddmmyy)
            #print(type(dia_evento_ddmmyy))

            titulo_evento=request.form['titulo_evento']
            detalle_evento=request.form['detalle_evento']


            print (legajo)
            print (nombre)
            print (sector)
            print (dia_evento)
            print (dia_evento)
            print (titulo_evento)
            print (detalle_evento)
            
            #cursor.execute("INSERT INTO avisos (fecha_evento, LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO) VALUES (%s, %s, %s, %s, %s, %s)", (dia_evento,legajo,nombre, sector,titulo_evento,detalle_evento))
            cursor=conexion.connection.cursor()
            cursor.execute("INSERT INTO avisos (LEG, NOMBRE, SECTOR, fecha_evento, TITULO_EVENTO, DETALLE_EVENTO) VALUES (%s, %s, %s,%s,%s,%s)", (legajo,nombre,sector,dia_evento,titulo_evento,detalle_evento))
            conexion.connection.commit()

        return render_template('aviso_cargado_exitosamente.html')


@app.route('/Formulario_Reporte') #PERMITE INGRESAR DATOS PARA PERSONALIZAR EL FILTRO
def formulario_reporte():
    return render_template('Formulario_Filtro_Reporte.html')


@app.route('/Reporte', methods=['POST']) #PERMITE INGRESAR DATOS PARA PERSONALIZAR EL FILTRO
def tabla_reporte():
    if request.method=='POST': 
            legajo=request.form['legajo']
            dia_evento_desde=request.form['dia_evento_desde']
            dia_evento_hasta=request.form['dia_evento_hasta']

            if legajo=="":
                if dia_evento_desde == "":
                    if dia_evento_hasta =="":
                        # --- IF NRO 1 LEG="" + DESDE ="" + HASTA="" -----
                        cursor=conexion.connection.cursor()
                        cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%d-%m-%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos")
                        reporte_eventos=cursor.fetchall()
                    else:
                        # --- IF NRO 2 LEG="" + DESDE ="" + HASTA="DD-MM-YY" -----
                            cursor=conexion.connection.cursor()
                            cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%%d-%%m-%%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos  WHERE fecha_evento<%s", (dia_evento_hasta,))
                            reporte_eventos=cursor.fetchall()
                else:
                    if dia_evento_hasta=="":
                        # --- IF NRO 3 LEG="" + DESDE ="DD-MM-YY"  + HASTA "" -----
                        cursor=conexion.connection.cursor()
                        cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%%d-%%m-%%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos  WHERE fecha_evento>%s", (dia_evento_desde,))
                        reporte_eventos=cursor.fetchall()
                    else:
                        # --- IF NRO 4 LEG="" + DESDE ="DD-MM-YY"  + HASTA "DD-MM-YY" -----
                        cursor=conexion.connection.cursor()
                        cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%%d-%%m-%%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos  WHERE fecha_evento>%s AND fecha_evento<%s", (dia_evento_desde,dia_evento_hasta))
                        reporte_eventos=cursor.fetchall()
            else:
                if dia_evento_desde == "":
                    if dia_evento_hasta =="":
                        # --- IF NRO 5 LEG="#####" + DESDE ="" + HASTA="" -----
                        cursor=conexion.connection.cursor()
                        cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%%d-%%m-%%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos WHERE LEG=%s", (legajo,))
                        reporte_eventos=cursor.fetchall()
                    else:
                        # --- IF NRO 6 LEG="####" + DESDE ="" + HASTA="DD-MM-YY" -----
                            cursor=conexion.connection.cursor()
                            cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%%d-%%m-%%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos  WHERE LEG=%s AND fecha_evento<%s", (legajo,dia_evento_hasta))
                            reporte_eventos=cursor.fetchall()
                else:
                    if dia_evento_hasta=="":
                        # --- IF NRO 7 LEG="####" + DESDE ="DD-MM-YY"  + HASTA "" -----
                        cursor=conexion.connection.cursor()
                        cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%%d-%%m-%%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos WHERE LEG=%s AND fecha_evento>%s", (legajo,dia_evento_desde))
                        reporte_eventos=cursor.fetchall()
                    else:
                        # --- IF NRO 8 LEG="####" + DESDE ="DD-MM-YY"  + HASTA "DD-MM-YY" -----
                        cursor=conexion.connection.cursor()
                        cursor.execute("SELECT nro_aviso, fecha_carga, date_format(fecha_evento,'%%d-%%m-%%Y'), LEG, NOMBRE, SECTOR, TITULO_EVENTO, DETALLE_EVENTO FROM avisos  WHERE LEG=%s AND fecha_evento>%s AND fecha_evento<%s", (legajo,dia_evento_desde,dia_evento_hasta))
                        reporte_eventos=cursor.fetchall()
        
    return render_template('Reporte_avisos.html', eventos=reporte_eventos)



if __name__=='__main__':
    app.run(debug=True, port=5000)

