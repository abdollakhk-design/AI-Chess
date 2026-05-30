import json
from pathlib import Path
import pygame
import chess
from ai_agent import get_best_move

WIDTH, HEIGHT = 640, 640
STATUS_HEIGHT = 140
SQUARE_SIZE = WIDTH // 8
BOARD_COLOR_LIGHT = (238, 238, 210)
BOARD_COLOR_DARK = (118, 150, 86)
HIGHLIGHT_COLOR = (246, 246, 105)
TEXT_COLOR = (20, 20, 20)
PANEL_COLOR = (235, 235, 220)
BASE_DIR = Path(__file__).resolve().parent
PERFORMANCE_FILE = BASE_DIR / "performance.json"

PIECE_COLORS = {
    chess.WHITE: (245, 245, 245),
    chess.BLACK: (35, 35, 35),
}
PIECE_HIGHLIGHT = {
    chess.WHITE: (200, 200, 200),
    chess.BLACK: (70, 70, 70),
}

LEVEL_LABELS = {
    1: "Beginner",
    2: "Intermediate",
    3: "Advanced",
}


def load_performance():
    if not PERFORMANCE_FILE.exists():
        return {"games": 0, "wins": 0, "losses": 0, "draws": 0, "level": 1}
    with open(PERFORMANCE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_performance(data):
    with open(PERFORMANCE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def adapt_level(stats):
    if stats["games"] < 3:
        return stats["level"]
    win_rate = stats["wins"] / stats["games"]
    if win_rate >= 0.66:
        return min(3, stats["level"] + 1)
    if win_rate <= 0.33:
        return max(1, stats["level"] - 1)
    return stats["level"]


def draw_piece_icon(screen, piece, rect):
    fill = PIECE_COLORS[piece.color]
    outline = (15, 15, 15) if piece.color == chess.WHITE else (240, 240, 240)
    detail = PIECE_HIGHLIGHT[piece.color]
    cx, cy = rect.center
    size = rect.width * 0.4
    radius = int(size * 0.35)
    base_h = int(size * 0.25)
    top_y = cy - int(size * 0.3)
    bottom_y = cy + int(size * 0.35)

    if piece.piece_type == chess.PAWN:
        pygame.draw.circle(screen, fill, (cx, top_y), radius)
        pygame.draw.circle(screen, outline, (cx, top_y), radius, 2)
        body = pygame.Rect(cx - int(size * 0.25), top_y, int(size * 0.5), int(size * 0.6))
        pygame.draw.rect(screen, fill, body)
        pygame.draw.rect(screen, outline, body, 2)
        base = pygame.Rect(cx - int(size * 0.35), bottom_y - base_h // 2, int(size * 0.7), base_h)
        pygame.draw.rect(screen, fill, base)
        pygame.draw.rect(screen, outline, base, 2)
    elif piece.piece_type == chess.ROOK:
        tower = pygame.Rect(cx - int(size * 0.35), top_y, int(size * 0.7), int(size * 0.9))
        pygame.draw.rect(screen, fill, tower)
        pygame.draw.rect(screen, outline, tower, 2)
        for i in range(3):
            notch = pygame.Rect(cx - int(size * 0.35) + i * int(size * 0.24), top_y - int(size * 0.2), int(size * 0.18), int(size * 0.18))
            pygame.draw.rect(screen, fill, notch)
            pygame.draw.rect(screen, outline, notch, 2)
        base = pygame.Rect(cx - int(size * 0.45), bottom_y - base_h // 2, int(size * 0.9), base_h)
        pygame.draw.rect(screen, detail, base)
    elif piece.piece_type == chess.KNIGHT:
        head = [
            (cx - int(size * 0.35), bottom_y - int(size * 0.8)),
            (cx - int(size * 0.2), top_y),
            (cx + int(size * 0.3), top_y + int(size * 0.1)),
            (cx + int(size * 0.1), bottom_y - int(size * 0.2)),
            (cx - int(size * 0.2), bottom_y - int(size * 0.1)),
        ]
        pygame.draw.polygon(screen, fill, head)
        pygame.draw.polygon(screen, outline, head, 2)
        pygame.draw.circle(screen, outline, (cx + int(size * 0.15), top_y + int(size * 0.05)), int(size * 0.06))
        base = pygame.Rect(cx - int(size * 0.35), bottom_y - base_h // 2, int(size * 0.7), base_h)
        pygame.draw.rect(screen, detail, base)
    elif piece.piece_type == chess.BISHOP:
        glass = pygame.Rect(cx - int(size * 0.2), top_y, int(size * 0.4), int(size * 0.9))
        pygame.draw.ellipse(screen, fill, glass)
        pygame.draw.ellipse(screen, outline, glass, 2)
        pygame.draw.line(screen, outline, (cx - int(size * 0.15), top_y + int(size * 0.2)), (cx + int(size * 0.15), top_y + int(size * 0.7)), 3)
        base = pygame.Rect(cx - int(size * 0.4), bottom_y - base_h // 2, int(size * 0.8), base_h)
        pygame.draw.rect(screen, detail, base)
    elif piece.piece_type == chess.QUEEN:
        crown = [
            (cx - int(size * 0.35), bottom_y - int(size * 0.45)),
            (cx - int(size * 0.25), top_y + int(size * 0.1)),
            (cx - int(size * 0.1), bottom_y - int(size * 0.55)),
            (cx, top_y),
            (cx + int(size * 0.1), bottom_y - int(size * 0.55)),
            (cx + int(size * 0.25), top_y + int(size * 0.1)),
            (cx + int(size * 0.35), bottom_y - int(size * 0.45)),
        ]
        pygame.draw.polygon(screen, fill, crown)
        pygame.draw.polygon(screen, outline, crown, 2)
        pygame.draw.rect(screen, detail, (cx - int(size * 0.25), bottom_y - int(size * 0.25), int(size * 0.5), int(size * 0.25)))
    elif piece.piece_type == chess.KING:
        crown = [
            (cx - int(size * 0.35), bottom_y - int(size * 0.45)),
            (cx - int(size * 0.25), top_y + int(size * 0.1)),
            (cx - int(size * 0.1), bottom_y - int(size * 0.55)),
            (cx, top_y),
            (cx + int(size * 0.1), bottom_y - int(size * 0.55)),
            (cx + int(size * 0.25), top_y + int(size * 0.1)),
            (cx + int(size * 0.35), bottom_y - int(size * 0.45)),
        ]
        pygame.draw.polygon(screen, fill, crown)
        pygame.draw.polygon(screen, outline, crown, 2)
        pygame.draw.rect(screen, fill, (cx - int(size * 0.05), top_y, int(size * 0.1), int(size * 0.7)))
        pygame.draw.line(screen, outline, (cx, top_y - int(size * 0.05)), (cx, top_y + int(size * 0.2)), 3)
        pygame.draw.line(screen, outline, (cx - int(size * 0.2), top_y + int(size * 0.05)), (cx + int(size * 0.2), top_y + int(size * 0.05)), 3)
        pygame.draw.rect(screen, detail, (cx - int(size * 0.25), bottom_y - int(size * 0.25), int(size * 0.5), int(size * 0.25)))
    else:
        pygame.draw.circle(screen, fill, (cx, cy), radius)
        pygame.draw.circle(screen, outline, (cx, cy), radius, 2)


def draw_board(screen, board, selected_square):
    for rank in range(8):
        for file in range(8):
            color = BOARD_COLOR_LIGHT if (rank + file) % 2 == 0 else BOARD_COLOR_DARK
            rect = pygame.Rect(file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            square = chess.square(file, 7 - rank)
            if selected_square == square:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect)
            piece = board.piece_at(square)
            if piece:
                draw_piece_icon(screen, piece, rect)


def draw_status(screen, board, stats, level):
    pygame.draw.rect(screen, PANEL_COLOR, (0, HEIGHT, WIDTH, STATUS_HEIGHT))
    status_text = "Game over" if board.is_game_over() else "Your turn"
    if board.is_checkmate():
        status_text = "Checkmate"
    elif board.is_stalemate():
        status_text = "Stalemate"
    elif board.is_check():
        status_text = "Check"

    info = [
        f"AI difficulty: {LEVEL_LABELS[level]}",
        f"Games: {stats['games']}  Wins: {stats['wins']}  Losses: {stats['losses']}  Draws: {stats['draws']}",
        status_text,
        "Press R to restart, ESC to exit",
    ]
    for index, line in enumerate(info):
        text = SMALL_FONT.render(line, True, TEXT_COLOR)
        screen.blit(text, (10, HEIGHT + 10 + index * 28))


def position_to_square(pos):
    file = pos[0] // SQUARE_SIZE
    rank = 7 - (pos[1] // SQUARE_SIZE)
    return chess.square(file, rank)


def apply_move(board, move_uci):
    try:
        move = chess.Move.from_uci(move_uci)
        if move in board.legal_moves:
            board.push(move)
            return True
    except ValueError:
        pass
    return False


def play_game():
    pygame.init()
    global FONT, SMALL_FONT
    FONT = pygame.font.SysFont(None, 60)
    SMALL_FONT = pygame.font.SysFont(None, 24)

    screen = pygame.display.set_mode((WIDTH, HEIGHT + STATUS_HEIGHT))
    pygame.display.set_caption("AI-Chess")

    board = chess.Board()
    selected_square = None
    stats = load_performance()
    level = adapt_level(stats)
    running = True
    ai_wait = False
    game_over_recorded = False

    while running:
        screen.fill((240, 240, 240))
        draw_board(screen, board, selected_square)
        draw_status(screen, board, stats, level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    board = chess.Board()
                    selected_square = None
                    stats = load_performance()
                    level = adapt_level(stats)
                    ai_wait = False
                    game_over_recorded = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not board.is_game_over():
                square = position_to_square(pygame.mouse.get_pos())
                if selected_square is None:
                    piece = board.piece_at(square)
                    if piece and piece.color == chess.WHITE:
                        selected_square = square
                else:
                    if (board.piece_at(selected_square).piece_type == chess.PAWN
                            and (chess.square_rank(square) == 0 or chess.square_rank(square) == 7)):
                        move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                    else:
                        move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                        ai_wait = not board.is_game_over()
                    else:
                        selected_square = None

        if ai_wait and not board.is_game_over():
            pygame.time.delay(300)
            move = get_best_move(board, level)
            board.push(move)
            ai_wait = False

        if board.is_game_over() and not game_over_recorded:
            if board.is_checkmate():
                if board.turn == chess.WHITE:
                    stats["losses"] += 1
                else:
                    stats["wins"] += 1
            else:
                stats["draws"] += 1
            stats["games"] += 1
            level = adapt_level(stats)
            save_performance(stats)
            game_over_recorded = True

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    play_game()
