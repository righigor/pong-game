import tkinter as tk

# Configuração inicial
root = tk.Tk()
root.title("Pong")
canvas = tk.Canvas(root, width=800, height=400, bg="black")
canvas.pack()

# Desenho dos elementos
paddle1 = canvas.create_rectangle(20, 150, 30, 250, fill="white")
paddle2 = canvas.create_rectangle(770, 150, 780, 250, fill="white")
ball = canvas.create_oval(390, 190, 410, 210, fill="white")

# Variáveis de movimentação
paddle1_speed = 0
paddle2_speed = 0
ball_speed_x = 3
ball_speed_y = 3

# Movimentação dos paddles
def move_paddle1(event):
    global paddle1_speed
    if event.keysym == 'w':
        paddle1_speed = -3
    elif event.keysym == 's':
        paddle1_speed = 3

def stop_paddle1(event):
    global paddle1_speed
    if event.keysym in ['w', 's']:
        paddle1_speed = 0

def move_paddle2(event):
    global paddle2_speed
    if event.keysym == 'Up':
        paddle2_speed = -3
    elif event.keysym == 'Down':
        paddle2_speed = 3

def stop_paddle2(event):
    global paddle2_speed
    if event.keysym in ['Up', 'Down']:
        paddle2_speed = 0

root.bind('<KeyPress-w>', move_paddle1)
root.bind('<KeyPress-s>', move_paddle1)
root.bind('<KeyRelease-w>', stop_paddle1)
root.bind('<KeyRelease-s>', stop_paddle1)

root.bind('<KeyPress-Up>', move_paddle2)
root.bind('<KeyPress-Down>', move_paddle2)
root.bind('<KeyRelease-Up>', stop_paddle2)
root.bind('<KeyRelease-Down>', stop_paddle2)

# Função para atualizar o jogo
def update_game():
    global ball_speed_x, ball_speed_y

    # Mover paddles
    canvas.move(paddle1, 0, paddle1_speed)
    canvas.move(paddle2, 0, paddle2_speed)

    # Mover bola
    canvas.move(ball, ball_speed_x, ball_speed_y)
    
    # Obter coordenadas dos elementos
    ball_coords = canvas.coords(ball)
    paddle1_coords = canvas.coords(paddle1)
    paddle2_coords = canvas.coords(paddle2)

    # Verificar colisão com as bordas
    if ball_coords[1] <= 0 or ball_coords[3] >= 400:
        ball_speed_y = -ball_speed_y

    # Verificar colisão com os paddles
    if (ball_coords[0] <= paddle1_coords[2] and paddle1_coords[1] < ball_coords[3] and paddle1_coords[3] > ball_coords[1]) or \
       (ball_coords[2] >= paddle2_coords[0] and paddle2_coords[1] < ball_coords[3] and paddle2_coords[3] > ball_coords[1]):
        ball_speed_x = -ball_speed_x

    # Verificar pontuação
    if ball_coords[0] <= 0 or ball_coords[2] >= 800:
        canvas.coords(ball, 390, 190, 410, 210)
        ball_speed_x = -ball_speed_x

    root.after(20, update_game)

# Iniciar o jogo
update_game()
root.mainloop()
