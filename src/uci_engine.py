import sys
import chess
import chess.engine
from engine import GameState, Move
from chessAi import findBestMove
from multiprocessing import Queue

def uci_loop():
    gs = GameState()
    print("id name MyChessAI")
    print("id author YourName")
    print("uciok")

    while True:
        line = sys.stdin.readline().strip()
        if line == "uci":
            print("id name MyChessAI")
            print("id author YourName")
            print("uciok")
        elif line == "isready":
            print("readyok")
        elif line.startswith("position"):
            handle_position(line, gs)
        elif line.startswith("go"):
            make_move(gs)
        elif line == "quit":
            break

def handle_position(command, gs):
    if "startpos" in command:
        gs.__init__()  # reset game state
        moves = command.split("moves")[1].strip().split() if "moves" in command else []
    elif "fen" in command:
        # Chưa hỗ trợ FEN input trong GameState, nên chỉ dùng startpos
        print("info string FEN input not supported yet", file=sys.stderr)
        return

    for move_str in moves:
        move = uci_to_move(gs, move_str)
        if move:
            gs.makeMove(move)

def make_move(gs):
    validMoves = gs.getValidMoves()
    returnQueue = Queue()
    findBestMove(gs, validMoves, returnQueue)
    best_move = returnQueue.get()

    if best_move:
        move_str = move_to_uci(best_move)
        print(f"bestmove {move_str}")
    else:
        print("bestmove 0000")

def uci_to_move(gs, move_str):
    if len(move_str) < 4:
        return None
    startCol = ord(move_str[0]) - ord('a')
    startRow = 8 - int(move_str[1])
    endCol = ord(move_str[2]) - ord('a')
    endRow = 8 - int(move_str[3])
    for move in gs.getValidMoves():
        if (move.startRow, move.startCol) == (startRow, startCol) and (move.endRow, move.endCol) == (endRow, endCol):
            return move
    return None

def move_to_uci(move):
    return f"{chr(move.startCol + ord('a'))}{8 - move.startRow}{chr(move.endCol + ord('a'))}{8 - move.endRow}"

if __name__ == "__main__":
    uci_loop()
