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
    // 1. Estado Global del Carrito
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    // 2. Selección de Productos (Abarca todos los casos)
    const productos = document.querySelectorAll('.tarjeta_juego, .producto, .producto_item, .card-producto');

    productos.forEach((juego) => {
        // Solo creamos el botón si no existe uno manualmente en el HTML
        let boton = juego.querySelector(".btn-carrito");
        
        if (!boton) {
            juego.style.position = "relative";
            boton = document.createElement("button");
            boton.classList.add("btn-carrito");
            boton.innerHTML = `<i class="fa-solid fa-cart-shopping"></i>`;
            
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
            const precio = parseFloat(precioTexto.replace(/[^\d.]/g, ""));
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

    // 3. Funciones de Interfaz del Carrito
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

        document.querySelectorAll(".eliminar-producto").forEach(btn => {
            btn.onclick = () => {
                carrito.splice(btn.dataset.index, 1);
                actualizarYGuardar();
            };
        });
    }

    // 4. Lógica para botón agregar desde detalle
    const btnAgregarDetalle = document.querySelector('.btn-carrito'); 
    if (btnAgregarDetalle && !btnAgregarDetalle.closest('.tarjeta_juego, .producto')) {
        btnAgregarDetalle.addEventListener('click', (e) => {
            e.preventDefault();
            const nombre = document.querySelector('.nombre-juego')?.textContent.trim() || "Juego";
            const precioTexto = document.querySelector('.precio')?.textContent || "0";
            const precio = parseFloat(precioTexto.replace(/[^\d.]/g, ""));
            const imagen = document.querySelector('img')?.src || "";
            const cantidadInput = document.querySelector('.input-valor');
            const cantidad = cantidadInput ? parseInt(cantidadInput.value) : 1;

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

    // 5. Lógica para realizar pedido
    //const btnRealizar = document.querySelector('.btn-realizar-pedido');
    //if (btnRealizar) {
    //    btnRealizar.addEventListener('click', function() {
    //        if (carrito.length === 0) {
    //            alert("Tu cesta está vacía.");
    //            return;
    //        }
    //        alert("¡Compra realizada con éxito! Gracias por confiar en Systemic Play.");
    //        localStorage.removeItem('carrito');
    //        carrito = [];
    //        mostrarCarrito();
    //        window.location.replace('/');
    //    });
    //}

    const btnRealizar = document.querySelector('.btn-realizar-pedido');
    if (btnRealizar) {
        btnRealizar.addEventListener('click', function() {
            if (carrito.length === 0) {
                alert("Tu cesta está vacía.");
                return;
            }

            // Enviamos el carrito al servidor Flask
            fetch('/finalizar-compra', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(carrito),
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje) {
                    alert("¡Compra realizada con éxito! Stock actualizado.");
                    localStorage.removeItem('carrito');
                    carrito = [];
                    mostrarCarrito();
                    window.location.replace('/');
                } else {
                    alert("Error: " + data.error);
                }
            });
        });
    }

    // 6. Botones de cantidad (+ / -)
    const botonRestar = document.querySelector('.btn-restar');
    const botonSumar = document.querySelector('.btn-sumar');
    const inputCantidad = document.querySelector('.input-valor');

    if (botonRestar && botonSumar && inputCantidad) {
        botonRestar.addEventListener('click', () => {
            let valorActual = parseInt(inputCantidad.value);
            if (valorActual > 1) inputCantidad.value = valorActual - 1;
        });

        botonSumar.addEventListener('click', () => {
            let valorActual = parseInt(inputCantidad.value);
            inputCantidad.value = valorActual + 1;
        });
    }

    // Inicializar
    mostrarCarrito();
});