import tkinter as tk

# Configuração inicial
root = tk.Tk()
root.title("Pong Game")
canvas = tk.Canvas(root, width=800, height=400, bg="green")
canvas.pack()

# Desenho dos elementos
# Linhas dos gols
goal_line_left = canvas.create_line(30, 0, 30, 400, fill="white", width=2)
goal_line_right = canvas.create_line(770, 0, 770, 400, fill="white", width=2)

# Meio de campo
midfield_circle = canvas.create_oval(370, 170, 430, 230, outline="white", width=2)
midfield_line = canvas.create_line(400, 0, 400, 400, fill="white", width=2)

# Paddles e bola
paddle1 = canvas.create_rectangle(20, 150, 30, 250, fill="blue")
paddle2 = canvas.create_rectangle(770, 150, 780, 250, fill="white")
ball = canvas.create_oval(390, 190, 410, 210, fill="white")

# Pontuação e Placar
score_p1 = 0
score_p2 = 0
player_1 = ""
player_2 = ""
score_bg = canvas.create_rectangle(280, 10, 520, 50, fill="#4682b4")
score_label = canvas.create_text(400, 30, text=f"{player_1} {score_p1} x {score_p2} {player_2}", fill="white", font=("Arial", 16))

# Variáveis globais para as entradas e botões
player1_entry = None
player2_entry = None
start_button = None
play_again_button = None

# Função para atualizar a pontuação
def update_score():
    canvas.itemconfig(score_label, text=f"{player_1} {score_p1} x {score_p2} {player_2}")

# Renomear jogadores
def create_player_entries():
    global player1_entry, player2_entry, start_button
    player1_entry = tk.Entry(root)
    player1_entry.pack()
    player1_entry.place(x=180, y=185)
    player2_entry = tk.Entry(root)
    player2_entry.pack()
    player2_entry.place(x=450, y=185)

    start_button = tk.Button(root, text="Start", command=start_game)
    start_button.pack()
    start_button.place(x=371, y=184)

def start_game():
    global player_1, player_2
    player_1 = player1_entry.get()
    player_2 = player2_entry.get()
    if player_1 != "" and player_2 != "":
        update_score()
        player1_entry.destroy()
        player2_entry.destroy()
        start_button.destroy()
        update_game()

# Variáveis de movimentação
paddle1_speed = 0
paddle2_speed = 0
ball_speed_x = 5
ball_speed_y = 5

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

# Função para redefinir o jogo
def reset_game():
    global score_p1, score_p2, player_1, player_2, play_again_button
    score_p1 = 0
    score_p2 = 0
    player_1 = ""
    player_2 = ""
    canvas.delete("all")
    canvas.create_line(30, 0, 30, 400, fill="white", width=2)
    canvas.create_line(770, 0, 770, 400, fill="white", width=2)
    canvas.create_oval(370, 170, 430, 230, outline="white", width=2)
    canvas.create_line(400, 0, 400, 400, fill="white", width=2)
    global paddle1, paddle2, ball, score_bg, score_label
    paddle1 = canvas.create_rectangle(20, 150, 30, 250, fill="blue")
    paddle2 = canvas.create_rectangle(770, 150, 780, 250, fill="white")
    ball = canvas.create_oval(390, 190, 410, 210, fill="white")
    score_bg = canvas.create_rectangle(280, 10, 520, 50, fill="#4682b4")
    score_label = canvas.create_text(400, 30, text=f"{player_1} {score_p1} x {score_p2} {player_2}", fill="white", font=("Arial", 16))
    create_player_entries()
    if play_again_button:
        play_again_button.destroy()
        play_again_button = None

# Função para atualizar o jogo
def update_game():
    global ball_speed_x, ball_speed_y, score_p1, score_p2, player_1, player_2, play_again_button

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
    if ball_coords[0] <= 0:
        score_p2 += 1
        update_score()
        if score_p2 == 6:
            canvas.create_rectangle(250, 170, 550, 230, fill="white")
            canvas.create_text(400, 200, text=f"{player_2} venceu!", fill="#4169e1", font=("Arial", 24))
            play_again_button = tk.Button(root, text="Jogar Novamente", command=reset_game)
            play_again_button.pack()
            play_again_button.place(x=350, y=250)
            return
        canvas.coords(ball, 390, 190, 410, 210)
        ball_speed_x = -ball_speed_x
    elif ball_coords[2] >= 800:
        score_p1 += 1
        update_score()
        if score_p1 == 6:
            canvas.create_rectangle(250, 170, 550, 230, fill="#4169e1")
            canvas.create_text(400, 200, text=f"{player_1} venceu!", fill="white", font=("Arial", 24))
            play_again_button = tk.Button(root, text="Jogar Novamente", command=reset_game)
            play_again_button.pack()
            play_again_button.place(x=350, y=250)
            return
        canvas.coords(ball, 390, 190, 410, 210)
        ball_speed_x = -ball_speed_x

    root.after(20, update_game)

# Criar entradas e botões iniciais
create_player_entries()

# Iniciar o jogo
root.mainloop()
