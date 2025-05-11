import sys
from engine import GameState, Move
from chessAi import findBestMove, findRandomMoves
from multiprocessing import Queue

def uci_loop():
    try:
        print("Debug: Starting UCI loop")  # Debug
        gs = GameState()
        validMoves = gs.getValidMoves()
        while True:
            command = input().strip()
            print(f"Debug: Received command: {command}")  # Debug
            if command == "uci":
                print("id name MyChessEngine")
                print("id author YourName")
                print("uciok")
            elif command == "isready":
                print("readyok")
            elif command.startswith("position"):
                parts = command.split()
                if parts[1] == "startpos":
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                if "moves" in parts:
                    move_list = parts[parts.index("moves") + 1:]
                    for move in move_list:
                        start_col = ord(move[0]) - ord('a')
                        start_row = 8 - int(move[1])
                        end_col = ord(move[2]) - ord('a')
                        end_row = 8 - int(move[3])
                        for valid_move in validMoves:
                            if (valid_move.startRow == start_row and
                                valid_move.startCol == start_col and
                                valid_move.endRow == end_row and
                                valid_move.endCol == end_col):
                                gs.makeMove(valid_move)
                                break
                        validMoves = gs.getValidMoves()
            elif command.startswith("go"):
                returnQueue = Queue()
                findBestMove(gs, validMoves, returnQueue)
                best_move = returnQueue.get()
                if best_move is None:
                    best_move = findRandomMoves(validMoves)
                uci_move = (chr(best_move.startCol + ord('a')) +
                            str(8 - best_move.startRow) +
                            chr(best_move.endCol + ord('a')) +
                            str(8 - best_move.endRow))
                if best_move.isPawnPromotion:
                    uci_move += "q"
                print(f"bestmove {uci_move}")
            elif command == "quit":
                print("Debug: Quitting")  # Debug
                break
    except Exception as e:
        print(f"Error: {e}")  # Debug

if __name__ == "__main__":
    uci_loop()