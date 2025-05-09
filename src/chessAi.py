'''
    Keep DEPTH <= 4 for AI to run smoothly.

    DEPTH means the fot will looks depth moves ahead and calculate the best possible move based on PIECE-CAPTURE-SCORE AND PIECE-POSITION SCORE :
    DEPTH = 4
'''


'''

WAYS TO IMPROVE AI AND MAKE AI FASTER

1) Create a database for initial ai moves/ book openings
2) AI find possible moves for all the piece after each move, if one piece is moved possible moves for other piece would be same no need to find again
    In this case new possible move would be :
        i) if any piece could move to the starting location of piece moved
        ii) if the piece moved to (x, y) position check if it blocked any piece to move to that location
3) no need to evaluate all the position again and again use zobrus hashing to save good position and depth
4) if [ black moved x, white move a, black moved y, white move b ] is sometime same as: 
      [ black moved y, white move a, black moved x, white move b ]
      [ black moved x, white move b, black moved y, white move a ]
      [ black moved y, white move b, black moved y, white move a ]
5) Teach theories to AI, like some time it is better to capture threat than to move a pawn or take back our piece to previous position rather than attacking


'''


import random
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
    global nextMove, whitePawnScores, blackPawnScores
    nextMove = None
    random.shuffle(validMoves)

    if gs.playerWantsToPlayAsBlack:
        # Swap the variables
        whitePawnScores, blackPawnScores = blackPawnScores, whitePawnScores

    SET_WHITE_AS_BOT = 1 if gs.whiteToMove else -1

    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -
                             CHECKMATE, CHECKMATE,  SET_WHITE_AS_BOT)

    returnQueue.put(nextMove)


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

'''
    Enhanced Chess AI with multiple improvements:
    1. Opening book implementation
    2. Zobrist hashing for position caching
    3. More sophisticated evaluation function
    4. Move ordering for better alpha-beta pruning performance
    5. Iterative deepening
    6. Quiescence search to handle tactical positions
    7. Improved time management
'''

import random
import time
from collections import OrderedDict, defaultdict

# Piece scores - slightly modified values
pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}

# Advanced position-based evaluation tables
# Pawns - encouraged to advance and control center
whitePawnScores = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

blackPawnScores = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [5, 10, 10,-20,-20, 10, 10,  5],
    [5, -5,-10,  0,  0,-10, -5,  5],
    [0,  0,  0, 20, 20,  0,  0,  0],
    [5,  5, 10, 25, 25, 10,  5,  5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

# Knights - encouraged to stay in center, penalized at edges
knightScores = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

# Bishops - encouraged to control diagonals
bishopScores = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5,  5,  5,  5,  5,-10],
    [-10,  0,  5,  0,  0,  5,  0,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

# Rooks - encouraged to control open files and 7th rank
rookScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

# Queens - combination of rook and bishop mobility
queenScores = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-5,  0,  5,  5,  5,  5,  0, -5],
    [0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

# Kings - different tables for middlegame and endgame
kingMiddlegameScores = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [20, 20,  0,  0,  0,  0, 20, 20],
    [20, 30, 10,  0,  0, 10, 30, 20]
]

kingEndgameScores = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

piecePositionScores = {
    "N": knightScores,
    "B": bishopScores,
    "Q": queenScores,
    "R": rookScores,
    "wp": whitePawnScores,
    "bp": blackPawnScores,
    "wK_mid": kingMiddlegameScores,
    "bK_mid": kingMiddlegameScores,
    "wK_end": kingEndgameScores,
    "bK_end": kingEndgameScores
}

# Constants for scoring
CHECKMATE = 100000
STALEMATE = 0
DEFAULT_DEPTH = 4  # Can be adjusted based on hardware capabilities
QUIESCENCE_DEPTH = 4  # Maximum depth for quiescence search

# Opening book - simple implementation
OPENING_BOOK = {
    "": ["e2e4", "d2d4", "c2c4", "g1f3"],  # Start position
    "e2e4": ["e7e5", "c7c5", "e7e6", "c7c6"],  # Responses to e4
    "d2d4": ["d7d5", "g8f6", "e7e6", "c7c5"],  # Responses to d4
    "c2c4": ["e7e5", "c7c5", "g8f6"],          # Responses to c4
    "g1f3": ["d7d5", "g8f6", "c7c5"]           # Responses to Nf3
}

# Zobrist hashing constants
ZOBRIST_KEYS = None
POSITION_CACHE = {}  # Cache for positions already evaluated

def init_zobrist():
    """Initialize Zobrist hashing keys"""
    global ZOBRIST_KEYS
    
    # If already initialized, return
    if ZOBRIST_KEYS is not None:
        return
        
    import random
    random.seed(42)  # For reproducibility
    
    ZOBRIST_KEYS = {}
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    
    # Keys for each piece on each square
    for piece in pieces:
        ZOBRIST_KEYS[piece] = [[random.getrandbits(64) for _ in range(8)] for _ in range(8)]
    
    # Key for side to move
    ZOBRIST_KEYS['side'] = random.getrandbits(64)
    
    # Keys for castling rights
    ZOBRIST_KEYS['wk_castle'] = random.getrandbits(64)
    ZOBRIST_KEYS['wq_castle'] = random.getrandbits(64)
    ZOBRIST_KEYS['bk_castle'] = random.getrandbits(64)
    ZOBRIST_KEYS['bq_castle'] = random.getrandbits(64)
    
    # Keys for en passant file
    ZOBRIST_KEYS['enpassant'] = [random.getrandbits(64) for _ in range(8)]

def compute_zobrist_hash(gs):
    """Compute the Zobrist hash for the current board position"""
    if ZOBRIST_KEYS is None:
        init_zobrist()
        
    h = 0
    
    # Hash pieces on board
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece != "--":
                h ^= ZOBRIST_KEYS[piece][r][c]
    
    # Hash side to move
    if gs.whiteToMove:
        h ^= ZOBRIST_KEYS['side']
    
    # Hash castling rights (simplified - would need to track these in game state)
    # if gs.whiteCastleKingside:
    #     h ^= ZOBRIST_KEYS['wk_castle']
    # ... other castling rights
    
    # Hash en passant square (simplified)
    if gs.enpassantPossible:
        col = gs.enpassantPossible[1]
        h ^= ZOBRIST_KEYS['enpassant'][col]
    
    return h

def is_endgame(gs):
    """Determine if the current position is in the endgame phase"""
    # Count major pieces (queens and rooks)
    white_major_pieces = 0
    black_major_pieces = 0
    
    for row in gs.board:
        for square in row:
            if square == "wQ" or square == "wR":
                white_major_pieces += 1
            elif square == "bQ" or square == "bR":
                black_major_pieces += 1
    
    # If both sides have 1 or fewer major pieces, it's likely an endgame
    return white_major_pieces <= 1 and black_major_pieces <= 1

def findBestMove(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    
    # Initialize zobrist hashing
    init_zobrist()
    
    # Check opening book first
    if len(gs.moveLog) < 6:  # Only use opening book for first few moves
        book_move = check_opening_book(gs)
        if book_move:
            for move in validMoves:
                if move_to_string(move, gs) == book_move:
                    returnQueue.put(move)
                    return
    
    # Iterative deepening - gradually increase depth
    for current_depth in range(2, DEFAULT_DEPTH + 1):
        start_time = time.time()
        findMoveNegaMaxAlphaBetaID(gs, validMoves, current_depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
        
        # If we've spent too much time, break
        if time.time() - start_time > 5:  # 5 second limit
            break
    
    # If we didn't find a move (shouldn't happen normally), pick random
    if nextMove is None and len(validMoves) > 0:
        nextMove = validMoves[random.randint(0, len(validMoves) - 1)]
    
    returnQueue.put(nextMove)

def check_opening_book(gs):
    """Check opening book for the current position"""
    # Convert move log to simplified format
    position_key = ""
    if len(gs.moveLog) > 0:
        # Use the last move as the key
        last_move = gs.moveLog[-1]
        position_key = move_to_string(last_move, gs)
    
    # Check if position is in opening book
    if position_key in OPENING_BOOK:
        responses = OPENING_BOOK[position_key]
        return random.choice(responses)
    
    # If starting position
    if position_key == "" and len(gs.moveLog) == 0:
        return random.choice(OPENING_BOOK[""])
        
    return None

def move_to_string(move, gs):
    """Convert move object to string format (e.g., 'e2e4')"""
    # Convert row, col to algebraic notation
    cols = "abcdefgh"
    rows = "87654321"
    
    start_square = cols[move.startCol] + rows[move.startRow]
    end_square = cols[move.endCol] + rows[move.endRow]
    
    return start_square + end_square

def findMoveNegaMaxAlphaBetaID(gs, validMoves, depth, alpha, beta, turnMultiplier):
    """NegaMax algorithm with alpha-beta pruning and iterative deepening"""
    global nextMove
    
    # Order moves to improve alpha-beta pruning efficiency
    orderMoves(gs, validMoves)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        
        # Calculate hash for position after move
        position_hash = compute_zobrist_hash(gs)
        
        # Check if we've seen this position before
        if position_hash in POSITION_CACHE and POSITION_CACHE[position_hash]['depth'] >= depth - 1:
            score = POSITION_CACHE[position_hash]['score']
        else:
            # Recursive call with quiescence search if needed
            if depth == 1 and is_capture_or_check(gs, move):
                score = -negaMaxAlphaBeta(gs, nextMoves, QUIESCENCE_DEPTH, -beta, -alpha, -turnMultiplier)
            else:
                score = -negaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            
            # Cache the result
            POSITION_CACHE[position_hash] = {'score': score, 'depth': depth - 1}
        
        if score > maxScore:
            maxScore = score
            if depth == DEFAULT_DEPTH:
                nextMove = move
                print(f"Best move so far: {move_to_string(move, gs)} with score: {score}")
        
        gs.undoMove()
        
        # Alpha-beta pruning
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
            
    return maxScore

def negaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    """Standard negamax with alpha-beta pruning"""
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    # Order moves to improve pruning
    orderMoves(gs, validMoves)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -negaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()
        
        if score > maxScore:
            maxScore = score
        
        # Alpha-beta pruning
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
            
    return maxScore

def is_capture_or_check(gs, move):
    """Determine if a move is a capture or gives check"""
    if move.pieceCaptured != "--":
        return True
        
    # Simplified check detection - a more comprehensive implementation would determine if the move gives check
    # This is a placeholder that assumes any checking moves would be caught by deeper search
    return False

def orderMoves(gs, moves):
    """Order moves to improve alpha-beta pruning efficiency"""
    # Assign scores to moves for sorting
    moveScores = []
    for move in moves:
        moveScore = 0
        
        # Prioritize captures by MVV-LVA (Most Valuable Victim - Least Valuable Aggressor)
        if move.pieceCaptured != "--":
            # Calculate value of captured piece
            capturedValue = getPieceValue(move.pieceCaptured)
            # Calculate value of attacking piece
            attackerValue = getPieceValue(move.pieceMoved)
            # MVV-LVA score: victim value * 10 - attacker value
            moveScore = capturedValue * 10 - attackerValue
        
        # Prioritize promotions
        if move.isPawnPromotion:
            moveScore += 800  # High value for promotion
        
        # Prioritize checks (simplified - we're not detecting checks here)
        # You'd need more complex logic to determine if a move gives check
        
        # Prioritize central pawn moves in opening
        if move.pieceMoved[1] == "p" and len(gs.moveLog) < 10:
            if move.endCol >= 3 and move.endCol <= 4 and move.endRow >= 3 and move.endRow <= 4:
                moveScore += 50
        
        moveScores.append(moveScore)
    
    # Sort moves based on scores (highest first)
    # Use bubble sort for simplicity
    for i in range(len(moves)):
        for j in range(0, len(moves) - i - 1):
            if moveScores[j] < moveScores[j + 1]:
                # Swap moves and scores
                moves[j], moves[j + 1] = moves[j + 1], moves[j]
                moveScores[j], moveScores[j + 1] = moveScores[j + 1], moveScores[j]

def getPieceValue(piece):
    """Get the value of a piece"""
    pieceType = piece[1]
    return pieceScore.get(pieceType, 0)

def scoreBoard(gs):
    """Evaluate the current board position"""
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE   # White wins
    elif gs.stalemate:
        return STALEMATE
    
    # Determine if we're in endgame
    endgame = is_endgame(gs)
    
    score = 0
    
    # Material and position score
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # Base piece value
                pieceValue = pieceScore.get(square[1], 0)
                
                # Position-based evaluation
                positionScore = 0
                if square[1] == "p":
                    # Pawns
                    positionScore = piecePositionScores["wp" if square[0] == "w" else "bp"][row][col]
                elif square[1] == "K":
                    # Kings - use different tables for middlegame and endgame
                    kingTable = f"{square[0]}K_{'end' if endgame else 'mid'}"
                    positionScore = piecePositionScores[kingTable][row][col]
                else:
                    # Other pieces
                    positionScore = piecePositionScores[square[1]][row][col]
                
                # Add to score based on piece color
                if square[0] == 'w':
                    score += pieceValue + positionScore * 0.1
                else:
                    score -= pieceValue + positionScore * 0.1
    
    # Additional evaluation features
    
    # Pawn structure evaluation (simplified)
    pawn_structure_score = evaluate_pawn_structure(gs)
    score += pawn_structure_score
    
    # Mobility evaluation (simplified)
    mobility_score = evaluate_mobility(gs)
    score += mobility_score
    
    # King safety (simplified)
    king_safety_score = evaluate_king_safety(gs)
    score += king_safety_score
    
    return score

def evaluate_pawn_structure(gs):
    """Evaluate pawn structure - doubled, isolated, and passed pawns"""
    score = 0
    
    # Count pawns in each file
    white_pawn_files = [0] * 8
    black_pawn_files = [0] * 8
    
    # Track pawn positions
    white_pawns = []
    black_pawns = []
    
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece == "wp":
                white_pawn_files[col] += 1
                white_pawns.append((row, col))
            elif piece == "bp":
                black_pawn_files[col] += 1
                black_pawns.append((row, col))
    
    # Doubled pawns penalty
    for file_count in white_pawn_files:
        if file_count > 1:
            score -= 15 * (file_count - 1)  # Penalty for each doubled pawn
    
    for file_count in black_pawn_files:
        if file_count > 1:
            score += 15 * (file_count - 1)  # Penalty for opponent's doubled pawns
    
    # Isolated pawns penalty
    for col in range(8):
        # White isolated pawns
        if white_pawn_files[col] > 0:
            is_isolated = True
            if col > 0 and white_pawn_files[col-1] > 0:
                is_isolated = False
            if col < 7 and white_pawn_files[col+1] > 0:
                is_isolated = False
            
            if is_isolated:
                score -= 10
        
        # Black isolated pawns
        if black_pawn_files[col] > 0:
            is_isolated = True
            if col > 0 and black_pawn_files[col-1] > 0:
                is_isolated = False
            if col < 7 and black_pawn_files[col+1] > 0:
                is_isolated = False
            
            if is_isolated:
                score += 10
    
    # Passed pawns bonus (simplified)
    for row, col in white_pawns:
        is_passed = True
        # Check if there are any black pawns that can block or capture
        for r in range(row-1, -1, -1):  # Check rows ahead
            if col > 0 and gs.board[r][col-1] == "bp":
                is_passed = False
                break
            if gs.board[r][col] == "bp":
                is_passed = False
                break
            if col < 7 and gs.board[r][col+1] == "bp":
                is_passed = False
                break
        
        if is_passed:
            # Bonus increases as pawn advances
            score += (7 - row) * 10
    
    for row, col in black_pawns:
        is_passed = True
        # Check if there are any white pawns that can block or capture
        for r in range(row+1, 8):  # Check rows ahead
            if col > 0 and gs.board[r][col-1] == "wp":
                is_passed = False
                break
            if gs.board[r][col] == "wp":
                is_passed = False
                break
            if col < 7 and gs.board[r][col+1] == "wp":
                is_passed = False
                break
        
        if is_passed:
            # Bonus increases as pawn advances
            score -= row * 10
    
    return score

def evaluate_mobility(gs):
    """Evaluate piece mobility - more options is better"""
    # This is a simplified version - ideally would count legal moves for each piece
    
    # Store the original whiteToMove value
    original_turn = gs.whiteToMove
    
    # Calculate mobility for white
    gs.whiteToMove = True
    white_moves = len(gs.getValidMoves())
    
    # Calculate mobility for black
    gs.whiteToMove = False
    black_moves = len(gs.getValidMoves())
    
    # Restore original turn
    gs.whiteToMove = original_turn
    
    # Return mobility difference
    return (white_moves - black_moves) * 0.1

def evaluate_king_safety(gs):
    """Evaluate king safety based on pawn shield and piece proximity"""
    score = 0
    
    # Find kings
    white_king_pos = None
    black_king_pos = None
    
    for row in range(8):
        for col in range(8):
            if gs.board[row][col] == "wK":
                white_king_pos = (row, col)
            elif gs.board[row][col] == "bK":
                black_king_pos = (row, col)
    
    if white_king_pos and black_king_pos:
        # Evaluate pawn shield for white king (simplified)
        if white_king_pos[0] == 7:  # King on bottom rank
            # Check for pawns in front of king
            for col_offset in [-1, 0, 1]:
                king_col = white_king_pos[1]
                if 0 <= king_col + col_offset < 8:
                    if gs.board[6][king_col + col_offset] == "wp":
                        score += 10  # Bonus for each pawn protecting the king
        
        # Evaluate pawn shield for black king
        if black_king_pos[0] == 0:  # King on top rank
            # Check for pawns in front of king
            for col_offset in [-1, 0, 1]:
                king_col = black_king_pos[1]
                if 0 <= king_col + col_offset < 8:
                    if gs.board[1][king_col + col_offset] == "bp":
                        score -= 10  # Bonus for opponent's king protection
        
        # Penalty for exposed king in the middle of the board
        if not is_endgame(gs):
            # White king out in the open
            if 2 <= white_king_pos[0] <= 5 and 2 <= white_king_pos[1] <= 5:
                score -= 50
                
            # Black king out in the open
            if 2 <= black_king_pos[0] <= 5 and 2 <= black_king_pos[1] <= 5:
                score += 50
    
    return score
