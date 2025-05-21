import turtle
import tkinter as tk
from turtle import RawTurtle, TurtleScreen

# ========================
# Configuración de la ventana y del lienzo
# ========================
ventana = tk.Tk()
ventana.title("Pong")
lienzo = tk.Canvas(ventana, width=800, height=600)
lienzo.pack()
pantalla = TurtleScreen(lienzo)
pantalla.bgcolor("black")
pantalla.tracer(0)  # Actualizamos la pantalla manualmente

# ========================
# Variables globales del juego
# ========================
puntos_a = 0                   # Puntuación del Jugador A
puntos_b = 0                   # Puntuación del Jugador B
velocidad_pelota = 1.0         # Factor de velocidad base de la pelota (según la dificultad)
juego_activo = False           # Bandera que indica si el juego está en marcha
puntuacion_ganadora = 5        # Puntuación necesaria para ganar
direccion_inicial = 1          # Dirección inicial de la pelota (1: derecha, -1: izquierda)
modo_extremo = False           # Bandera para saber si se ha seleccionado el nivel EXTREMO

# Variables para controlar el movimiento continuo de las paletas
mover_paleta_a_arriba = False
mover_paleta_a_abajo = False
mover_paleta_b_arriba = False
mover_paleta_b_abajo = False

# ========================
# Creación de las paletas
# ========================
# Paleta del Jugador A (izquierda)
paleta_a = RawTurtle(pantalla)
paleta_a.speed(0)
paleta_a.shape("square")
paleta_a.color("white")
paleta_a.shapesize(stretch_wid=6, stretch_len=1)
paleta_a.penup()
paleta_a.goto(-380, 0)  # La X es fija; la Y se centrará en cada ronda

# Paleta del Jugador B (derecha)
paleta_b = RawTurtle(pantalla)
paleta_b.speed(0)
paleta_b.shape("square")
paleta_b.color("white")
paleta_b.shapesize(stretch_wid=6, stretch_len=1)
paleta_b.penup()
paleta_b.goto(380, 0)

# ========================
# Creación de la pelota
# ========================
pelota = RawTurtle(pantalla)
pelota.speed(1)
pelota.shape("square")
pelota.color("white")
pelota.penup()
pelota.goto(0, 0)
# La velocidad en X e Y se ajustará en reiniciarPelota() usando 'velocidad_pelota' y 'direccion_inicial'
pelota.dx = 1.25  
pelota.dy = -1.25 

# ========================
# Creación de los indicadores (marcador y mensajes)
# ========================
# Indicador de puntuación
indicador = RawTurtle(pantalla)
indicador.speed(0)
indicador.color("white")
indicador.penup()
indicador.hideturtle()
indicador.goto(0, 260)

# Turtle para mostrar mensajes temporales
mensaje = RawTurtle(pantalla)
mensaje.speed(0)
mensaje.color("yellow")
mensaje.penup()
mensaje.hideturtle()
mensaje.goto(0, 0)

def actualizarMarcador():
    """Limpia y muestra el marcador con las puntuaciones actuales."""
    indicador.clear()
    indicador.write(f"Jugador A: {puntos_a}  Jugador B: {puntos_b}",
                     align="center", font=("Courier", 24, "normal"))

def mostrarMensaje(texto, duracion=2000):
    """
    Muestra un mensaje en pantalla durante 'duracion' milisegundos sin detener el juego.
    
    :param texto: Mensaje a mostrar.
    :param duracion: Tiempo en milisegundos que el mensaje estará visible.
    """
    mensaje.clear()
    mensaje.write(texto, align="center", font=("Courier", 24, "normal"))
    ventana.after(duracion, lambda: (mensaje.clear(), actualizarMarcador()))

def mostrarMensajeFinal(texto, duracion=6000):
    """
    Muestra un mensaje final en grande para felicitar al ganador.
    
    :param texto: Mensaje de felicitación.
    :param duracion: Tiempo en milisegundos que el mensaje estará visible.
    """
    mensaje.clear()
    # Fuente más grande para el mensaje final
    mensaje.write(texto, align="center", font=("Courier", 32, "normal"))
    ventana.after(duracion, lambda: (mensaje.clear(), actualizarMarcador()))    

# ========================
# Movimiento continuo de las paletas
# ========================
def actualizarMovimientoPaletas():
    """
    Actualiza la posición de las paletas de forma continua según las teclas presionadas.
    Se llama en cada iteración del bucle del juego.
    """
    # Movimiento para el Jugador A (izquierda)
    if mover_paleta_a_arriba:
        y = paleta_a.ycor()
        if y < 240:
            paleta_a.sety(y + 20)
    if mover_paleta_a_abajo:
        y = paleta_a.ycor()
        if y > -240:
            paleta_a.sety(y - 20)
    # Movimiento para el Jugador B (derecha)
    if mover_paleta_b_arriba:
        y = paleta_b.ycor()
        if y < 240:
            paleta_b.sety(y + 20)
    if mover_paleta_b_abajo:
        y = paleta_b.ycor()
        if y > -240:
            paleta_b.sety(y - 20)

# ========================
# Manejadores de eventos de teclado para movimiento continuo
# ========================
def alPresionarTecla(evento):
    """
    Activa la bandera de movimiento continuo según la tecla presionada.
    
    :param evento: Objeto del evento con la tecla presionada.
    """
    global mover_paleta_a_arriba, mover_paleta_a_abajo, mover_paleta_b_arriba, mover_paleta_b_abajo
    tecla = evento.keysym.lower()
    if tecla == "w":
        mover_paleta_a_arriba = True
    elif tecla == "s":
        mover_paleta_a_abajo = True
    elif evento.keysym == "Up":
        mover_paleta_b_arriba = True
    elif evento.keysym == "Down":
        mover_paleta_b_abajo = True

def alSoltarTecla(evento):
    """
    Desactiva la bandera de movimiento continuo al soltar una tecla.
    
    :param evento: Objeto del evento con la tecla liberada.
    """
    global mover_paleta_a_arriba, mover_paleta_a_abajo, mover_paleta_b_arriba, mover_paleta_b_abajo
    tecla = evento.keysym.lower()
    if tecla == "w":
        mover_paleta_a_arriba = False
    elif tecla == "s":
        mover_paleta_a_abajo = False
    elif evento.keysym == "Up":
        mover_paleta_b_arriba = False
    elif evento.keysym == "Down":
        mover_paleta_b_abajo = False

# Vinculación de eventos de teclado
ventana.bind("<KeyPress>", alPresionarTecla)
ventana.bind("<KeyRelease>", alSoltarTecla)

# ========================
# Configuración de los botones
# ========================
# Botón único para iniciar o continuar la partida
boton_inicio = tk.Button(ventana, text="¡EMPEZAR A JUGAR!", font=("Courier", 16))

def mostrarBotonInicio(texto, comando):
    """
    Configura y muestra el botón de inicio/continuación.
    
    :param texto: Texto a mostrar en el botón.
    :param comando: Función a ejecutar al pulsar el botón.
    """
    boton_inicio.config(text=texto, command=comando)
    boton_inicio.pack(pady=10)

def ocultarBotonInicio():
    """Oculta el botón de inicio para evitar duplicados."""
    boton_inicio.pack_forget()

# Panel para seleccionar la dificultad (ahora con 4 opciones: Fácil, Medio, Difícil y EXTREMO)
panel_dificultad = tk.Frame(ventana)
boton_facil = tk.Button(panel_dificultad, text="Fácil", font=("Courier", 16),
                         command=lambda: seleccionarDificultad(5.0, extremo=False))
boton_medio = tk.Button(panel_dificultad, text="Medio", font=("Courier", 16),
                         command=lambda: seleccionarDificultad(6.5, extremo=False))
boton_dificil = tk.Button(panel_dificultad, text="Difícil", font=("Courier", 16),
                           command=lambda: seleccionarDificultad(8, extremo=False))
boton_extremo = tk.Button(panel_dificultad, text="EXTREMO", font=("Courier", 16),
                          command=lambda: seleccionarDificultad(8, extremo=True))
boton_facil.pack(side="left", padx=5, pady=5)
boton_medio.pack(side="left", padx=5, pady=5)
boton_dificil.pack(side="left", padx=5, pady=5)
boton_extremo.pack(side="left", padx=5, pady=5)

def mostrarPanelDificultad():
    """Muestra el panel de selección de dificultad."""
    panel_dificultad.pack(pady=10)

def ocultarPanelDificultad():
    """Oculta el panel de selección de dificultad."""
    panel_dificultad.pack_forget()

def seleccionarDificultad(velocidad_inicial, extremo=False):
    """
    Configura la dificultad seleccionada, reiniciando la velocidad base de la pelota,
    las puntuaciones y, en caso de EXTREMO, activa el modo extremo.
    
    :param velocidad_inicial: Valor numérico que define la velocidad base.
    :param extremo: Valor booleano que indica si se seleccionó el modo EXTREMO.
    """
    global velocidad_pelota, puntos_a, puntos_b, direccion_inicial, modo_extremo
    velocidad_pelota = velocidad_inicial
    puntos_a = 0
    puntos_b = 0
    direccion_inicial = 1  # Se inicia lanzando la pelota hacia la derecha
    modo_extremo = extremo  # Activa o desactiva el modo EXTREMO según la selección
    actualizarMarcador()
    ocultarPanelDificultad()
    reiniciarRonda()  # Centra las paletas y reposiciona la pelota
    iniciarBucleJuego()

# ========================
# Funciones para controlar la partida
# ========================
def reiniciarPelota():
    """
    Reposiciona la pelota en el centro, la lanza en la dirección establecida y asigna
    su velocidad en función de 'velocidad_pelota' y 'direccion_inicial'. Luego, invierte
    la dirección para la próxima ronda.
    """
    global direccion_inicial
    pelota.goto(0, -200)
    pelota.dx = 1.25 * velocidad_pelota * direccion_inicial
    pelota.dy = -1.25 * velocidad_pelota
    direccion_inicial *= -1  # Alterna la dirección de lanzamiento

def reiniciarPaletas():
    """
    Centra verticalmente ambas paletas en el eje Y.
    Las posiciones en X permanecen fijas.
    """
    paleta_a.sety(0)
    paleta_b.sety(0)

def reiniciarRonda():
    """
    Reinicia la ronda: centra las paletas y reposiciona la pelota con dirección alterna.
    """
    reiniciarPaletas()
    reiniciarPelota()

def iniciarJuegoConDificultad():
    """
    Reinicia el juego mostrando el panel de selección de dificultad.
    Se utiliza al reiniciar la partida completa.
    """
    mostrarPanelDificultad()

def siguienteRonda():
    """
    Inicia la siguiente ronda:
      - Incrementa la velocidad de la pelota en un 5%.
      - Reinicia la posición de la pelota y centra las paletas.
      - Reanuda el juego.
    """
    global velocidad_pelota
    velocidad_pelota *= 1.05  # Incrementa la velocidad en un 5%
    reiniciarRonda()
    ocultarBotonInicio()
    iniciarBucleJuego()

def iniciarBucleJuego():
    """Activa la bandera del juego y comienza el bucle principal."""
    global juego_activo
    juego_activo = True
    bucleJuego()

def bucleJuego():
    """
    Bucle principal del juego que:
      - Actualiza el movimiento continuo de las paletas.
      - Mueve la pelota según su velocidad.
      - Verifica colisiones con paredes y paletas.
      - Controla la anotación de puntos y el final de la ronda.
    """
    global puntos_a, puntos_b, juego_activo

    if not juego_activo:
        return  # Si el juego está pausado, se detiene el bucle

    pantalla.update()  # Actualiza la pantalla

    # Actualiza el movimiento de las paletas
    actualizarMovimientoPaletas()

    # Mueve la pelota sumando su velocidad a su posición actual
    pelota.setx(pelota.xcor() + pelota.dx)
    pelota.sety(pelota.ycor() + pelota.dy)

    # ------------------------
    # Colisiones con las paredes superior e inferior
    # ------------------------
    if pelota.ycor() > 290:
        pelota.sety(290)
        pelota.dy *= -1
    if pelota.ycor() < -290:
        pelota.sety(-290)
        pelota.dy *= -1

    # ------------------------
    # Colisiones laterales y con las paletas
    # ------------------------
    # Si la pelota se dirige hacia la derecha
    if pelota.dx > 0:
        # Si la pelota está en la zona de la paleta derecha (entre x=360 y x=390)
        if pelota.xcor() >= 360 and pelota.xcor() <= 390:
            if abs(pelota.ycor() - paleta_b.ycor()) < 60:
                # Rebote en la paleta derecha
                pelota.setx(360)
                pelota.dx *= -1
                # En EXTREMO, aumenta la velocidad en un 2% en cada choque
                if modo_extremo:
                    pelota.dx *= 1.02
                    pelota.dy *= 1.02
        # Si la pelota sobrepasa x=390, es gol para el Jugador A
        elif pelota.xcor() > 390:
            pelota.goto(0, 0)
            pelota.dx *= -1
            puntos_a += 1
            juego_activo = False
            mostrarMensaje("¡Jugador A anota un punto!")
            if puntos_a == puntuacion_ganadora:
                ventana.after(2100, lambda: mostrarMensajeFinal(" ¡FELICITACIONES, Jugador A!\nEres el nuevo MAESTRO DEL PONG 🎉🏆🔥", 10000))
                ventana.after(2100, lambda: mostrarBotonInicio("¡VOLVER A JUGAR!", iniciarJuegoConDificultad))
            else:
                ventana.after(2100, lambda: mostrarBotonInicio("PULSA ESPACIO - ¡SIGUIENTE RONDA! - PULSA ESPACIO", siguienteRonda))
            return

    # Si la pelota se dirige hacia la izquierda
    if pelota.dx < 0:
        if pelota.xcor() <= -360 and pelota.xcor() >= -390:
            if abs(pelota.ycor() - paleta_a.ycor()) < 60:
                # Rebote en la paleta izquierda
                pelota.setx(-360)
                pelota.dx *= -1
                if modo_extremo:
                    pelota.dx *= 1.05
                    pelota.dy *= 1.05
        elif pelota.xcor() < -390:
            pelota.goto(0, 0)
            pelota.dx *= -1
            puntos_b += 1
            juego_activo = False
            mostrarMensaje("¡Jugador B anota un punto!")
            if puntos_b == puntuacion_ganadora:
                ventana.after(2100, lambda: mostrarMensajeFinal(" ¡FELICITACIONES, Jugador B!\nEres el nuevo MAESTRO DEL PONG 🎉🏆🔥", 10000))
                ventana.after(2100, lambda: mostrarBotonInicio("¡VOLVER A JUGAR!", iniciarJuegoConDificultad))
            else:
                ventana.after(2100, lambda: mostrarBotonInicio("PULSA ESPACIO - ¡SIGUIENTE RONDA! - PULSA ESPACIO", siguienteRonda))
            return

    # Programa la siguiente iteración del bucle después de 20 ms
    pantalla.ontimer(bucleJuego, 20)

# ========================
# Implementación de la tecla "espacio" para avanzar la ronda
# ========================
def alPresionarEspacio(evento):
    """
    Si el juego está en pausa y se muestra el botón "PULSA ESPACIO - ¡SIGUIENTE RONDA! - PULSA ESPACIO", al presionar
    la barra espaciadora se inicia la siguiente ronda.
    """
    if not juego_activo and boton_inicio.winfo_ismapped():
        if boton_inicio.cget("text") == "PULSA ESPACIO - ¡SIGUIENTE RONDA! - PULSA ESPACIO":
            siguienteRonda()

ventana.bind("<space>", alPresionarEspacio)

# ========================
# Implementación de la tecla "esc" para volver al menú de dificultad
# ========================
def alPresionarEscape(evento):
    """
    Al presionar "esc", se detiene el juego y se muestra el menú de selección de dificultad.
    Permite reiniciar la partida o cambiar la dificultad sin usar el ratón.
    """
    global juego_activo
    juego_activo = False
    ocultarBotonInicio()
    mostrarPanelDificultad()

ventana.bind("<Escape>", alPresionarEscape)

def mostrarInstrucciones():
    """
    Muestra un mensaje inicial con las instrucciones de los controles del juego.
    """
    instrucciones = (
        "¡Bienvenidos al Pong Extremo!\n\n"
        "Controles del juego:\n"
        "Jugador A (izquierda):\n"
        "  - Mover hacia arriba: 'W'\n"
        "  - Mover hacia abajo:  'S'\n\n"
        "Jugador B (derecha):\n"
        "  - Mover hacia arriba: 'Flecha Arriba ⬆️'\n"
        "  - Mover hacia abajo:  'Flecha Abajo  ⬇️'\n\n"
        "¡Que comience el juego!"
    )
    mostrarMensaje(instrucciones, duracion=10000)

# ========================
# Inicio del programa
# ========================

# Llama a la función para mostrar las instrucciones al inicio del programa
mostrarInstrucciones()

mostrarPanelDificultad()
ventana.mainloop()
