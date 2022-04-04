from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.jinja', nombre='Eduardo', dia='jueves', integrantes=[
        'foca',
        'lapagol',
        'palion',
        'rayo advincula'
        ], usuario={
            'nombre':"juan",
            'direccion':'las piedritas 105',
            'edad': '40'
        }, selecciones=[{
            'nombre':'Bolivia',
            'clasificado': False
        },{
            'nombre': 'Brasil',
            'clasificado': True
        },{
            'nombre':'Chile',
            'clasificado':False
        },{
            'nombre': 'Peru',
            'timado': True
        }])

if(__name__=='__main__'):
    app.run(debug=True)