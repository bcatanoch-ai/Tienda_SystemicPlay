from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
import os
app.secret_key = 'clave_secreta_super_segura'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL')
    or 'sqlite:///tienda.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# --- MODELOS ---
class Juego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    img = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=10)

# Nueva clase User para que se guarde en la BD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Nueva clase para registrar las compras
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100))
    producto = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)        # Cantidad comprada
    total = db.Column(db.Float)             # Precio Total (precio * cantidad)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- LISTAS GLOBALES ---
# PARA VISTA PS5
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

accesorios_generales = [
    {"nombre": "PLAYSTATION PORTAL PS5", "categoria": "Reproductor remoto", "precio": "S/ 1100.00", "img": "accesorio1.jpg"},
    {"nombre": "MANDO DUALSENSE PS5 GALATIC PURPLE", "categoria": "Mando DualSense", "precio": "S/ 255.00", "img": "accesorio2.jpg"},
    {"nombre": "PS5 PLAYSTATION PULSE ELITE AUDIFONOS", "categoria": "Audífono PS5", "precio": "S/ 729.90", "img": "accesorio3.jpg"},
    {"nombre": "MANDO INALÁMBRICO XBOX ONE", "categoria": "Mando Xbox", "precio": "S/ 299.90", "img": "accesorio4.jpg"},
    {"nombre": "ESTUCHE RÍGIDO DE VIAJERO NINTENDO SWITCH 2", "categoria": "Accesorio Switch", "precio": "S/ 89.90", "img": "accesorio5.jpg"},
    {"nombre": "JOY-CON NINTENDO SWITCH 2", "categoria": "Joy-cons", "precio": "S/ 249.90", "img": "accesorio6.jpg"},
    {"nombre": "COMBO LOGITECH MK270 TECLADO Y MOUSE", "categoria": "Logitech", "precio": "S/ 129.00", "img": "accesorio7.jpg"},
    {"nombre": "LOGITECH G321 LIGHTSPEED AUDÍFONOS", "categoria": "Auriculares", "precio": "S/ 285.00", "img": "accesorio8.jpg"}
]

coleccionables_lista = [
    {"nombre": "FIGURA BANDAI GOKU ULTRA INSTINTO", "categoria": "Figuras de Acción", "precio": "S/ 99.90", "img": "coleccionable1.jpg"},
    {"nombre": "FIGURA BANDAI ONE PIECE DXF TEACH", "categoria": "Figura de Acción", "precio": "S/ 99.90", "img": "coleccionable2.jpg"},
    {"nombre": "FIGURA BANDAI ONE PIECE MONKEY D. LUFFY", "categoria": "Figura de Acción", "precio": "S/ 119.00", "img": "coleccionable3.jpg"},
    {"nombre": "FIGURA STAR WARS CHEWBACA", "categoria": "Figura de Acción", "precio": "S/ 199.90", "img": "coleccionable4.jpg"},
    {"nombre": "FUNKO POP MARVEL SPIDER-MAN", "categoria": "Funko Pop", "precio": "S/ 79.00", "img": "coleccionable5.jpg"},
    {"nombre": "FUNKO POP LIONEL MESSI N°1", "categoria": "Funko Pop", "precio": "S/ 89.00", "img": "coleccionable6.jpg"},
    {"nombre": "FIGURA SUPER MARIO YOSHI", "categoria": "Funko Pop", "precio": "S/ 299.00", "img": "coleccionable7.jpg"},
    {"nombre": "POKÉMON TCG - CAJA DE ENTRENADOR", "categoria": "Funko Pop", "precio": "S/ 279.00", "img": "coleccionable8.jpg"}
]


with app.app_context():
    db.create_all()
    if not Juego.query.first():
        print("Migrando...")
        # Incluye todas tus listas globales aquí
        datos_a_migrar = [
            (juegos_ps5, 'ps5'), (juegos_ps4, 'ps4'), 
            (juegos_xbox, 'xbox'), (juegos_nintendo, 'nintendo'),
            (juegos_pc, 'pc'), # Cambiado a 'juegos_pc'
            (accesorios_generales, 'accesorios'),
            (coleccionables_lista, 'coleccionables')
        ]
    if not User.query.filter_by(email='admin@systemic.com').first():
        admin = User(
                        nombre='Admin',
                        apellido='Sistema',
                        email='admin@systemic.com',
                        password='123456'
                     )
        db.session.add(admin)
        db.session.commit()    
        
        for lista, categoria in datos_a_migrar:
            for item in lista:
                nuevo = Juego(nombre=item['nombre'], precio=item['precio'], categoria=categoria, img=item['img'])
                db.session.add(nuevo)
        db.session.commit()

# --- RUTAS DE AUTENTICACIÓN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("El correo no está registrado.")
            return render_template('login.html')

        if user.password != password:
            flash("Contraseña incorrecta.")
            return render_template('login.html')

        login_user(user)
        flash("Bienvenido nuevamente.")
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash("Este correo ya está registrado.")
            return redirect(url_for('login'))
        nuevo_usuario = User(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=password
            )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.") # Este aviso saldrá en el login
    return redirect(url_for('login'))

# --- ADMINISTRACIÓN Y CRUD ---
@app.route('/panel-admin')
@login_required
def panel_admin():
    if current_user.email != 'admin@systemic.com':
        flash("Acceso denegado.")
        return redirect(url_for('home'))
    juegos = Juego.query.all()
    clientes = User.query.all()
    historial_compras = Compra.query.all()
    inventario = {cat: Juego.query.filter_by(categoria=cat).count() for cat in ['ps5', 'ps4', 'xbox', 'nintendo', 'pc', 'accesorios', 'coleccionables']}
    return render_template('admin.html', juegos=juegos, total_productos=len(juegos), inventario=inventario, clientes=clientes, compras=historial_compras)

@app.route('/agregar-juego', methods=['POST'])
@login_required
def agregar_juego():
    nuevo = Juego(nombre=request.form.get('nombre'),
                  precio=request.form.get('precio'),
                  stock=request.form.get('stock'),
                  img=request.form.get('img'),
                  categoria=request.form.get('categoria'))
    db.session.add(nuevo)
    db.session.commit()
    flash(f"Producto {nuevo.nombre} agregado correctamente.")
    return redirect(url_for('panel_admin'))

@app.route('/actualizar-juego', methods=['POST'])
@login_required
def actualizar_juego():
    juego = Juego.query.get(int(request.form.get('id')))
    if juego:
        juego.nombre = request.form.get('nombre');
        juego.precio = request.form.get('precio');
        juego.stock = request.form.get('stock');
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
            
            # Limpiar precio: quita "S/ " y convierte a float
            precio_limpio = float(juego.precio.replace('S/', '').replace(' ', ''))
            total_compra = precio_limpio * item['cantidad']
            
            # Guardamos incluyendo cantidad y total
            nueva_compra = Compra(
                user_email=current_user.email, 
                producto=juego.nombre,
                cantidad=item['cantidad'],
                total=total_compra
            )
            db.session.add(nueva_compra)
        else:
            return {"error": f"Stock insuficiente para {item['nombre']}"}, 400
            
    db.session.commit()
    return {"mensaje": "Compra exitosa"}, 200

# --- RUTAS DE TIENDA Y VISTAS ---
@app.route('/')
def home(): return render_template('index.html')

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')
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
    # Buscamos en la BD los que tengan la categoria 'accesorios'
    accesorios_db = Juego.query.filter_by(categoria='accesorios').all()
    return render_template('accesorios.html', accesorios=accesorios_db)

@app.route('/coleccionables')
def coleccionables():
    # Consulta a la base de datos filtrando por la categoría 'coleccionables'
    items = Juego.query.filter_by(categoria='coleccionables').all()
    return render_template('coleccionables.html', coleccionables=items)

@app.route('/lanzamientos')
def lanzamientos():
    return render_template('lanzamientos.html')

# --- RUTA PS5 ---
@app.route('/PS5')
def PS5():
    juegos_db = Juego.query.filter_by(categoria='ps5').all()
    return render_template('PS5.html', juegos=juegos_db)

# --- RUTA PS4 ---
@app.route('/PS4')
def PS4():
    juegos_db = Juego.query.filter_by(categoria='ps4').all()
    return render_template('PS4.html', juegos=juegos_db)

# --- RUTA XBOX ---
@app.route('/XBOX')
def XBOX():
    juegos_db = Juego.query.filter_by(categoria='xbox').all()
    return render_template('XBOX.html', juegos=juegos_db)

# --- RUTA NINTENDO SWITCH ---
@app.route('/NintendoSwitch')
def NintendoSwitch():
    juegos_db = Juego.query.filter_by(categoria='nintendo').all()
    return render_template('NintendoSwitch.html', juegos=juegos_db)

# --- RUTA PC ---
@app.route('/PC')
def PC():
    juegos_db = Juego.query.filter_by(categoria='juegos_pc').all()
    return render_template('PC.html', juegos_pc=juegos_pc)


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

@app.context_processor
def inject_user(): return dict(current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
