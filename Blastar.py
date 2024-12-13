import tkinter as tk  
from random import randint  
import pygame  

pygame.mixer.init()  

sonido_disparo = pygame.mixer.Sound("shoot.wav")  
sonido_explosion = pygame.mixer.Sound("explosion.wav")  

raiz = tk.Tk()  
raiz.title("Blastar")  
raiz.resizable(False, False)  

canvas = tk.Canvas(raiz, width=600, height=400, bg="black")  
canvas.pack()  

imagen_jugador = tk.PhotoImage(file="player_ship.png")  
imagen_enemigo = tk.PhotoImage(file="enemy.png")  

nave_jugador = canvas.create_image(300, 350, image=imagen_jugador, tags="player")  
 
velocidad_nave = 20  
velocidad_bala = 10  
velocidad_enemigo = 2  
puntuacion, nivel = 0, 1  

etiqueta_puntuacion = tk.Label(raiz, text=f"Puntuación: {puntuacion}", fg="white", bg="black", font=("Arial", 14))  
etiqueta_puntuacion.pack()  
etiqueta_nivel = tk.Label(raiz, text=f"Nivel: {nivel}", fg="white", bg="black", font=("Arial", 14))  
etiqueta_nivel.pack()  
 
balas = []  
enemigos = []  

def iniciar_juego():  
    global balas, enemigos, puntuacion, nivel  
    boton_inicio.pack_forget()  
    canvas.delete("all")  
    balas.clear()  
    enemigos.clear()  
    puntuacion = 0  
    nivel = 1  
    etiqueta_puntuacion.config(text=f"Puntuación: {puntuacion}")  
    etiqueta_nivel.config(text=f"Nivel: {nivel}")  
    canvas.create_image(300, 350, image=imagen_jugador, tags="player")  
    raiz.bind("<Left>", mover_izquierda)  
    raiz.bind("<Right>", mover_derecha)  
    raiz.bind("<space>", disparar)  
    crear_enemigo()  
    mover_enemigos()  
    mover_balas()  


def juego_terminado():  
    canvas.create_text(300, 200, text="FIN DEL JUEGO", fill="red", font=("Arial", 30))  
    raiz.after(3000, raiz.quit)  


def mover_izquierda(event):  
    canvas.move("player", -velocidad_nave, 0)  
    x1, _ = canvas.coords("player")  
    if x1 < 30:   
        canvas.move("player", 30 - x1, 0)  


def mover_derecha(event):  
    canvas.move("player", velocidad_nave, 0)  
    x1, _ = canvas.coords("player")  
    if x1 > 570: 
        canvas.move("player", 570 - x1, 0)  


def disparar(event):  
    x1, y1 = canvas.coords("player")  
    bala = canvas.create_rectangle(x1 - 5, y1 - 20, x1 + 5, y1, fill="white", tags="bullet")  
    balas.append(bala)  
    sonido_disparo.play()  


def crear_enemigo():  
    posicion_x = randint(50, 550)  
    enemigo = canvas.create_image(posicion_x, 50, image=imagen_enemigo, tags="enemy")  
    enemigos.append(enemigo)  
    raiz.after(max(500, 2000 - nivel * 100), crear_enemigo)  


def mover_enemigos():  
    for enemigo in list(enemigos):  
        canvas.move(enemigo, 0, velocidad_enemigo)  
        if canvas.coords(enemigo)[1] >= 400:  
            enemigos.remove(enemigo)  
            canvas.delete(enemigo)  
            juego_terminado()  
    raiz.after(50, mover_enemigos)  


def mover_balas():  
    for bala in list(balas):  
        canvas.move(bala, 0, -velocidad_bala)  
        if canvas.coords(bala)[1] <= 0:  
            balas.remove(bala)  
            canvas.delete(bala)  
    raiz.after(50, mover_balas)  

   
def verificar_colisiones():  
    global puntuacion, nivel, velocidad_enemigo  
    for bala in list(balas):  
        for enemigo in list(enemigos):  
            if canvas.bbox(bala) and canvas.bbox(enemigo):  
                if (canvas.bbox(bala)[2] > canvas.bbox(enemigo)[0] and  
                    canvas.bbox(bala)[0] < canvas.bbox(enemigo)[2] and  
                    canvas.bbox(bala)[1] < canvas.bbox(enemigo)[3] and  
                    canvas.bbox(bala)[3] > canvas.bbox(enemigo)[1]):  
                    canvas.delete(bala)  
                    balas.remove(bala)  
                    canvas.delete(enemigo)  
                    enemigos.remove(enemigo)  
                    sonido_explosion.play()  
                    puntuacion += 10  
                    etiqueta_puntuacion.config(text=f"Puntuación: {puntuacion}")  

                    if puntuacion % 100 == 0:  
                        nivel += 1  
                        velocidad_enemigo += 1  
                        etiqueta_nivel.config(text=f"Nivel: {nivel}")  
                    break  
    raiz.after(50, verificar_colisiones)  


boton_inicio = tk.Button(raiz, text="JUGAR", command=iniciar_juego, font=("Arial", 14), bg="green", fg="white")  
boton_inicio.pack()  


mover_balas()  
mover_enemigos()  
verificar_colisiones()  


raiz.mainloop()