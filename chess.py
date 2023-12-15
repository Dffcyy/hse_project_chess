import pygame

pygame.init()

width = 640
height = 720
screen = pygame.display.set_mode([width, height])
font = pygame.font.Font('freesansbold.ttf', 20)
big_fond = pygame.font.Font('freesansbold.ttf', 45)
timer = pygame.time.Clock()
fps = 60

# загружаем текстуры черных фигур
black_queen = pygame.image.load('assets/images/bQ.png')
black_queen = pygame.transform.scale(black_queen, (60, 60))
black_king = pygame.image.load('assets/images/bK.png')
black_king = pygame.transform.scale(black_king, (60, 60))
black_rook = pygame.image.load('assets/images/bR.png')
black_rook = pygame.transform.scale(black_rook, (60, 60))
black_pawn = pygame.image.load('assets/images/bp.png')
black_pawn = pygame.transform.scale(black_pawn, (60, 60))
black_bishop = pygame.image.load('assets/images/bB.png')
black_bishop = pygame.transform.scale(black_bishop, (60, 60))
black_knight = pygame.image.load('assets/images/bN.png')
black_knight = pygame.transform.scale(black_knight, (60, 60))

# загружаем текстуры белых фигур
white_queen = pygame.image.load('assets/images/wQ.png')
white_queen = pygame.transform.scale(white_queen, (60, 60))
white_king = pygame.image.load('assets/images/wK.png')
white_king = pygame.transform.scale(white_king, (60, 60))
white_rook = pygame.image.load('assets/images/wR.png')
white_rook = pygame.transform.scale(white_rook, (60, 60))
white_pawn = pygame.image.load('assets/images/wp.png')
white_pawn = pygame.transform.scale(white_pawn, (60, 60))
white_bishop = pygame.image.load('assets/images/wB.png')
white_bishop = pygame.transform.scale(white_bishop, (60, 60))
white_knight = pygame.image.load('assets/images/wN.png')
white_knight = pygame.transform.scale(white_knight, (60, 60))

white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                  (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                  (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]

# 0 - белый ход, не выбрал: 1 - белый ход, выбрал: 2 - черный ход, не выбрал: 3 - черный ход, выбрал
turn_step = 0
selection = 100
valid_moves = []

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

"""
    Рисует основную шахматную доску и статус игры.

    Входные данные:
    Нет входных данных.

    Выходные данные:
    Нет выходных данных.
    """
def draw_board():
    for i in range(32):
        colonm = i % 4
        row = i // 4
        if row % 2 == 0:    # 1 если сдвиг вниз на 1
            pygame.draw.rect(screen, 'light gray', [(colonm * 160), row * 80, 80, 80])
        else:
            pygame.draw.rect(screen, 'light gray', [80 + (colonm * 160), row * 80, 80, 80])
        pygame.draw.rect(screen, 'gray', [0, 640, width, 80])
        pygame.draw.rect(screen, 'black', [0, 640, width, 80], 3)
        status_text = ['Белые: выбирают фигуру', 'Белые: выбирают ход',
                       'Черные: выбирают фигуру', 'Черные: выбирают ход']
        screen.blit(big_fond.render(status_text[turn_step], True, 'black'), (20, 660))

"""
    Рисует фигуры на шахматной доске.

    Входные данные:
    Нет входных данных.

    Выходные данные:
    Нет выходных данных.
    """
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        screen.blit(white_images[index], (white_locations[i][0] * 80 + 10, white_locations[i][1] * 80 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0]*80, white_locations[i][1]*80, 80, 80], 2)
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        screen.blit(black_images[index], (black_locations[i][0] * 80 + 10, black_locations[i][1] * 80 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [black_locations[i][0]*80, black_locations[i][1]*80, 80, 80], 2)

"""
    Проверяет возможные ходы для каждой фигуры.

    Входные данные:
    - pieces (list): Список фигур.
    - locations (list): Список текущего расположения фигур.
    - color (str): Цвет фигур ('white' или 'black').

    Выходные данные:
    list: Список возможных ходов для каждой фигуры.
"""
def check_all_moves(pieces,locations,color):
    moves = []
    all_moves = []
    for i in range (len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves = check_pawn(location, color)
        elif piece == 'queen':
            moves = check_queen(location, color)
        elif piece == 'king':
            moves = check_king(location, color)
        elif piece == 'knight':
            moves = check_knight(location, color)
        elif piece == 'rook':
            moves = check_rook(location, color)
        elif piece == 'bishop':
            moves = check_bishop(location, color)
        all_moves.append(moves)
    return all_moves

"""
    Проверяет возможные ходы для пешки.

    Входные данные:
    - position (tuple): Текущее положение пешки.
    - color (str): Цвет пешки ('white' или 'black').

    Выходные данные:
    list: Список возможных ходов для пешки.
"""
def check_pawn(position,color):
    moves = []
    count = 0
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves.append((position[0], position[1] + 1))
        if (position[0], position[1] + 1) in white_locations:
            count += 1
        if (position[0], position[1] + 2) not in white_locations and (position[0], position[1] + 2) not in black_locations and position[1] == 1 and count == 0:
            moves.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves.append((position[0], position[1] - 1))
        if (position[0], position[1] - 1) in black_locations:
            count += 1
        if (position[0], position[1] - 2) not in white_locations and (position[0], position[1] - 2) not in black_locations and position[1] == 6 and count == 0:
            moves.append((position[0], position[1] - 2))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves.append((position[0] - 1, position[1] - 1))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves.append((position[0] + 1, position[1] - 1))
    return moves


"""
    Проверяет возможные ходы для ладьи.

    Входные данные:
    - position (tuple): Текущее положение ладьи.
    - color (str): Цвет ладьи ('white' или 'black').

    Выходные данные:
    list: Список возможных ходов для ладьи.
"""
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

"""
    Проверяет возможные ходы для коня.

    Входные данные:
    - position (tuple): Текущее положение коня.
    - color (str): Цвет коня ('white' или 'black').

    Выходные данные:
    list: Список возможных ходов для коня.
"""
def check_knight(position, color):
    moves = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 клеток для проверки наличия коней, они могут пройти две клетки в одном направлении и одну в другом
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves.append(target)
    return moves

"""
    Проверяет возможные ходы для короля.

    Входные данные:
    - position (tuple): Текущее положение короля.
    - color (str): Цвет короля ('white' или 'black').

    Выходные данные:
    list: Список возможных ходов для короля.
"""
def check_king(position, color):
    moves = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 клеток для проверки наличия королей, они могут пройти на одну клетку в любом направлении
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves.append(target)
    return moves

"""
    Проверяет возможные ходы для слона.

    Входные данные:
    - position (tuple): Текущее положение слона.
    - color (str): Цвет слона ('white' или 'black').

    Выходные данные:
    list: Список возможных ходов для слона.
"""
def check_bishop(position, color):
    moves = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves

"""
    Проверяет возможные ходы для ферзя.

    Входные данные:
    - position (tuple): Текущее положение ферзя.
    - color (str): Цвет ферзя ('white' или 'black').

    Выходные данные:
    list: Список возможных ходов для ферзя.
"""
def check_queen(position, color):
    moves = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves.append(second_list[i])
    return moves

"""
    Проверяет возможные ходы для выбранной фигуры.

    Входные данные:
    Нет входных данных.

    Выходные данные:
    list: Список возможных ходов для выбранной фигуры.
"""
def check_valid_moves():
    if turn_step < 2:
        options = white_moves
    else:
        options = black_moves
    valid_options = options[selection]
    return valid_options

"""
    Рисует возможные ходы на экране.

    Входные данные:
    - moves (list): Список координат возможных ходов.

    Выходные данные:
    Нет выходных данных.
"""
def draw_valid(moves):
    color = 'red'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 5)


"""
    Генерирует строку с информацией о ходе.

Входные данные:
    - start (tuple): Начальные координаты фигуры.
    - end (tuple): Конечные координаты фигуры.
    - color (str): Цвет фигуры ('W' или 'B').
    - figure (str): Тип фигуры.

    Выходные данные:
    str: Строка с информацией о ходе.
"""
def turns(start, end, color, figure):
    num_abc = {0: 'H', 1: 'G', 2: 'F', 3: 'E', 4: 'D', 5: 'C', 6: 'B', 7: 'A'}
    num_num = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'}
    return color + figure + ': ' + num_abc[start[0]] + num_num[start[1]] + ' - ' + num_abc[end[0]] + num_num[end[1]]

"""
выводим на экран табличку кто выиграл
"""
def draw_game_over():
    pygame.draw.rect(screen, 'black', [95,285,450,70])
    screen.blit(font.render(f'{winner} выиграли', True, 'white'), (220, 295))
    screen.blit(font.render(f'Нажмите enter чтобы перезапустить игру', True, 'white'), (110, 325))
"""
основная игра
"""
black_moves = check_all_moves(black_pieces, black_locations, 'black')
white_moves = check_all_moves(white_pieces, white_locations, 'white')
game = True
game_over = False
winner = ''
while game:
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                turn_step = 0
                selection = 100
                valid_moves = []
                black_moves = check_all_moves(black_pieces, black_locations, 'black')
                white_moves = check_all_moves(white_pieces, white_locations, 'white')
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x = event.pos[0] // 80
            y = event.pos[1] // 80
            click_xy = (x, y)
            if turn_step <= 1:
                if click_xy in white_locations:
                    selection = white_locations.index(click_xy)
                    start = click_xy
                    if turn_step == 0:
                        turn_step = 1
                if click_xy in valid_moves and selection != 100:
                    white_locations[selection] = click_xy
                    active_figure = white_pieces[selection]
                    end = click_xy
                    print(turns(start, end, 'W', active_figure))
                    if white_pieces[selection] == 'pawn' and white_locations[selection][1] == 7:
                        white_pieces[selection] = 'queen'
                    if click_xy in black_locations:
                        black_piece = black_locations.index(click_xy)
                        if black_pieces[black_piece] == 'king':
                            winner = 'Белые'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_moves = check_all_moves(black_pieces, black_locations, 'black')
                    white_moves = check_all_moves(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_xy in black_locations:
                    selection = black_locations.index(click_xy)
                    start = click_xy
                    if turn_step == 2:
                        turn_step = 3
                if click_xy in valid_moves and selection != 100:
                    black_locations[selection] = click_xy
                    active_figure = black_pieces[selection]
                    end = click_xy
                    print(turns(start, end, 'B', active_figure))
                    if black_pieces[selection] == 'pawn' and black_locations[selection][1] == 0:
                        black_pieces[selection] = 'queen'
                    if click_xy in white_locations:
                        white_piece = white_locations.index(click_xy)
                        if white_pieces[white_piece] == 'king':
                            winner = 'Черные'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_moves = check_all_moves(black_pieces, black_locations, 'black')
                    white_moves = check_all_moves(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
    if winner != '':
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()