/* --- CARRUSEL UNIVERSAL (Index y Diablo.html) --- */
function cambiarSlide(direccion, selectorContenedor) {
    const contenedor = document.querySelector(selectorContenedor);
    
    // CORRECCIÓN: Busca SOLO dentro del contenedor padre
    const slides = contenedor.querySelectorAll('.slide'); 
    
    let indice = parseInt(contenedor.dataset.indice) || 0;
    
    // Aplicamos el módulo con la cantidad real de slides de este contenedor
    indice = (indice + direccion + slides.length) % slides.length;
    
    contenedor.dataset.indice = indice;
    contenedor.style.transform = `translateX(-${indice * 100}%)`;
}

document.addEventListener("DOMContentLoaded", () => {
    // 2. Estado Global
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    // 3. Selección de Productos (Abarca todos los casos)
    const productos = document.querySelectorAll('.tarjeta_juego, .producto, .producto_item, .card-producto');

    productos.forEach((juego) => {
        // Solo creamos el botón si no existe uno manualmente en el HTML
        let boton = juego.querySelector(".btn-carrito");
        
        if (!boton) {
            juego.style.position = "relative";
            boton = document.createElement("button");
            boton.classList.add("btn-carrito");
            boton.innerHTML = `<i class="fa-solid fa-cart-shopping"></i>`;
            
            // Estilos básicos (Considera pasar esto a un archivo CSS)
            Object.assign(boton.style, {
                position: "absolute", top: "10px", right: "10px", width: "40px", height: "40px",
                borderRadius: "50%", background: "#00bfff", color: "white", border: "none",
                cursor: "pointer", opacity: "0", transition: ".3s", zIndex: "1000"
            });

            juego.appendChild(boton);

            juego.addEventListener("mouseenter", () => boton.style.opacity = "1");
            juego.addEventListener("mouseleave", () => boton.style.opacity = "0");
        }

        // Evento único para agregar al carrito
        boton.addEventListener("click", (e) => {
            e.preventDefault();
            
            const nombre = juego.querySelector("h3, h2, .titulo_juego, .titulo")?.textContent.trim() || "Producto";
            const precioTexto = juego.querySelector(".precio_ahora, .precio")?.textContent || "0";
            const precio = parseFloat(precioTexto.replace(/[^\d.]/g, "")); // Limpia cualquier moneda (S/, $, etc)
            const imagen = juego.querySelector("img")?.src || "";

            const existe = carrito.find(item => item.nombre === nombre);
            if (existe) {
                existe.cantidad++;
            } else {
                carrito.push({ nombre, precio, imagen, cantidad: 1 });
            }

            actualizarYGuardar();
            alert(`${nombre} agregado al carrito`);
        });
    });

    // 4. Funciones de Interfaz
    function actualizarYGuardar() {
        localStorage.setItem("carrito", JSON.stringify(carrito));
        mostrarCarrito();
    }

    function mostrarCarrito() {
        const contenedor = document.getElementById("items-carrito");
        if (!contenedor) return;

        contenedor.innerHTML = "";
        let total = 0;

        carrito.forEach((producto, index) => {
            const subtotal = producto.precio * producto.cantidad;
            total += subtotal;

            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td style="display:flex;align-items:center;gap:10px;">
                    <img src="${producto.imagen}" width="70" style="border-radius:10px;">
                    ${producto.nombre}
                </td>
                <td>S/ ${producto.precio.toFixed(2)}</td>
                <td>${producto.cantidad}</td>
                <td>S/ ${subtotal.toFixed(2)}</td>
                <td>
                    <button class="eliminar-producto" data-index="${index}" style="background:red; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">
                        Eliminar
                    </button>
                </td>
            `;
            contenedor.appendChild(fila);
        });

        const subtotalEl = document.getElementById("subtotal-valor");
        const totalEl = document.getElementById("total-valor");
        if (subtotalEl) subtotalEl.textContent = `S/ ${total.toFixed(2)}`;
        if (totalEl) totalEl.textContent = `S/ ${total.toFixed(2)}`;

        // Eventos para eliminar
        document.querySelectorAll(".eliminar-producto").forEach(btn => {
            btn.onclick = () => {
                carrito.splice(btn.dataset.index, 1);
                actualizarYGuardar();
            };
        });
    }

    const btnAgregarDetalle = document.querySelector('.btn-carrito'); 

    if (btnAgregarDetalle && !btnAgregarDetalle.closest('.tarjeta_juego, .producto')) {
        btnAgregarDetalle.addEventListener('click', (e) => {
            e.preventDefault();

            // Capturamos la info desde la página actual
            const nombre = document.querySelector('.nombre-juego')?.textContent.trim() || "Juego";
            const precioTexto = document.querySelector('.precio')?.textContent || "0";
            const precio = parseFloat(precioTexto.replace(/[^\d.]/g, ""));
            const imagen = document.querySelector('img')?.src || "";
            const cantidadInput = document.querySelector('.input-valor');
            const cantidad = cantidadInput ? parseInt(cantidadInput.value) : 1;

            // Agregamos al carrito usando la lógica que ya tienes
            const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
            const existe = carrito.find(item => item.nombre === nombre);
            
            if (existe) {
                existe.cantidad += cantidad;
            } else {
                carrito.push({ nombre, precio, imagen, cantidad });
            }

            localStorage.setItem("carrito", JSON.stringify(carrito));
            alert(`${nombre} agregado al carrito`);
        });
    }

    // Inicio de la app
    mostrarCarrito();
});


//LOGICA PARA EL BOTON LOGIN
/* --- CONFIGURACIÓN DE DATOS --- */
const ADMIN_USER = {
    email: "bryan@systemic.com",
    pass: "ingeniero2026"
};

document.addEventListener('DOMContentLoaded', () => {
    // --- 1. LÓGICA DE PERSISTENCIA DE SESIÓN (Para todas las páginas) ---
    const authLink = document.getElementById('auth-link');
    const sesionIniciada = localStorage.getItem('sesionIniciada');
    const usuarioActivo = JSON.parse(localStorage.getItem('usuarioSystemic'));

    if (sesionIniciada === "true" && usuarioActivo) {
        // Extraemos el nombre del correo (ej: 'bryan' de 'bryan@systemic.com')
        const nombreUsuario = usuarioActivo.email.split('@')[0];
        
        // Modificamos el header para mostrar el nombre
        if (authLink) {
            authLink.innerText = `Hola, ${nombreUsuario}`;
            authLink.href = "#"; // Evita que te mande de nuevo al login
            authLink.style.color = "#3b82f6";
            authLink.style.fontWeight = "bold";
            
            // Opcional: Agregar un evento para cerrar sesión si se desea
            authLink.title = "Haz doble clic para cerrar sesión";
            authLink.addEventListener('dblclick', () => {
                localStorage.removeItem('sesionIniciada');
                location.reload();
            });
        }
    }

    // --- 2. LÓGICA ESPECÍFICA DEL FORMULARIO DE LOGIN ---
    // Usamos condicionales para evitar errores si el script carga en páginas sin formulario
    const loginForm = document.querySelector('.caja-login form');
    
    if (loginForm) {
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const btnCrearCuenta = document.querySelector('.btn-secundario');

        // EVENTO: INICIAR SESIÓN
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const emailValue = emailInput.value;
            const passValue = passwordInput.value;
            const usuarioGuardado = JSON.parse(localStorage.getItem('usuarioSystemic'));

            // Validación contra Admin o Usuario Registrado
            if (emailValue === ADMIN_USER.email && passValue === ADMIN_USER.pass) {
                iniciarSesionExitosa(emailValue);
            } 
            else if (usuarioGuardado && emailValue === usuarioGuardado.email && passValue === usuarioGuardado.pass) {
                iniciarSesionExitosa(emailValue);
            } 
            else {
                alert("Credenciales incorrectas. Prueba con bryan@systemic.com / ingeniero2026");
            }
        });

        // EVENTO: CREAR CUENTA
        if (btnCrearCuenta) {
            btnCrearCuenta.addEventListener('click', () => {
                const emailValue = emailInput.value;
                const passValue = passwordInput.value;

                if (!emailValue || !passValue) {
                    alert("Por favor, ingresa datos para el registro.");
                    return;
                }

                const nuevoUsuario = { email: emailValue, pass: passValue };
                localStorage.setItem('usuarioSystemic', JSON.stringify(nuevoUsuario));
                
                alert("¡Cuenta creada! Ahora dale a 'Iniciar Sesión' con tus datos.");
            });
        }
    }
});

/* --- FUNCIONES AUXILIARES --- */
function iniciarSesionExitosa(email) {
    localStorage.setItem('sesionIniciada', 'true');
    // Guardamos el objeto completo para que el nombre persista al navegar
    localStorage.setItem('usuarioSystemic', JSON.stringify({ email: email }));
    
    alert("¡Inicio de sesión correcto!");
    // Redirigir a la raíz (ajusta la ruta según donde estés)
    window.location.href = "/"; 
}


// Buscamos el botón de realizar pedido
const btnRealizar = document.querySelector('.btn-realizar-pedido');

if (btnRealizar) {
    btnRealizar.addEventListener('click', function() {
        // 1. Verificar si hay algo en el carrito
        const carrito = JSON.parse(localStorage.getItem('carrito')) || [];

        if (carrito.length === 0) {
            alert("Tu cesta está vacía. Agrega algunos juegos antes de comprar.");
            return;
        }

        // 2. Mostrar el anuncio nativo (como el de tu imagen)
        alert("¡Compra realizada con éxito! Gracias por confiar en Systemic Play.");

        // 3. Limpiar los datos
        localStorage.removeItem('carrito');

        // 4. Limpiar la vista de la tabla para que el profe vea que ya no hay nada
        const tablaItems = document.getElementById('items-carrito');
        if (tablaItems) tablaItems.innerHTML = '';

        // 5. Resetear los totales
        if (document.getElementById('subtotal-valor')) {
            document.getElementById('subtotal-valor').innerText = 'S/ 0.00';
        }
        if (document.getElementById('total-valor')) {
            document.getElementById('total-valor').innerText = 'S/ 0.00';
        }

        // 6. Regresar al inicio automáticamente tras aceptar la alerta
        window.location.replace('/');
    });
}

// Función para que los botones + y - funcionen
function cambiarCantidad(valor) {
    const input = document.getElementById('cantidad-producto');
    let cantidadActual = parseInt(input.value);
    
    cantidadActual += valor;

    // No permitimos menos de 1 producto
    if (cantidadActual < 1) cantidadActual = 1;
    
    input.value = cantidadActual;
}

/*erick*/

/* --- FUNCIONES AUXILIARES --- barra subir y bajar funcion*/
function iniciarSesionExitosa(email) {
    localStorage.setItem('sesionIniciada', 'true');
    // Guardamos el objeto completo para que el nombre persista al navegar
    localStorage.setItem('usuarioSystemic', JSON.stringify({ email: email }));
    
    alert("¡Inicio de sesión correcto!");
    // Redirigir a la raíz (ajusta la ruta según donde estés)
    window.location.href = "/"; 
}

// 1. Seleccionamos los elementos del DOM
  const botonRestar = document.querySelector('.btn-restar');
  const botonSumar = document.querySelector('.btn-sumar');
  const inputCantidad = document.querySelector('.input-valor');

if (botonRestar && botonSumar && inputCantidad) {
    
    // 2. Función para restar
    botonRestar.addEventListener('click', () => {
        let valorActual = parseInt(inputCantidad.value);
        if (valorActual > 1) {
            inputCantidad.value = valorActual - 1;
        }
    });

    // 3. Función para sumar
    botonSumar.addEventListener('click', () => {
        let valorActual = parseInt(inputCantidad.value);
        inputCantidad.value = valorActual + 1;
    });
}

//let indiceSlide = 0;
//function cambiarSlide(direccion) {
    //const wrapper = document.querySelector('.slider-wrapper');
    //const slides = document.querySelectorAll('.slide');
    
   // indiceSlide += direccion;
    
   // if (indiceSlide >= slides.length) indiceSlide = 0;
   // if (indiceSlide < 0) indiceSlide = slides.length - 1;
    
   // wrapper.style.transform = `translateX(-${indiceSlide * 100}%)`;
//}