from flask import Flask
from datetime import datetime

# la variabble __name__ > muestra si el archivo es el archivo raiz o principal del proyecto
app= Flask(__name__)

@app.route('/')

def inicial():
    print('me llamaron')
    return 'bienvenido a mi API 🚀 ' # tecla Windows + . para insertar emogis

@app.route('/api/info')
def info_app():
    return{
        'fecha': datetime.now().strftime('%Y %m %d %HH:%MM:%S')
    }

# con app.run() vamos a inicializar nuestro servidor flask
app.run(debug=True)