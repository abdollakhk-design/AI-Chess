import random
import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}


def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return -999999 if board.turn else 999999
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        return 0

    score = 0
    for piece_type in PIECE_VALUES:
        score += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]

    return score


def select_move_random(board: chess.Board) -> chess.Move:
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        raise ValueError("No legal moves available")
    return random.choice(legal_moves)


def select_move_greedy(board: chess.Board) -> chess.Move:
    maximizing = board.turn == chess.WHITE
    best_score = -999999 if maximizing else 999999
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        score = evaluate_board(board)
        board.pop()
        if (maximizing and score > best_score) or (not maximizing and score < best_score):
            best_score = score
            best_move = move
    return best_move or select_move_random(board)


def minimax(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing:
        max_eval = -999999
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 999999
        for move in board.legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def select_move_minimax(board: chess.Board, depth: int = 2) -> chess.Move:
    maximizing = board.turn == chess.WHITE
    best_score = -999999 if maximizing else 999999
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, -999999, 999999, board.turn == chess.WHITE)
        board.pop()
        if (maximizing and score > best_score) or (not maximizing and score < best_score):
            best_score = score
            best_move = move
    return best_move or select_move_random(board)


def get_best_move(board: chess.Board, level: int) -> chess.Move:
    if level == 1:
        return select_move_random(board)
    if level == 2:
        return select_move_greedy(board)
    return select_move_minimax(board, depth=2)


if __name__ == "__main__":
    board = chess.Board()
    for level in (1, 2, 3):
        move = get_best_move(board, level)
        print(f"Level {level} best move: {move}")
