from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# --- MODELOS (La estructura de tu nueva BD) ---
class Juego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    img = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    
# 1. PRIMERO definimos la clase User
class User(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email

# 2. LUEGO inicializamos la base de datos
usuarios_db = {}

# 3. Y FINALMENTE creamos el objeto admin usando la clase ya definida
admin = User(id='admin@systemic.com', nombre='Admin', email='admin@systemic.com')
admin.password = '123456' 
usuarios_db['admin@systemic.com'] = admin


# --- LISTAS GLOBALES ---
# PARA VISTA PS5
consolas_ps5 = [
    {"nombre": "PlayStation 5", "precio": "S/ 2,199.99", "img": "PlayStation5_1.jpg"},
    {"nombre": "PlayStation 5 Slim", "precio": "S/ 2,799.99", "img": "PlayStation5_2.jpg"},
    {"nombre": "PlayStation 5 Pro", "precio": "S/ 3,999.99", "img": "PlayStation5_3.webp"},
    {"nombre": "PlayStation 5 Pro 30th Anniversary", "precio": "S/ 5,999.99", "img": "PlayStation5_4.png"}
]

juegos_ps5 = [
    {"id": 1,"nombre": "Marvel's Spider-Man 2", "precio": "S/ 279.90", "img": "PlayStation5_juego1.png"},
    {"id": 2,"nombre": "God of War Ragnarök", "precio": "S/ 229.90", "img": "PlayStation5_juego2.png"},
    {"id": 3,"nombre": "Horizon Forbidden West", "precio": "S/ 179.90", "img": "PlayStation5_juego3.png"},
    {"id": 4,"nombre": "Elden Ring", "precio": "S/ 239.90", "img": "PlayStation5_juego4.png"},
    {"id": 5,"nombre": "Final Fantasy VII Rebirth", "precio": "S/ 279.90", "img": "PlayStation5_juego5.png"},
    {"id": 6,"nombre": "Demon's Souls", "precio": "S/ 189.90", "img": "PlayStation5_juego6.png"},
    {"id": 7,"nombre": "Ratchet & Clank: Rift Apart", "precio": "S/ 179.90", "img": "PlayStation5_juego7.png"},
    {"id": 8,"nombre": "Gran Turismo 7", "precio": "S/ 229.90", "img": "PlayStation5_juego8.png"}
]

# PARA VISTA PS4
consolas_ps4 = [
    {"nombre": "PlayStation 4 Fat", "precio": "S/ 849.99", "img": "PlayStation4_1.png"},
    {"nombre": "PlayStation 4 Fat(MATE)", "precio": "S/ 949.99", "img": "PlayStation4_2.png"},
    {"nombre": "PlayStation 4 Slim", "precio": "S/ 1,299.99", "img": "PlayStation4_3.png"},
    {"nombre": "PlayStation 4 Pro", "precio": "S/ 1,699.99", "img": "PlayStation4_4.png"}
]

juegos_ps4 = [
    {"id": 1,"nombre": "The Last of Us Part II", "precio": "S/ 149.90", "img": "PlayStation4_juego1.png"},
    {"id": 2,"nombre": "Ghost of Tsushima", "precio": "S/ 159.90", "img": "PlayStation4_juego2.png"},
    {"id": 3,"nombre": "Marvel's Spider-Man", "precio": "S/ 119.90", "img": "PlayStation4_juego3.jpg"},
    {"id": 4,"nombre": "Bloodborne", "precio": "S/ 79.90", "img": "PlayStation4_juego4.png"},
    {"id": 5,"nombre": "The Witcher 3: Wild Hunt", "precio": "S/ 99.90", "img": "PlayStation4_juego5.png"},
    {"id": 6,"nombre": "God of War (2018)", "precio": "S/ 79.90", "img": "PlayStation4_juego6.png"},
    {"id": 7,"nombre": "Uncharted 4: A Thief's End", "precio": "S/ 79.90", "img": "PlayStation4_juego7.png"},
    {"id": 8,"nombre": "Horizon Zero Dawn", "precio": "S/ 79.90", "img": "PlayStation4_juego8.png"}
]

# PARA VISTA XBOX
consolas_xbox = [
    {"nombre": "Xbox One S", "precio": "S/ 849.99", "img": "Xbox_1.png"},
    {"nombre": "Xbox One X", "precio": "S/ 1,099.90", "img": "Xbox_2.png"},
    {"nombre": "Xbox Series S", "precio": "S/ 1,399.99", "img": "Xbox_3.png"},
    {"nombre": "Xbox Series X", "precio": "S/ 2,499.99", "img": "Xbox_4.png"}
]

juegos_xbox = [
    {"id": 1,"nombre": "Halo Infinite", "precio": "S/ 199.90", "img": "Xbox_juego1.png"},
    {"id": 2,"nombre": "Forza Horizon 5", "precio": "S/ 219.90", "img": "Xbox_juego2.png"},
    {"id": 3,"nombre": "Gears 5", "precio": "S/ 119.90", "img": "Xbox_juego3.png"},
    {"id": 4,"nombre": "Starfield", "precio": "S/ 259.90", "img": "Xbox_juego4.png"},
    {"id": 5,"nombre": "Sea of Thieves", "precio": "S/ 139.90", "img": "Xbox_juego5.png"},
    {"id": 6,"nombre": "Microsoft Flight Simulator", "precio": "S/ 219.90", "img": "Xbox_juego6.png"},
    {"id": 7,"nombre": "State of Decay 2", "precio": "S/ 99.90", "img": "Xbox_juego7.png"},
    {"id": 8,"nombre": "Psychonauts 2", "precio": "S/ 159.90", "img": "Xbox_juego8.png"}
]

# PARA VISTA NintendoSwitch
consolas_nintendo = [
    {"nombre": "Nintendo Switch Lite", "precio": "S/ 799.90", "img": "NintendoSwitch_1.png"},
    {"nombre": "Nintendo Switch (V1)", "precio": "S/ 949.90", "img": "NintendoSwitch_2.png"},
    {"nombre": "Nintendo Switch (V2)", "precio": "S/ 1,199.90", "img": "NintendoSwitch_3.png"},
    {"nombre": "Nintendo Switch OLED", "precio": "S/ 1,449.90", "img": "NintendoSwitch_4.png"}
]

juegos_nintendo = [
    {"id": 1,"nombre": "Zelda: Tears of the Kingdom", "precio": "S/ 249.90", "img": "NintendoSwitch_juego1.png"},
    {"id": 2,"nombre": "Super Mario Odyssey", "precio": "S/ 209.90", "img": "NintendoSwitch_juego2.png"},
    {"id": 3,"nombre": "Mario Kart 8 Deluxe", "precio": "S/ 209.90", "img": "NintendoSwitch_juego3.png"},
    {"id": 4,"nombre": "Super Smash Bros. Ultimate", "precio": "S/ 219.90", "img": "NintendoSwitch_juego4.png"},
    {"id": 5,"nombre": "Animal Crossing: New Horizons", "precio": "S/ 209.90", "img": "NintendoSwitch_juego5.png"},
    {"id": 6,"nombre": "Pokémon Scarlet / Violet", "precio": "S/ 199.90", "img": "NintendoSwitch_juego6.png"},
    {"id": 7,"nombre": "Metroid Dread", "precio": "S/ 189.90", "img": "NintendoSwitch_juego7.png"},
    {"id": 8,"nombre": "Splatoon 3", "precio": "S/ 199.90", "img": "NintendoSwitch_juego8.png"}
]

#PARA VISTA PC
pcs = [
    {"nombre": "PC Gamer Entry", "precio": "S/ 1,800.00", "img": "PC_1.png"},
    {"nombre": "PC Gamer Mid Range", "precio": "S/ 3,200.00", "img": "PC_2.png"},
    {"nombre": "PC Gamer High End", "precio": "S/ 5,500.00", "img": "PC_3.png"},
    {"nombre": "PC Gamer Ultra", "precio": "S/ 9,500.00", "img": "PC_4.png"}
]

juegos_pc = [
    {"id": 1,"nombre": "Cyberpunk 2077", "precio": "S/ 159.90", "img": "PC_juegos1.png"},
    {"id": 2,"nombre": "Dead Island 2", "precio": "S/ 140.00", "img": "PC_juegos2.png"},
    {"id": 3,"nombre": "Grand Theft Auto V", "precio": "S/ 105.00", "img": "PC_juegos3.jpg"},
    {"id": 4,"nombre": "Red Dead Redemption 2", "precio": "S/ 199.90", "img": "PC_juegos4.jpg"},
    {"id": 5,"nombre": "Helldivers 2", "precio": "S/ 150.00", "img": "PC_juegos5.png"},
    {"id": 6,"nombre": "Palworld", "precio": "S/ 89.00", "img": "PC_juegos6.png"},
    {"id": 7,"nombre": "Project Zomboid", "precio": "S/ 45.00", "img": "PC_juegos7.png"},
    {"id": 8,"nombre": "Stardew Valley", "precio": "S/ 40.00", "img": "PC_juegos8.png"}
]

accesorios_pc = [
    {"nombre": "ASUS Dual GeForce RTX 5060 Ti", "precio": "S/ 1,499.90", "img": "PC_accesorio1.jpg"},
    {"nombre": "Samsung SSD 9100 PRO 1TB", "precio": "S/ 949.90", "img": "PC_accesorio2.jpg"},
    {"nombre": "Epson EcoTank ET-4950", "precio": "S/ 1,399.90", "img": "PC_accesorio3.jpg"},
    {"nombre": "Samsung 49\" Odyssey OLED", "precio": "S/ 3,099.90", "img": "PC_accesorio4.jpg"},
    {"nombre": "Cable HDMI 4K 60Hz", "precio": "S/ 19.90", "img": "PC_accesorio5.jpg"},
    {"nombre": "Epson Lifestudio Pop Plus 4K", "precio": "S/ 2,579.90", "img": "PC_accesorio6.jpg"},
    {"nombre": "Turtle Beach Wireless Controller", "precio": "S/ 219.90", "img": "PC_accesorio7.jpg"},
    {"nombre": "Fuente 1000W 80+ Gold", "precio": "S/ 309.90", "img": "PC_accesorio8.jpg"}
]


with app.app_context():
    db.create_all()
    
    # Verificamos si la base de datos tiene algo
    if not Juego.query.first():
        print("Migrando listas originales a la base de datos...")
        
        # Diccionario para automatizar la migración de todas las categorías
        todas_las_listas = {
            'ps5': juegos_ps5,
            'ps4': juegos_ps4,
            'xbox': juegos_xbox,
            'nintendo': juegos_nintendo,
            'pc': juegos_pc
        }
        
        for categoria, lista in todas_las_listas.items():
            for item in lista:
                nuevo = Juego(
                    nombre=item['nombre'], 
                    precio=item['precio'], 
                    categoria=categoria, 
                    img=item['img']
                )
                db.session.add(nuevo)
        
        db.session.commit()
        print("Migración completada exitosamente.")


@login_manager.user_loader
def load_user(user_id):
    return usuarios_db.get(user_id)

# --- RUTAS DE AUTENTICACIÓN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = usuarios_db.get(email)
        
        if user:
            # VALIDACIÓN DE CONTRASEÑA
            if user.password == password:
                login_user(user)
                
                # --- AQUÍ ESTABA EL ERROR DE SANGRÍA ---
                if email == 'admin@systemic.com': 
                    flash("Bienvenido administrador.")
                    return redirect(url_for('home')) 
                # ----------------------------------------
                
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta.")
                return redirect(url_for('login'))
        else:
            flash("Correo no registrado. Crea una cuenta primero")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/panel-admin')
@login_required
def panel_admin():
    if current_user.email != 'admin@systemic.com':
        flash("Acceso denegado.")
        return redirect(url_for('home'))
    
    # Obtenemos todos los juegos de la base de datos
    juegos = Juego.query.all()
    
    # Contamos basándonos en la base de datos
    total_productos = len(juegos)
    inventario = {
        "PS5": Juego.query.filter_by(categoria='ps5').count(),
        "PS4": Juego.query.filter_by(categoria='ps4').count(),
        "XBOX": Juego.query.filter_by(categoria='xbox').count(),
        "Nintendo": Juego.query.filter_by(categoria='nintendo').count(),
        "PC": Juego.query.filter_by(categoria='pc').count()
    }
    
    return render_template('admin.html', 
                           juegos=juegos, 
                           total_productos=total_productos,
                           inventario=inventario)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password') # <-- Capturamos la contraseña
        
        if email in usuarios_db:
            flash("Este correo ya está registrado.")
            return redirect(url_for('login'))
            
        # Guardamos el objeto User con la contraseña (o un atributo extra)
        nuevo_usuario = User(id=email, nombre=nombre, email=email)
        nuevo_usuario.password = password # Guardamos la contraseña en el objeto
        usuarios_db[email] = nuevo_usuario
        
        flash("¡Cuenta creada exitosamente!")
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.") # Este aviso saldrá en el login
    return redirect(url_for('login'))

@app.context_processor
def inject_user():
    return dict(current_user=current_user)

#RUTAS DE TODAS LAS VISTAS DE LA PÁGINA
@app.route('/')
def home():
    # Esto busca el archivo index.html en la carpeta 'templates'
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '') # Captura lo que escribió el usuario
    # Filtra juegos cuyo nombre contenga la búsqueda (case-insensitive)
    resultados = Juego.query.filter(Juego.nombre.ilike(f'%{query}%')).all()
    
    return render_template('resultados_busqueda.html', resultados=resultados, query=query)

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
# PARA AGREGAR JUEGOS:
@app.route('/agregar-juego', methods=['POST'])
@login_required
def agregar_juego():
    categoria = request.form.get('categoria')
    
    nuevo_juego = Juego(
        nombre=request.form.get('nombre'),
        precio=request.form.get('precio'),
        stock=request.form.get('stock'),
        img=request.form.get('img'),
        categoria=categoria
    )
    
    db.session.add(nuevo_juego)
    db.session.commit()
    
    flash(f"Producto {nuevo_juego.nombre} agregado correctamente.")
    return redirect(url_for('panel_admin'))

#PARA ELIMINAR Y EDITAR JUEGOS:
# Función auxiliar para buscar el juego y su lista contenedora
def buscar_juego(id_juego):
    listas = [juegos_ps5, juegos_ps4, juegos_xbox, juegos_nintendo, juegos_pc]
    for lista in listas:
        for juego in lista:
            if juego.get('id') == id_juego:
                return juego, lista
    return None, None

@app.route('/actualizar-juego', methods=['POST'])
@login_required
def actualizar_juego():
    id_juego = int(request.form.get('id'))
    juego = Juego.query.get(id_juego)
    
    if juego:
        juego.nombre = request.form.get('nombre')
        juego.precio = request.form.get('precio')
        juego.stock = request.form.get('stock')
        juego.img = request.form.get('img')
        db.session.commit()
        flash(f"Juego '{juego.nombre}' actualizado.")
    else:
        flash("Error: Juego no encontrado.")
        
    return redirect(url_for('panel_admin'))

@app.route('/eliminar-juego/<int:id>')
@login_required
def eliminar_juego(id):
    juego = Juego.query.get(id)
    if juego:
        db.session.delete(juego)
        db.session.commit()
        flash(f"Juego '{juego.nombre}' eliminado.")
    else:
        flash("Error: No se pudo eliminar el juego.")
    return redirect(url_for('panel_admin'))


@app.route('/finalizar-compra', methods=['POST'])
@login_required
def finalizar_compra():
    # Recibimos la lista de productos desde el JavaScript
    productos_comprados = request.json
    
    for item in productos_comprados:
        # Buscamos el producto por su nombre (o ID si lo tuvieras)
        juego = Juego.query.filter_by(nombre=item['nombre']).first()
        if juego and juego.stock >= item['cantidad']:
            juego.stock -= item['cantidad']
        else:
            return {"error": f"Stock insuficiente para {item['nombre']}"}, 400
            
    db.session.commit()
    return {"mensaje": "Compra exitosa"}, 200


# --- RUTA PS5 ---
@app.route('/PS5')
def PS5():
    juegos_db = Juego.query.filter_by(categoria='ps5').all()
    return render_template('PS5.html', consolas=consolas_ps5, juegos=juegos_db)

# --- RUTA PS4 ---
@app.route('/PS4')
def PS4():
    juegos_db = Juego.query.filter_by(categoria='ps4').all()
    return render_template('PS4.html', consolas=consolas_ps4, juegos=juegos_db)

# --- RUTA XBOX ---
@app.route('/XBOX')
def XBOX():
    juegos_db = Juego.query.filter_by(categoria='xbox').all()
    return render_template('XBOX.html', consolas=consolas_xbox, juegos=juegos_db)

# --- RUTA NINTENDO SWITCH ---
@app.route('/NintendoSwitch')
def NintendoSwitch():
    juegos_db = Juego.query.filter_by(categoria='nintendo').all()
    return render_template('NintendoSwitch.html', consolas=consolas_nintendo, juegos=juegos_db)

# --- RUTA PC ---
@app.route('/PC')
def PC():
    juegos_db = Juego.query.filter_by(categoria='pc').all()
    return render_template('PC.html', lista_pcs=pcs, juegos_pc=juegos_db, accesorios_pc=accesorios_pc)

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
