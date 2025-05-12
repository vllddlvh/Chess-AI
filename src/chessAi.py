import random
import json
import os
pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 2, 2, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 2, 1, 1, 2, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N": knightScores, "B": bishopScores, "Q": queenScores,
                       "R": rookScores, "wp": whitePawnScores, "bp": blackPawnScores}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
SET_WHITE_AS_BOT = -1


def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves, returnQueue):
    """Hàm này giờ gọi đến hàm cải tiến."""
    find_best_move_with_improvements(gs, validMoves, returnQueue)


# with alpha beta pruning
'''
alpha is keeping track of maximum so far
beta is keeping track of minimum so far
'''


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # (will add later) move ordering - like evaluate all the move first that results in check or evaluate all the move first that results in capturing opponent's queen

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()  # opponent validmoves
        '''
        negative sign because what ever opponents best score is, is worst score for us
        negative turnMultiplier because it changes turns after moves made 
        -beta, -alpha (new max, new min) our max become opponents new min and our min become opponents new max
        '''
        score = - \
            findMoveNegaMaxAlphaBeta(
                gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore  # alpha is the new max
        if alpha >= beta:  # if we find new max is greater than minimum so far in a branch then we stop iterating in that branch as we found a worse move in that branch
            break
    return maxScore


'''
Positive score is good for white
Negative score is good for black
'''


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            gs.checkmate = False
            return -CHECKMATE  # black wins
        else:
            gs.checkmate = False
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                # score positionally based on piece type
                if square[1] != "K":
                    # return score of the piece at that position
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if SET_WHITE_AS_BOT:
                    if square[0] == 'w':
                        score += pieceScore[square[1]] + \
                            piecePositionScore * .1
                    elif square[0] == 'b':
                        score -= pieceScore[square[1]] + \
                            piecePositionScore * .1
                else:
                    if square[0] == 'w':
                        score -= pieceScore[square[1]] + \
                            piecePositionScore * .1
                    elif square[0] == 'b':
                        score += pieceScore[square[1]] + \
                            piecePositionScore * .1

    return score

# -------------------- OPENING BOOK IMPLEMENTATION --------------------

class OpeningBook:
    def __init__(self, file_path="C:\\Users\\ADMIN\\Chess-AI\\src\\opening_book.json"):
        """Initialize an opening book from a JSON file or create a new one."""
        self.file_path = file_path
        self.openings = {}
        self.load_openings()
    
    def load_openings(self):
        """Load opening moves from a JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    self.openings = json.load(f)
                print(f"Opening book loaded with {len(self.openings)} positions")
            except Exception as e:
                print(f"Error loading opening book: {e}")
                self.openings = {}
                self.create_default_openings()
        else:
            print("No opening book found, creating default openings")
            self.create_default_openings()
            self.save_openings()
    
    def create_default_openings(self):
        """Create some basic opening moves."""
        # Format: Board FEN (or simplified position string) -> list of good moves
        # For simplicity, we'll use just the move history as the key
        
        # Starting position
        self.openings[""] = [
            {"move": "e2e4", "weight": 10, "name": "King's Pawn Opening"},
            {"move": "d2d4", "weight": 10, "name": "Queen's Pawn Opening"},
            {"move": "c2c4", "weight": 8, "name": "English Opening"},
            {"move": "g1f3", "weight": 7, "name": "Réti Opening"}
        ]
        
        # After 1.e4
        self.openings["e2e4"] = [
            {"move": "e7e5", "weight": 10, "name": "Open Game"},
            {"move": "c7c5", "weight": 10, "name": "Sicilian Defense"},
            {"move": "e7e6", "weight": 8, "name": "French Defense"},
            {"move": "c7c6", "weight": 7, "name": "Caro-Kann Defense"}
        ]
        
        # After 1.d4
        self.openings["d2d4"] = [
            {"move": "d7d5", "weight": 10, "name": "Closed Game"},
            {"move": "g8f6", "weight": 9, "name": "Indian Defense"},
            {"move": "f7f5", "weight": 7, "name": "Dutch Defense"}
        ]
        
        # Some popular continuations
        self.openings["e2e4 e7e5"] = [
            {"move": "g1f3", "weight": 10, "name": "King's Knight Opening"}
        ]
        
        self.openings["e2e4 e7e5 g1f3"] = [
            {"move": "b8c6", "weight": 10, "name": "Two Knights Defense"},
            {"move": "g8f6", "weight": 8, "name": "Petrov's Defense (continuation)"}
        ]
        
        self.openings["e2e4 c7c5"] = [
            {"move": "g1f3", "weight": 10, "name": "Open Sicilian"},
            {"move": "b1c3", "weight": 8, "name": "Closed Sicilian"},
            {"move": "c2c3", "weight": 7, "name": "Alapin Sicilian"}
        ]
        
        # Add more openings as needed
    
    def save_openings(self):
        """Save the opening book to a JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.openings, f, indent=4)
            print(f"Opening book saved to {self.file_path}")
        except Exception as e:
            print(f"Error saving opening book: {e}")
    
    def get_move(self, move_history):
        """
        Get a move from the opening book based on the current move history.
        
        Args:
            move_history: A string of moves in algebraic notation separated by spaces
                         (e.g., "e2e4 e7e5 g1f3")
        
        Returns:
            A move object or None if no move is found in the book
        """
        # Simplify the move history to use as a key
        key = " ".join([move for move in move_history.split()])
        
        if key in self.openings and self.openings[key]:
            # Select a move based on weights
            moves = self.openings[key]
            total_weight = sum(move["weight"] for move in moves)
            r = random.uniform(0, total_weight)
            cumulative_weight = 0
            
            for move in moves:
                cumulative_weight += move["weight"]
                if r <= cumulative_weight:
                    print(f"Using opening book: {move['name']}")
                    return move["move"]
        
        return None
    
    def add_move(self, move_history, move, weight=5, name="Custom"):
        """Add a new move to the opening book."""
        key = " ".join([move for move in move_history.split()])
        
        if key not in self.openings:
            self.openings[key] = []
        
        # Check if the move already exists
        for existing in self.openings[key]:
            if existing["move"] == move:
                existing["weight"] = weight
                existing["name"] = name
                self.save_openings()
                return
        
        # Add new move
        self.openings[key].append({
            "move": move,
            "weight": weight,
            "name": name
        })
        self.save_openings()

# -------------------- ZOBRIST HASHING & TRANSPOSITION TABLE --------------------

class ZobristHashing:
    def __init__(self):
        """Initialize Zobrist hashing with random bitstrings."""
        self.piece_codes = {"wp": 0, "wN": 1, "wB": 2, "wR": 3, "wQ": 4, "wK": 5,
                           "bp": 6, "bN": 7, "bB": 8, "bR": 9, "bQ": 10, "bK": 11}
        
        # Initialize random numbers for each piece at each position
        random.seed(42)  # For consistency between runs
        self.piece_position_keys = [[[random.getrandbits(64) for _ in range(12)]  # 12 piece types
                                    for _ in range(8)]  # 8 columns
                                   for _ in range(8)]  # 8 rows
        
        # Random number for side to move
        self.black_to_move_key = random.getrandbits(64)
        
        # Random numbers for castling rights
        self.castling_keys = [random.getrandbits(64) for _ in range(4)]  # K, Q, k, q
        
        # Random numbers for en passant file
        self.en_passant_keys = [random.getrandbits(64) for _ in range(8)]  # 8 files
    
    def compute_hash(self, board, white_to_move, castling_rights, en_passant_square):
        """
        Compute Zobrist hash for the current board position.
        
        Args:
            board: 2D array representing the chess board
            white_to_move: Boolean indicating if it's white's turn
            castling_rights: A string containing castling availability (e.g., "KQkq")
            en_passant_square: The en passant target square or None
            
        Returns:
            A 64-bit integer hash
        """
        h = 0
        
        # XOR in the pieces
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != "--":
                    piece_type = piece[0] + piece[1]  # e.g., "wp", "bK"
                    if piece_type in self.piece_codes:
                        h ^= self.piece_position_keys[row][col][self.piece_codes[piece_type]]
        
        # XOR in the side to move
        if not white_to_move:
            h ^= self.black_to_move_key
        
        # XOR in the castling rights
        if 'K' in castling_rights:
            h ^= self.castling_keys[0]
        if 'Q' in castling_rights:
            h ^= self.castling_keys[1]
        if 'k' in castling_rights:
            h ^= self.castling_keys[2]
        if 'q' in castling_rights:
            h ^= self.castling_keys[3]
        
        # XOR in the en passant square
        if en_passant_square:
            file = ord(en_passant_square[0]) - ord('a')  # Convert file letter to 0-7
            h ^= self.en_passant_keys[file]
        
        return h

class TranspositionTable:
    def __init__(self, max_size=1000000):
        """Initialize the transposition table with a maximum size."""
        self.max_size = max_size
        self.table = {}  # hash -> (depth, flag, score, move)
        self.zobrist = ZobristHashing()
    
    def store(self, board, white_to_move, castling_rights, en_passant_square, depth, flag, score, move):
        """
        Store a position in the transposition table.
        
        Args:
            board, white_to_move, castling_rights, en_passant_square: Position data
            depth: Search depth remaining at this position
            flag: Type of node (EXACT, UPPERBOUND, LOWERBOUND)
            score: Score at this position
            move: Best move at this position
        """
        # If table is full, remove the oldest entries (simple LRU policy)
        if len(self.table) >= self.max_size:
            # Remove 10% of the oldest entries
            remove_count = int(self.max_size * 0.1)
            for _ in range(remove_count):
                self.table.pop(next(iter(self.table)))
        
        # Compute position hash
        pos_hash = self.zobrist.compute_hash(board, white_to_move, castling_rights, en_passant_square)
        
        # Store the position
        self.table[pos_hash] = (depth, flag, score, move)
    
    def lookup(self, board, white_to_move, castling_rights, en_passant_square):
        """
        Look up a position in the transposition table.
        
        Args:
            board, white_to_move, castling_rights, en_passant_square: Position data
            
        Returns:
            (depth, flag, score, move) or None if not found
        """
        pos_hash = self.zobrist.compute_hash(board, white_to_move, castling_rights, en_passant_square)
        return self.table.get(pos_hash)
    
    def clear(self):
        """Clear the transposition table."""
        self.table.clear()

# -------------------- UTILITY FUNCTIONS --------------------

def move_to_algebraic(move):
    """Convert a move from the format (startRow, startCol, endRow, endCol) to algebraic notation (e.g., 'e2e4')."""
    start_row, start_col, end_row, end_col = move.startRow, move.startCol, move.endRow, move.endCol
    # Convert to algebraic notation
    files = 'abcdefgh'
    ranks = '87654321'  # Chess board is numbered from 8 to 1 from top to bottom
    
    return f"{files[start_col]}{ranks[start_row]}{files[end_col]}{ranks[end_row]}"

def algebraic_to_move(algebraic, Move):
    """Convert algebraic notation (e.g., 'e2e4') to a Move object."""
    files = 'abcdefgh'
    ranks = '87654321'
    
    start_col = files.index(algebraic[0])
    start_row = ranks.index(algebraic[1])
    end_col = files.index(algebraic[2])
    end_row = ranks.index(algebraic[3])
    
    # Create a new Move object (assuming the Move class constructor looks like this)
    return Move((start_row, start_col), (end_row, end_col), None)

# Integration function to modify findBestMove
def find_best_move_with_improvements(gs, valid_moves, return_queue):
    """Enhanced version of findBestMove that uses the opening book and transposition table."""
    global next_move
    next_move = None
    
    # Check if we can use an opening book move
    move_history = " ".join([move_to_algebraic(move) for move in gs.moveLog])
    opening_book = OpeningBook()
    book_move = opening_book.get_move(move_history)
    
    if book_move:
        # Convert the algebraic move to a Move object
        for move in valid_moves:
            if move_to_algebraic(move) == book_move:
                next_move = move
                return_queue.put(next_move)
                return
    
    # If no opening book move is available, use the enhanced alpha-beta search
    random.shuffle(valid_moves)
    
    # Create or get a transposition table
    if not hasattr(find_best_move_with_improvements, "tt"):
        find_best_move_with_improvements.tt = TranspositionTable()
    
    # Determine multiplier based on side to move
    set_white_as_bot = 1 if gs.whiteToMove else -1
    
    # Perform alpha-beta search with transposition table
    find_move_alpha_beta_with_tt(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, set_white_as_bot, find_best_move_with_improvements.tt)
    
    return_queue.put(next_move)

# Alpha-beta search with transposition table
def find_move_alpha_beta_with_tt(gs, valid_moves, depth, alpha, beta, turn_multiplier, tt):
    global next_move
    
    # Check transposition table
    tt_result = tt.lookup(gs.board, gs.whiteToMove, gs.getCastlingRights(), gs.getEnPassantSquare())
    
    if tt_result and tt_result[0] >= depth:
        depth_stored, flag, score, move = tt_result
        
        if flag == "EXACT":
            if depth == DEPTH:
                next_move = move
            return score
        elif flag == "LOWERBOUND" and score >= beta:
            return score
        elif flag == "UPPERBOUND" and score <= alpha:
            return score
    
    if depth == 0:
        return turn_multiplier * scoreBoard(gs)
    
    # Move ordering: prioritize captures and checks
    ordered_moves = order_moves(gs, valid_moves)
    
    max_score = -CHECKMATE
    best_move = None
    
    for move in ordered_moves:
        gs.makeMove(move)
        next_moves = gs.getValidMoves()
        
        score = -find_move_alpha_beta_with_tt(gs, next_moves, depth-1, -beta, -alpha, -turn_multiplier, tt)
        
        gs.undoMove()
        
        if score > max_score:
            max_score = score
            best_move = move
            if depth == DEPTH:
                next_move = move
                print(f"Current best: {move_to_algebraic(move)}, score: {score}")
        
        if max_score > alpha:
            alpha = max_score
        
        if alpha >= beta:
            break
    
    # Store position in transposition table
    flag = "EXACT"
    if max_score <= alpha:
        flag = "UPPERBOUND"
    if max_score >= beta:
        flag = "LOWERBOUND"
    
    tt.store(gs.board, gs.whiteToMove, gs.getCastlingRights(), gs.getEnPassantSquare(), 
             depth, flag, max_score, best_move)
    
    return max_score

def order_moves(gs, moves):
    """Order moves to improve alpha-beta pruning efficiency."""
    # Simple heuristic: prioritize captures, especially high-value captures
    move_scores = []
    
    for move in moves:
        score = 0
        # Prioritize captures by MVV-LVA (Most Valuable Victim - Least Valuable Aggressor)
        if gs.board[move.endRow][move.endCol] != "--":
            # Capturing a piece
            victim_score = pieceScore.get(gs.board[move.endRow][move.endCol][1], 0)
            aggressor_score = pieceScore.get(gs.board[move.startRow][move.startCol][1], 0)
            
            if aggressor_score > 0:
                score = 10 * victim_score - aggressor_score
            else:
                score = 10 * victim_score
        
        # Prioritize pawn promotions
        if move.isPawnPromotion:
            score += 900  # Queen promotion value
        
        # Prioritize center control in early game (first 10 moves)
        if len(gs.moveLog) < 10:
            # Center squares are more valuable
            if 2 <= move.endRow <= 5 and 2 <= move.endCol <= 5:
                score += 10
            if 3 <= move.endRow <= 4 and 3 <= move.endCol <= 4:
                score += 10
        
        move_scores.append((move, score))
    
    # Sort moves by score in descending order
    move_scores.sort(key=lambda x: x[1], reverse=True)
    return [move for move, score in move_scores]

# Sample implementation for required methods in GameState class
def getCastlingRights(self):
    """Get the current castling rights."""
    rights = ""
    if self.currentCastlingRight.wks:
        rights += "K"
    if self.currentCastlingRight.wqs:
        rights += "Q"
    if self.currentCastlingRight.bks:
        rights += "k"
    if self.currentCastlingRight.bqs:
        rights += "q"
    return rights if rights else "-"

def getEnPassantSquare(self):
    """Get the current en passant square in algebraic notation."""
    if self.enpassantPossible:
        files = 'abcdefgh'
        ranks = '87654321'
        col = self.enpassantPossible[1]
        row = self.enpassantPossible[0]
        return files[col] + ranks[row]
    return None