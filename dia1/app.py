from flask import Flask, request
from datetime import datetime

app=Flask(__name__)

clientes=[]

@app.route('/')
def estado():
    hora_del_servidor=datetime.now()

    return{
        'status':True,
        'hour': hora_del_servidor.strftime('%d/%m/%Y %H:%M:%S')
    }

@app.route('/clientes', methods=['POST'])
def obtener_clientes():
    # sólo puede ser llamado en cada controlador
    print(request.method)
    print(request.get_json())
    data=request.get_json()
    clientes.append(data)

    return{
        'message':'cliente agregado exitosamente',
        'client': data
    }


app.run(debug=True)