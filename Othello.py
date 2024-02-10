from tkinter import *
import time
import random

def initialize_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]
    board[3][3] = board[4][4] = 'X'
    board[3][4] = board[4][3] = 'O'
    return board

def draw_board(canvas, board, current_player, selected_row, selected_col, valid_moves):
    canvas.delete("board")
    for row in range(8):
        for col in range(8):
            x1, y1, x2, y2 = col * 50, row * 50, (col + 1) * 50, (row + 1) * 50
            canvas.create_rectangle(x1, y1, x2, y2, fill='green', tags="board")

            if (row, col) in valid_moves:
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline='yellow', width=2, tags="board")

            if row == selected_row and col == selected_col:
                canvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=2, tags="board")

            position_text = f'{row}, {col}'
            canvas.create_text(x1 + 10, y1 + 10, text=position_text, font=("Helvetica", 15), fill='black', anchor='nw', tags="board")

    for row in range(8):
        for col in range(8):
            if board[row][col] != ' ':
                x1, y1, x2, y2 = col * 50, row * 50, (col + 1) * 50, (row + 1) * 50
                canvas.create_oval(x1, y1, x2, y2, fill='black' if board[row][col] == 'X' else 'white', tags="board")

def is_valid_move(board, row, col, player):
    if row < 0 or row >= 8 or col < 0 or col >= 8 or board[row][col] != ' ':
        return False
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ('X' if player == 'O' else 'O'):
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ('X' if player == 'O' else 'O'):
                    r, c = r + dr, c + dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    return True
    return False

def get_valid_moves(board, player):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, player):
                valid_moves.append((row, col))
    return valid_moves

def make_move(board, row, col, player):
    if not is_valid_move(board, row, col, player):
        return False
    board[row][col] = player
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ('X' if player == 'O' else 'O'):
                to_flip = [(row, col)]
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ('X' if player == 'O' else 'O'):
                    to_flip.append((r, c))
                    r, c = r + dr, c + dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                    for r, c in to_flip:
                        board[r][c] = player
    return True

def count_score(board):
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    return x_count, o_count

def is_game_over(board):
    return not any(' ' in row for row in board)

def get_winner(board):
    x_count, o_count = count_score(board)
    if x_count > o_count:
        return 'X'
    elif o_count > x_count:
        return 'O'
    else:
        return 'Tie'

def show_player_history(player):
    history = player_history[player]  
    history_text = f'{player} History:\n'
    for idx, (row, col) in enumerate(history):
        history_text += f'Move {idx + 1}: ({row}, {col})\n'
    canvas.create_text(40, 460, text=history_text, font=("Helvetica", 12), fill="black", tags="board")

def on_canvas_click(event):
    row, col = event.y // 50, event.x // 50
    if is_game_over(board):
        return
    global current_player
    if make_move(board, row, col, current_player):
        if len(player_history[current_player]) >= 5:
            player_history[current_player].pop(0)  # ลบรายการเก่าเมื่อมีเพิ่มรายการใหม่
        player_history[current_player].append((row, col))
        current_player = 'O' if current_player == 'X' else 'X'
        valid_moves = get_valid_moves(board, current_player)
        draw_board(canvas, board, current_player, -1, -1, valid_moves)
        show_player_history(current_player)
        if current_player == 'O':
            if current_mode.get() == "Player vs Computer":
                computer_move()

def computer_move():
    if is_game_over(board):
        return
    global current_player
    valid_moves = get_valid_moves(board, current_player)
    if valid_moves:
        row, col = random.choice(valid_moves)
        if make_move(board, row, col, current_player):
            if len(player_history[current_player]) >= 5:
                player_history[current_player].pop(0)  # ลบรายการเก่าเมื่อมีเพิ่มรายการใหม่
            player_history[current_player].append((row, col))
            current_player = 'O' if current_player == 'X' else 'X'
            valid_moves = get_valid_moves(board, current_player)
            draw_board(canvas, board, current_player, -1, -1, valid_moves)
            show_player_history(current_player)
            update_game()

def new_game():
    global board, current_player, start_time, player_history  # เพิ่ม player_history ในรายการ global
    board = initialize_board()
    current_player = 'X'
    canvas.delete("score")
    draw_board(canvas, board, current_player, -1, -1, get_valid_moves(board, current_player))
    start_time = time.time()
    # ล้างประวัติการเดินทั้ง X และ O
    for player in player_history:
        player_history[player] = []
    update_game()

def update_game():
    canvas.delete("score")
    valid_moves = get_valid_moves(board, current_player)
    draw_board(canvas, board, current_player, -1, -1, valid_moves)
    if not is_game_over(board):
        x_count, o_count = count_score(board)
        canvas.create_text(100, 410, text=f'X: {x_count}', font=("Helvetica", 30), fill="black", tags="score")
        canvas.create_text(300, 410, text=f'O: {o_count}', font=("Helvetica", 30), fill="white", tags="score")
        canvas.create_text(200, 450, text=f'Turn: {current_player}', font=("Helvetica", 20), fill="black", tags="board")
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        canvas.create_text(200, 480, text=f'Time: {minutes:02d}:{seconds:02d}', font=("Helvetica", 20), fill="black", tags="board")
        show_player_history(current_player)
        root.after(1000, update_game)
    else:
        winner = get_winner(board)
        if winner == 'Tie':
            canvas.create_text(200, 450, text="It's a Tie!", font=("Helvetica", 20), fill="black", tags="board")
        else:
            canvas.create_text(200, 450, text=f'Winner: {winner}', font=("Helvetica", 20), fill="black", tags="board")

def main():
    global canvas, board, current_player, root, start_time, current_mode, player_history
    root = Tk()
    root.title("Othello (Reversi)")
    canvas = Canvas(root, width=400, height=500)
    canvas.pack()
    canvas.create_rectangle(0, 0, 400, 400, fill='lightgreen', outline='brown', width=4, tags="board")
    canvas.bind("<Button-1>", on_canvas_click)

    board = initialize_board()
    current_player = 'X'
    start_time = time.time()

    player_history = {
        'X': [],
        'O': []
    }

    current_mode = StringVar()
    current_mode.set("Player vs Computer")

    mode_menu = OptionMenu(root, current_mode, "Player vs Computer", "Player vs Player")
    mode_menu.pack()

    new_game_button = Button(root, text="New Game", command=new_game)
    new_game_button.pack()

    update_game()

    root.mainloop()

if __name__ == "__main__":
    main()
