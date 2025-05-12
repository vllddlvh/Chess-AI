import json

default_openings = {
    "": [
        {"move": "e2e4", "weight": 10, "name": "King's Pawn Opening"},
        {"move": "d2d4", "weight": 10, "name": "Queen's Pawn Opening"},
        {"move": "c2c4", "weight": 8, "name": "English Opening"},
        {"move": "g1f3", "weight": 7, "name": "Réti Opening"},
        {"move": "b2b3", "weight": 5, "name": "Nimzowitsch-Larsen Attack"},
        {"move": "g2g3", "weight": 5, "name": "King's Indian Attack"},
        {"move": "f2f4", "weight": 4, "name": "Bird's Opening"},
        {"move": "b2b4", "weight": 3, "name": "Sokolsky Opening"},
        {"move": "a2a3", "weight": 2, "name": "Anderssen's Opening"},
        {"move": "d2d3", "weight": 2, "name": "Mieses Opening"}
    ],
    "e2e4": [
        {"move": "e7e5", "weight": 10, "name": "Open Game"},
        {"move": "c7c5", "weight": 10, "name": "Sicilian Defense"},
        {"move": "e7e6", "weight": 8, "name": "French Defense"},
        {"move": "c7c6", "weight": 7, "name": "Caro-Kann Defense"},
        {"move": "d7d5", "weight": 7, "name": "Scandinavian Defense"},
        {"move": "g8f6", "weight": 6, "name": "Alekhine's Defense"},
        {"move": "f7f5", "weight": 4, "name": "Latvian Gambit"},
        {"move": "b7b6", "weight": 4, "name": "Owen's Defense"},
        {"move": "d7d6", "weight": 5, "name": "Pirc Defense"},
        {"move": "g7g6", "weight": 5, "name": "Modern Defense"}
    ],
    "e2e4 e7e5": [
        {"move": "g1f3", "weight": 10, "name": "King's Knight Opening"},
        {"move": "f2f4", "weight": 8, "name": "King's Gambit"},
        {"move": "b1c3", "weight": 7, "name": "Vienna Game"},
        {"move": "c2c4", "weight": 6, "name": "Center Game"},
        {"move": "d2d4", "weight": 6, "name": "Danish Gambit"},
        {"move": "f1c4", "weight": 5, "name": "Bishop's Opening"},
        {"move": "g2g3", "weight": 4, "name": "Hungarian Opening"}
    ],
    "e2e4 e7e5 g1f3": [
        {"move": "b8c6", "weight": 10, "name": "Two Knights Defense"},
        {"move": "d7d6", "weight": 8, "name": "Philidor Defense"},
        {"move": "f7f5", "weight": 6, "name": "Latvian Gambit"},
        {"move": "g8f6", "weight": 9, "name": "Petrov's Defense"},
        {"move": "c7c5", "weight": 5, "name": "Schliemann Defense"},
        {"move": "a7a6", "weight": 4, "name": "O'Kelly Variation"}
    ],
    "e2e4 e7e5 g1f3 b8c6": [
        {"move": "f1b5", "weight": 10, "name": "Ruy Lopez"},
        {"move": "f1c4", "weight": 9, "name": "Italian Game"},
        {"move": "d2d4", "weight": 8, "name": "Scotch Game"},
        {"move": "c2c3", "weight": 7, "name": "Ponziani Opening"},
        {"move": "b1c3", "weight": 6, "name": "Three Knights Game"},
        {"move": "g2g3", "weight": 5, "name": "Konstantinopolsky Opening"}
    ],
    "e2e4 e7e5 g1f3 b8c6 f1b5": [
        {"move": "a7a6", "weight": 10, "name": "Ruy Lopez: Morphy Defense"},
        {"move": "f7f5", "weight": 7, "name": "Ruy Lopez: Schliemann Defense"},
        {"move": "d7d6", "weight": 8, "name": "Ruy Lopez: Steinitz Defense"},
        {"move": "g8f6", "weight": 9, "name": "Ruy Lopez: Berlin Defense"}
    ],
    "e2e4 c7c5": [
        {"move": "g1f3", "weight": 10, "name": "Moscow Variation"},
        {"move": "c2c3", "weight": 8, "name": "Alapin Variation"},
        {"move": "b1c3", "weight": 7, "name": "Closed Sicilian"},
        {"move": "f2f4", "weight": 6, "name": "Grand Prix Attack"},
        {"move": "d2d4", "weight": 9, "name": "Open Sicilian"},
        {"move": "b2b4", "weight": 5, "name": "Wing Gambit"},
        {"move": "g2g3", "weight": 5, "name": "Delayed Alapin"}
    ],
    "e2e4 c7c5 g1f3": [
        {"move": "d7d6", "weight": 10, "name": "Sicilian: Najdorf/Dragon"},
        {"move": "e7e6", "weight": 8, "name": "Sicilian: Scheveningen"},
        {"move": "g8f6", "weight": 7, "name": "Sicilian: Classical"},
        {"move": "b8c6", "weight": 7, "name": "Sicilian: Kalashnikov"}
    ],
    "e2e4 e7e6": [
        {"move": "d2d4", "weight": 10, "name": "French Defense: Advance Variation"},
        {"move": "g1f3", "weight": 8, "name": "French Defense: Two Knights Variation"},
        {"move": "b1c3", "weight": 9, "name": "French Defense: Winawer Variation"},
        {"move": "c2c4", "weight": 6, "name": "French Defense: King's Indian Attack"}
    ],
    "e2e4 c7c6": [
        {"move": "d2d4", "weight": 10, "name": "Caro-Kann: Classical Variation"},
        {"move": "c2c4", "weight": 8, "name": "Caro-Kann: Panov-Botvinnik Attack"},
        {"move": "b1c3", "weight": 7, "name": "Caro-Kann: Two Knights Variation"},
        {"move": "f2f3", "weight": 5, "name": "Caro-Kann: Fantasy Variation"}
    ],
    "d2d4": [
        {"move": "d7d5", "weight": 10, "name": "Queen's Gambit"},
        {"move": "g8f6", "weight": 10, "name": "Indian Defense"},
        {"move": "f7f5", "weight": 7, "name": "Dutch Defense"},
        {"move": "e7e6", "weight": 7, "name": "Queen's Gambit Declined"},
        {"move": "b8c6", "weight": 5, "name": "Chigorin Defense"},
        {"move": "g7g6", "weight": 6, "name": "Modern Defense"},
        {"move": "c7c6", "weight": 5, "name": "Slav Defense"},
        {"move": "e7e5", "weight": 4, "name": "Albin Countergambit"}
    ],
    "d2d4 d7d5": [
        {"move": "c2c4", "weight": 10, "name": "Queen's Gambit"},
        {"move": "g1f3", "weight": 8, "name": "Colle System"},
        {"move": "e2e3", "weight": 7, "name": "London System"},
        {"move": "b1c3", "weight": 6, "name": "Veresov Attack"},
        {"move": "f2f3", "weight": 5, "name": "Blackmar-Diemer Gambit"}
    ],
    "d2d4 d7d5 c2c4": [
        {"move": "e7e6", "weight": 10, "name": "Queen's Gambit Declined"},
        {"move": "c7c6", "weight": 9, "name": "Slav Defense"},
        {"move": "d5c4", "weight": 8, "name": "Queen's Gambit Accepted"},
        {"move": "g8f6", "weight": 7, "name": "Semi-Slav Defense"}
    ],
    "d2d4 g8f6": [
        {"move": "c2c4", "weight": 10, "name": "Indian Game"},
        {"move": "g1f3", "weight": 9, "name": "Torre Attack"},
        {"move": "e2e3", "weight": 7, "name": "London System"},
        {"move": "f2f3", "weight": 6, "name": "Trompowsky Attack"},
        {"move": "b1c3", "weight": 6, "name": "Richter-Veresov Attack"},
        {"move": "g2g3", "weight": 5, "name": "Barry Attack"}
    ],
    "d2d4 g8f6 c2c4": [
        {"move": "e7e6", "weight": 10, "name": "Nimzo-Indian Defense"},
        {"move": "g7g6", "weight": 9, "name": "King's Indian Defense"},
        {"move": "c7c5", "weight": 8, "name": "Benoni Defense"},
        {"move": "b7b6", "weight": 7, "name": "Queen's Indian Defense"}
    ],
    "c2c4": [
        {"move": "e7e5", "weight": 10, "name": "English Opening"},
        {"move": "c7c5", "weight": 9, "name": "Symmetrical Defense"},
        {"move": "g8f6", "weight": 8, "name": "Indian Defense"},
        {"move": "e7e6", "weight": 7, "name": "Hedgehog System"},
        {"move": "d7d5", "weight": 6, "name": "Reverse Benoni"},
        {"move": "g7g6", "weight": 5, "name": "Modern Defense"}
    ],
    "c2c4 e7e5": [
        {"move": "b1c3", "weight": 10, "name": "English: Four Knights"},
        {"move": "g1f3", "weight": 9, "name": "English: King's English"},
        {"move": "g2g3", "weight": 7, "name": "English: Fianchetto Variation"},
        {"move": "d2d4", "weight": 6, "name": "English: Bremen System"}
    ],
    "g1f3": [
        {"move": "d7d5", "weight": 10, "name": "Queen's Pawn Game"},
        {"move": "g8f6", "weight": 9, "name": "King's Indian Defense"},
        {"move": "c7c5", "weight": 8, "name": "Sicilian Invitation"},
        {"move": "e7e6", "weight": 7, "name": "English Opening"},
        {"move": "f7f5", "weight": 5, "name": "Dutch Defense"},
        {"move": "b7b6", "weight": 5, "name": "English Defense"}
    ],
    "g1f3 d7d5": [
        {"move": "d2d4", "weight": 10, "name": "Queen's Gambit"},
        {"move": "c2c4", "weight": 9, "name": "English Opening"},
        {"move": "g2g3", "weight": 7, "name": "Catalan Opening"},
        {"move": "e2e3", "weight": 6, "name": "Colle System"}
    ],
    "b2b3": [
        {"move": "e7e5", "weight": 10, "name": "Nimzowitsch-Larsen: Classical"},
        {"move": "d7d5", "weight": 9, "name": "Nimzowitsch-Larsen: Modern"},
        {"move": "g8f6", "weight": 8, "name": "Nimzowitsch-Larsen: Indian"},
        {"move": "c7c5", "weight": 7, "name": "Nimzowitsch-Larsen: Sicilian"}
    ]
}

with open("C:\\Users\\ADMIN\\Chess-AI\\src\\opening_book.json", "w") as f:
    json.dump(default_openings, f, indent=4)

print("Created extensively expanded opening book")