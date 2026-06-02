from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Esto busca el archivo index.html en la carpeta 'templates'
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/carrito')
def carrito():
    return render_template('carrito.html')

@app.route('/consola')
def consola():
    return render_template('consola.html')

@app.route('/accesorios')
def accesorios():
    return render_template('accesorios.html')

@app.route('/coleccionables')
def coleccionables():
    return render_template('coleccionables.html')

@app.route('/lanzamientos')
def lanzamientos():
    return render_template('lanzamientos.html')

# También necesitarás estas rutas para los sub-enlaces de tus archivos:
@app.route('/PS5')
def PS5():
    return render_template('PS5.html')

@app.route('/PS4')
def PS4():
    return render_template('PS4.html')

@app.route('/XBOX')
def XBOX():
    return render_template('XBOX.html')

@app.route('/NintendoSwitch')
def NintendoSwitch():
    return render_template('NintendoSwitch.html')

@app.route('/PC')
def PC():
    return render_template('PC.html')

if __name__ == '__main__':
    app.run(debug=True)
