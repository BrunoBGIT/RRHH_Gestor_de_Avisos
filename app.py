from flask import Flask, render_template, request
from flask.templating import render_template

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='rrhh_avisos'
#mysql=MySQL()

@app.route('/')
def principal():
    return render_template('index.html') 

    


if __name__=='__main__':
    app.run(debug=True, port=5017)

