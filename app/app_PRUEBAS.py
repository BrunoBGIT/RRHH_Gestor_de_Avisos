from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mysqldb import MySQL
from flask.templating import render_template

app=Flask(__name__)

# CONEXION MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='bruno'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='rrhh_avisos'

conexion = MySQL(app) 


@app.route('/prueba')
def hacer_prueba():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM nomina ORDER BY nombre ASC"
        cursor.execute(sql)
        cursos=cursor.fetchall()
        #print(cursos)
        data['cursos']=cursos
        data['mensaje']='Exito'

    except Exception as ex:
        data['mensaje']='Error al intentar hacer la consulta SQL'
    return jsonify(data)


if __name__=='__main__':
    app.run(debug=True, port=5000)

