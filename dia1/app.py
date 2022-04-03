from flask import Flask, request
from datetime import datetime
from flask_cors import CORS


app=Flask(__name__)

CORS(app=app)

clientes=[
    {
        "nombre":"ronald",
        "pais":"peru",
        "edad":"29",
        "id":1,
        "organos":True,
        "casado":False
    }
]
 
@app.route('/')
def estado():
    hora_del_servidor=datetime.now()

    return{
        'status':True,
        'hour': hora_del_servidor.strftime('%d/%m/%Y %H:%M:%S')
    }

@app.route('/clientes', methods=['POST','GET'])
def obtener_clientes():
    # sólo puede ser llamado en cada controlador
    print(request.method)
    print(request.get_json())
    if request.method =='POST':
        data=request.get_json()

        data['id']=len(clientes) + 1

        clientes.append(data)
        data['nombre']

        return{
            'message':'cliente agregado exitosamente',
            'client': data
        }
    else:
        return{
            'message':'la lista de clientes',
            'client': clientes
        }

@app.route('/cliente/<int:id>',methods=['GET'])
def gestion_usuario(id):
    print(id)

    resultado=None
    for cliente in clientes:
        if cliente.get('id')==id:
            resultado=cliente
            break
    if (resultado is not None):
        return resultado
    else:
        return({
            'message': 'el usuario a buscar no se encontró'
        }, 404)
    


    return{
        'id':id
    } 



app.run(debug=True)
