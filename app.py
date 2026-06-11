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

# Acá agregaré los .html de las vista de juegos, accesorios y coleccionables
@app.route('/Diablo')
def Diablo():
    return render_template('Diablo.html')

@app.route('/Cod')
def Cod():
    return render_template('Cod.html')

@app.route('/Motogp')
def Motogp():
    return render_template('Motogp.html')

@app.route('/ResidentEvil')
def ResidentEvil():
    return render_template('ResidentEvil.html')

@app.route('/NoManSky')
def NoManSky():
    return render_template('NoManSky.html')

@app.route('/Wwe')
def Wwe():
    return render_template('Wwe.html')

@app.route('/Uncharted')
def Uncharted():
    return render_template('Uncharted.html')

@app.route('/DaysToDie')
def DaysToDie():
    return render_template('DaysToDie.html')

@app.route('/SuperSmash')
def SuperSmash():
    return render_template('SuperSmash.html')

@app.route('/AlanWake')
def AlanWake():
    return render_template('AlanWake.html')

@app.route('/MortalKombat')
def MortalKombat():
    return render_template('MortalKombat.html')

@app.route('/NintendoSwitch2')
def NintendoSwitch2():
    return render_template('NintendoSwitch2.html')

@app.route('/PlayStationSpiderMan')
def PlayStationSpiderMan():
    return render_template('PlayStationSpiderMan.html')

@app.route('/ForzaHorizon')
def ForzaHorizon():
    return render_template('ForzaHorizon.html')

@app.route('/PortalPs5')
def PortalPs5():
    return render_template('PortalPs5.html')

@app.route('/MandoPs5')
def MandoPs5():
    return render_template('MandoPs5.html')

@app.route('/AudifonoPs5')
def AudifonoPs5():
    return render_template('AudifonoPs5.html')

@app.route('/MandoXbox')
def MandoXbox():
    return render_template('MandoXbox.html')

@app.route('/EstucheNs')
def EstucheNs():
    return render_template('EstucheNs.html')

@app.route('/JoyConNs')
def JoyConNs():
    return render_template('JoyConNs.html')

@app.route('/ComboLogitech')
def ComboLogitech():
    return render_template('ComboLogitech.html')

@app.route('/AudifonoLogitech')
def AudifonoLogitech():
    return render_template('AudifonoLogitech.html')

@app.route('/FiguraGoku')
def FiguraGoku():
    return render_template('FiguraGoku.html')

@app.route('/FiguraTeach')
def FiguraTeach():
    return render_template('FiguraTeach.html')

@app.route('/FiguraLuffy')
def FiguraLuffy():
    return render_template('FiguraLuffy.html')

@app.route('/FiguraChewbaca')
def FiguraChewbaca():
    return render_template('FiguraChewbaca.html')

@app.route('/FiguraSpiderman')
def FiguraSpiderman():
    return render_template('FiguraSpiderman.html')

@app.route('/FiguraMessi')
def FiguraMessi():
    return render_template('FiguraMessi.html')

@app.route('/FiguraYoshi')
def FiguraYoshi():
    return render_template('FiguraYoshi.html')

@app.route('/FiguraPokemon')
def FiguraPokemon():
    return render_template('FiguraPokemon.html')

if __name__ == '__main__':
    app.run(debug=True)
