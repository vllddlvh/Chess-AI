'''
    Add or remove bots :
    
    SET_WHITE_AS_BOT = False
    SET_BLACK_AS_BOT = True
'''

# Responsible for handling user input and displaying the current Gamestate object

import sys
import pygame as p
from engine import GameState, Move
from chessAi import findRandomMoves, findBestMove, OpeningBook, move_to_algebraic
from multiprocessing import Process, Queue

# Initialize the mixer
p.mixer.init()
# Load sound files
move_sound = p.mixer.Sound("sounds/move-sound.mp3")
capture_sound = p.mixer.Sound("sounds/capture.mp3")
promote_sound = p.mixer.Sound("sounds/promote.mp3")

PROFILE_CLIENT_WIDTH = PROFILE_BOT_WIDTH = 512 
PROFILE_CLIENT_HEIGHT = PROFILE_BOT_HEIGHT = 100
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 0
MOVE_LOG_PANEL_HEIGHT = 0
DIMENSION = 8
SQ_SIZE = BOARD_WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}
IMAGES_PROFILE = {}

SET_WHITE_AS_BOT = False
SET_BLACK_AS_BOT = True

# Define colors
LIGHT_SQUARE_COLOR = (237, 238, 209)
DARK_SQUARE_COLOR = (119, 153, 82)
MOVE_HIGHLIGHT_COLOR = (84, 115, 161)
POSSIBLE_MOVE_COLOR = (255, 255, 51)

def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK',
              'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        image_path = "images1/" + piece + ".png"
        original_image = p.image.load(image_path)
        IMAGES[piece] = p.transform.smoothscale(original_image, (SQ_SIZE, SQ_SIZE))

def loadProfiles():
    profiles = ['client', 'BOT']
    for profile in profiles:
        avatar_path = 'images1/' + profile + ".png"
        original_image = p.image.load(avatar_path)
        IMAGES_PROFILE[profile] = p.transform.smoothscale(original_image, (80, 80))  

def pawnPromotionPopup(screen, gs):
    font = p.font.SysFont("Times New Roman", 30, False, False)
    text = font.render("Choose promotion:", True, p.Color("black"))

    button_width, button_height = 100, 100
    buttons = [
        p.Rect(100, 200, button_width, button_height),
        p.Rect(200, 200, button_width, button_height),
        p.Rect(300, 200, button_width, button_height),
        p.Rect(400, 200, button_width, button_height)
    ]

    if gs.whiteToMove:
        button_images = [
            p.transform.smoothscale(p.image.load("images1/bQ.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/bR.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/bB.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/bN.png"), (100, 100))
        ]
    else:
        button_images = [
            p.transform.smoothscale(p.image.load("images1/wQ.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/wR.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/wB.png"), (100, 100)),
            p.transform.smoothscale(p.image.load("images1/wN.png"), (100, 100))
        ]

    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            elif e.type == p.MOUSEBUTTONDOWN:
                mouse_pos = e.pos
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        if i == 0:
                            return "Q"
                        elif i == 1:
                            return "R"
                        elif i == 2:
                            return "B"
                        else:
                            return "N"

        screen.fill(p.Color(LIGHT_SQUARE_COLOR))
        screen.blit(text, (110, 150))

        for i, button in enumerate(buttons):
            p.draw.rect(screen, p.Color("white"), button)
            screen.blit(button_images[i], button.topleft)

        p.display.flip()

def main():
    p.init()
    screen = p.display.set_mode(
        (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, PROFILE_CLIENT_HEIGHT + BOARD_HEIGHT + PROFILE_CLIENT_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(LIGHT_SQUARE_COLOR))
    moveLogFont = p.font.SysFont("Times New Roman", 12, False, False)
    gs = GameState()
    if gs.playerWantsToPlayAsBlack:
        gs.board = gs.board1
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    loadProfiles()
    running = True
    squareSelected = ()
    playerClicks = []
    gameOver = False
    playerWhiteHuman = not SET_WHITE_AS_BOT
    playerBlackHuman = not SET_BLACK_AS_BOT
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False
    pieceCaptured = False
    positionHistory = ""
    previousPos = ""
    countMovesForDraw = 0
    COUNT_DRAW = 0
    opening_book = OpeningBook()  # Khởi tạo sách khai cuộc

    while running:
        humanTurn = (gs.whiteToMove and playerWhiteHuman) or (not gs.whiteToMove and playerBlackHuman)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    x, y = location
                    if y < PROFILE_CLIENT_HEIGHT or y >= PROFILE_CLIENT_HEIGHT + BOARD_HEIGHT:
                        continue
                    adjusted_y = y - PROFILE_CLIENT_HEIGHT
                    col = x // SQ_SIZE
                    row = adjusted_y // SQ_SIZE
                    if squareSelected == (row, col) or col >= 8:
                        squareSelected = ()
                        playerClicks = []
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)
                    if len(playerClicks) == 2 and humanTurn:
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                if gs.board[validMoves[i].endRow][validMoves[i].endCol] != '--':
                                    pieceCaptured = True
                                gs.makeMove(validMoves[i])
                                if move.isPawnPromotion:
                                    promotion_choice = pawnPromotionPopup(screen, gs)
                                    gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotion_choice
                                    promote_sound.play()
                                    pieceCaptured = False
                                if pieceCaptured or move.isEnpassantMove:
                                    capture_sound.play()
                                elif not move.isPawnPromotion:
                                    move_sound.play()
                                pieceCaptured = False
                                moveMade = True
                                animate = True
                                squareSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [squareSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
                if e.key == p.K_r:
                    gs = GameState()
                    validMoves = gs.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking = True
                returnQueue = Queue()
                moveFinderProcess = Process(target=findBestMove, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start()
            if not moveFinderProcess.is_alive():
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = findRandomMoves(validMoves)
                if gs.board[AIMove.endRow][AIMove.endCol] != '--':
                    pieceCaptured = True
                gs.makeMove(AIMove)
                if AIMove.isPawnPromotion:
                    promotion_choice = pawnPromotionPopup(screen, gs)
                    gs.board[AIMove.endRow][AIMove.endCol] = AIMove.pieceMoved[0] + promotion_choice
                    promote_sound.play()
                    pieceCaptured = False
                if pieceCaptured or AIMove.isEnpassantMove:
                    capture_sound.play()
                elif not AIMove.isPawnPromotion:
                    move_sound.play()
                pieceCaptured = False
                AIThinking = False
                moveMade = True
                animate = True
                squareSelected = ()
                playerClicks = []

        if moveMade:
            if countMovesForDraw in [0, 1, 2, 3]:
                countMovesForDraw += 1
            if countMovesForDraw == 4:
                positionHistory += gs.getBoardString()
                if previousPos == positionHistory:
                    COUNT_DRAW += 1
                    positionHistory = ""
                    countMovesForDraw = 0
                else:
                    previousPos = positionHistory
                    positionHistory = ""
                    countMovesForDraw = 0
                    COUNT_DRAW = 0
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock, moveLogFont)
                drawGameState(screen, gs, validMoves, squareSelected, moveLogFont)
                p.display.update()
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
            moveUndone = False

        # Kiểm tra chiến thắng và cập nhật sách khai cuộc
        if gs.checkmate:
            gameOver = True
            if (SET_WHITE_AS_BOT and gs.whiteToMove) or (SET_BLACK_AS_BOT and not gs.whiteToMove):
                # AI thua, không cập nhật
                pass
            else:
                # AI thắng, cập nhật sách khai cuộc
                move_history = " ".join([move_to_algebraic(move) for move in gs.moveLog[:10]])  # Lấy 10 nước đầu
                opening_book.add_move(move_history, "winning_move", weight=10, name="Winning Sequence")
                print("AI thắng, đã cập nhật sách khai cuộc với chuỗi nước đi chiến thắng.")

        drawGameState(screen, gs, validMoves, squareSelected, moveLogFont)

        if COUNT_DRAW == 3:
            gameOver = True
            text = 'Draw due to repetition'
            drawEndGameText(screen, text)
        if gs.stalemate:
            gameOver = True
            text = 'Stalemate'
            drawEndGameText(screen, text)
        elif gs.checkmate:
            text = 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate'
            drawEndGameText(screen, text)

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, validMoves, squareSelected, moveLogFont):
    drawSquare(screen)
    highlightSquares(screen, gs, validMoves, squareSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
    drawProfiles(screen)

def drawSquare(screen):
    global colors
    colors = [p.Color(LIGHT_SQUARE_COLOR), p.Color(DARK_SQUARE_COLOR)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE + PROFILE_CLIENT_HEIGHT, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        row, col = squareSelected
        if 0 <= row < 8 and 0 <= col < 8:
            if gs.board[row][col][0] == ('w' if gs.whiteToMove else 'b'):
                s = p.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)
                s.fill(p.Color(MOVE_HIGHLIGHT_COLOR))
                screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE + PROFILE_CLIENT_HEIGHT))
                s.fill(p.Color(POSSIBLE_MOVE_COLOR))
                for move in validMoves:
                    if move.startRow == row and move.startCol == col:
                        screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE + PROFILE_CLIENT_HEIGHT))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE + PROFILE_CLIENT_HEIGHT, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color(LIGHT_SQUARE_COLOR), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = " " + str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 10
    lineSpacing = 5
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color('black'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def animateMove(move, screen, board, clock, moveLogFont):
    global colors
    deltaRow = move.endRow - move.startRow
    deltaCol = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(deltaRow) + abs(deltaCol)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = (move.startRow + deltaRow*frame/frameCount, move.startCol + deltaCol*frame/frameCount)
        drawSquare(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow * SQ_SIZE + PROFILE_CLIENT_HEIGHT, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow * SQ_SIZE + PROFILE_CLIENT_HEIGHT, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(col*SQ_SIZE, row*SQ_SIZE + PROFILE_CLIENT_HEIGHT, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(240)

def drawProfiles(screen):
    avatar_size = 80
    margin = 10
    if SET_BLACK_AS_BOT:
        screen.blit(IMAGES_PROFILE['BOT'], (margin, (PROFILE_CLIENT_HEIGHT - avatar_size) // 2))
    else:
        screen.blit(IMAGES_PROFILE['client'], (margin, (PROFILE_CLIENT_HEIGHT - avatar_size) // 2))
    if SET_WHITE_AS_BOT:
        screen.blit(IMAGES_PROFILE['BOT'], (margin, BOARD_HEIGHT + PROFILE_CLIENT_HEIGHT + 10))
    else:
        screen.blit(IMAGES_PROFILE['client'], (margin, BOARD_HEIGHT + PROFILE_CLIENT_HEIGHT + 10))

def drawEndGameText(screen, text):
    font = p.font.SysFont("Times New Roman", 30, False, False)
    textObject = font.render(text, True, p.Color('black'))
    text_width = textObject.get_width()
    text_height = textObject.get_height()
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(
        BOARD_WIDTH/2 - text_width/2, BOARD_HEIGHT/2 - text_height/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(1, 1))

if __name__ == "__main__":
    main()