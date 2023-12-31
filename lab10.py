from tkinter import *
from tkinter import messagebox


def new_game_btn():
    root.destroy()
    game()


def exit():
    root.destroy()


# Проверка наличия победителя
def check_winner():
    # Проверка строк
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    # Проверка столбцов
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    # Проверка диагоналей
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    # Проверка ничьей
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return 'Ничья'

    return None


def ai_move():
    best_score = float('-inf')
    best_move = None

    # Перебор всех возможных ходов
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ' '

                # Выбор лучшего хода
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    # Выполнение хода компьютера
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'
        buttons[best_move[0]][best_move[1]].config(text='о', font=("Arial 36 bold"), state='disabled')
        winner = check_winner()
        if winner:
            end_game(winner)


# Алгоритм минимакс
def minimax(board, depth, is_maximizing):
    global winner
    winner = check_winner()

    if winner:
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        else:
            return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score


# Завершение игры
def end_game(winner):
    for row in buttons:
        for button in row:
            button.config(state='disabled')
    if winner == 'Ничья':
        messagebox.showinfo('Конец игры', 'Ничья!')
        new_game()
    else:
        messagebox.showinfo('Конец игры', f'Победитель: {winner}!')
        new_game()


def dismiss(win):
    win.grab_release()
    win.destroy()


def new_game():
    win = Toplevel(root)
    w = root.winfo_screenwidth() // 2 - 150
    h = root.winfo_screenheight() // 2 - 50
    win.title('Конец игры')
    win.geometry(f'300x100+{w}+{h}')
    win.resizable(False, False)
    win.protocol("VM_DELETE_WINDOW", lambda: dismiss(win))
    win.grab_set()

    main_label = Label(win, text="Выберите нужный вариант.", font=("Arial 10 bold"), justify=CENTER, )
    main_label.pack()

    new_game_btn1 = Button(win, text='Новая Игра', command=new_game_btn)
    new_game_btn1.pack()

    exit_btn = Button(win, text='Выход', command=exit)
    exit_btn.pack()


# Обработчик клика по кнопке
def button_click(i, j):
    if board[i][j] == ' ':
        buttons[i][j].config(text='x', font=("Arial 36 bold"), state='disabled')
        board[i][j] = 'X'
        winner = check_winner()
        if not winner:
            ai_move()
        else:
            end_game(winner)


def game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]

    global root
    root = Tk()
    root.title('Крестики-нолики')

    w = root.winfo_screenwidth() // 2 - 225
    h = root.winfo_screenheight() // 2 - 225

    root.geometry(f'450x450+{w}+{h}')
    root.resizable(False, False)

    # создание и размещение кнопок
    for c in range(3): root.columnconfigure(index=c, weight=1)
    for r in range(3): root.rowconfigure(index=r, weight=1)
    global buttons
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            button = Button(root, text='  ', font=("Arial 36 bold"), command=lambda x=i, y=j: button_click(x, y))
            button.grid(row=i, column=j, sticky=NSEW)
            row.append(button)

        buttons.append(row)

    root.mainloop()


game()
