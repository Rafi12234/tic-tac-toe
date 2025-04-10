import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CELL_SIZE = WIDTH // BOARD_COLS

# Colors
NAVY_BLUE = (30, 30, 100)
NEON_YELLOW = (255, 255, 102)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe vs Computer")
screen.fill(NAVY_BLUE)

# Board
board = [[None for _ in range(BOARD_ROWS)] for _ in range(BOARD_COLS)]

def draw_grid():
    # Horizontal lines
    pygame.draw.line(screen, NEON_YELLOW, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, NEON_YELLOW, (0, 2*CELL_SIZE), (WIDTH, 2*CELL_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, NEON_YELLOW, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, NEON_YELLOW, (2*CELL_SIZE, 0), (2*CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_xo():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, 
                    (col*CELL_SIZE + 50, row*CELL_SIZE + 50),
                    (col*CELL_SIZE + CELL_SIZE - 50, row*CELL_SIZE + CELL_SIZE - 50), 
                    LINE_WIDTH)
                pygame.draw.line(screen, RED,
                    (col*CELL_SIZE + 50, row*CELL_SIZE + CELL_SIZE - 50),
                    (col*CELL_SIZE + CELL_SIZE - 50, row*CELL_SIZE + 50), 
                    LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, GREEN,
                    (col*CELL_SIZE + CELL_SIZE//2, row*CELL_SIZE + CELL_SIZE//2),
                    CELL_SIZE//2 - 50, LINE_WIDTH)

def get_cell(pos):
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

def is_winner(player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_ROWS-i-1] == player for i in range(BOARD_ROWS)):
        return True
    return False

def is_board_full():
    return all(all(cell is not None for cell in row) for row in board)

def show_game_over(message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    font = pygame.font.Font(None, 50)
    text = font.render("Press SPACE to restart", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 50))

def computer_move():
    # Check for winning move
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'O'
                if is_winner('O'):
                    board[row][col] = None
                    return (row, col)
                board[row][col] = None

    # Block player's winning move
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'X'
                if is_winner('X'):
                    board[row][col] = None
                    return (row, col)
                board[row][col] = None

    # Choose random empty cell
    empty_cells = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] is None]
    return random.choice(empty_cells) if empty_cells else None

# Game variables
current_player = 'X'  # Player is X, computer is O
game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == 'X':
            row, col = get_cell(event.pos)
            if board[row][col] is None:
                board[row][col] = 'X'
                
                if is_winner('X'):
                    game_over = True
                elif is_board_full():
                    game_over = True
                else:
                    current_player = 'O'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                # Reset game
                board = [[None for _ in range(BOARD_ROWS)] for _ in range(BOARD_COLS)]
                current_player = 'X'
                game_over = False
                screen.fill(NAVY_BLUE)

    # Computer's turn
    if not game_over and current_player == 'O':
        move = computer_move()
        if move:
            row, col = move
            pygame.time.wait(500)  # Short delay for better UX
            board[row][col] = 'O'
            if is_winner('O'):
                game_over = True
            elif is_board_full():
                game_over = True
            else:
                current_player = 'X'

    # Draw elements
    draw_grid()
    draw_xo()
    
    if game_over:
        if is_winner('X'):
            show_game_over("You Win!")
        elif is_winner('O'):
            show_game_over("Computer Wins!")
        else:
            show_game_over("It's a Tie!")
    
    pygame.display.update()