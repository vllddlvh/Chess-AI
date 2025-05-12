"""
Công cụ chuyển đổi file PGN (Portable Game Notation) thành Opening Book
Có thể sử dụng để nhập dữ liệu khai cuộc từ các ván cờ thực tế
"""
import chess
import chess.pgn
import json
import os
import io
import argparse
from collections import defaultdict

class PGNtoOpeningBook:
    def __init__(self, pgn_file="", opening_book_file="C:\\Users\\ADMIN\\Chess-AI\\opening_book.json", max_moves=200, min_elo=2000):
        self.pgn_file = pgn_file
        self.opening_book_file = opening_book_file
        self.max_moves = max_moves
        self.min_elo = min_elo
        self.openings = defaultdict(list)
        self.load_existing_book()

    def load_existing_book(self):
        if os.path.exists(self.opening_book_file):
            try:
                with open(self.opening_book_file, 'r') as f:
                    book_data = json.load(f)
                    for fen, moves in book_data.items():
                        self.openings[fen] = moves
                print(f"Đã tải opening book từ {self.opening_book_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Lỗi khi tải opening book: {e}")
                self.openings = defaultdict(list)

    def process_game(self, game):
        """
        Xử lý một ván cờ và trích xuất các nước đi khai cuộc
        """
        white_elo = game.headers.get("WhiteElo", "0")
        black_elo = game.headers.get("BlackElo", "0")

        try:
            white_elo = int(white_elo)
            black_elo = int(black_elo)
        except ValueError:
            print(f"Bỏ qua ván cờ do Elo không hợp lệ: WhiteElo={white_elo}, BlackElo={black_elo}")
            return

        if min(white_elo, black_elo) < self.min_elo:
            print(f"Bỏ qua ván cờ do Elo thấp: WhiteElo={white_elo}, BlackElo={black_elo}")
            return

        board = game.board()
        move_count = 0

        for move in game.mainline_moves():
            if move_count >= self.max_moves:
                break

            fen = board.fen().split(' ')[0]

            # Chỉ xử lý nước đi hợp lệ
            if not board.is_legal(move):
                print(f"Bỏ qua nước đi không hợp lệ: {move} tại FEN: {fen}")
                return

            try:
                # Sau khi xác nhận hợp lệ, lấy SAN và UCI
                san_move = board.san(move)
                uci_move = move.uci()

                move_info = {
                    "uci": uci_move,
                    "san": san_move,
                    "count": 1
                }

                # Cập nhật opening book
                existing = next((m for m in self.openings[fen] if m["uci"] == uci_move), None)
                if existing:
                    existing["count"] += 1
                else:
                    self.openings[fen].append(move_info)

                board.push(move)
                move_count += 1

            except Exception as e:
                print(f"Bỏ qua nước đi lỗi: {move} tại FEN: {fen}, lỗi: {e}")
                return

    def process_pgn_file(self):
        if not self.pgn_file:
            print("Không có file PGN nào được chỉ định")
            return
        game_count = 0
        try:
            with open(self.pgn_file, 'r') as pgn:
                while True:
                    game = chess.pgn.read_game(pgn)
                    if game is None:
                        break
                    self.process_game(game)
                    game_count += 1
                    if game_count % 100 == 0:
                        print(f"Đã xử lý {game_count} ván cờ...")
            print(f"Hoàn thành xử lý {game_count} ván cờ.")
        except FileNotFoundError:
            print(f"Không tìm thấy file PGN: {self.pgn_file}")
        except Exception as e:
            print(f"Lỗi khi xử lý file PGN: {e}")

    def process_pgn_string(self, pgn_string):
        pgn_stream = io.StringIO(pgn_string)
        game_count = 0
        while True:
            game = chess.pgn.read_game(pgn_stream)
            if game is None:
                break
            self.process_game(game)
            game_count += 1
        print(f"Đã xử lý {game_count} ván cờ từ chuỗi PGN.")

    def save_opening_book(self):
        try:
            with open(self.opening_book_file, 'w') as f:
                json.dump(dict(self.openings), f, indent=2)
            print(f"Đã lưu opening book vào {self.opening_book_file}")
        except IOError as e:
            print(f"Lỗi khi lưu opening book: {e}")

    def get_statistics(self):
        total_positions = len(self.openings)
        total_moves = sum(len(moves) for moves in self.openings.values())
        total_counts = sum(move["count"] for moves in self.openings.values() for move in moves)
        return {"positions": total_positions, "unique_moves": total_moves, "total_moves": total_counts}

    def search_position(self, fen):
        fen_key = fen.split(' ')[0]
        moves = self.openings.get(fen_key, [])
        return sorted(moves, key=lambda x: x['count'], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Chuyển đổi file PGN thành Opening Book")
    parser.add_argument("--pgn", type=str, help="Đường dẫn đến file PGN")
    parser.add_argument("--book", type=str, default="opening_book.json", help="Đường dẫn đến file opening book")
    parser.add_argument("--max-moves", type=int, default=10, help="Số nước đi tối đa từ mỗi ván cờ")
    parser.add_argument("--min-elo", type=int, default=2000, help="Điểm Elo tối thiểu của người chơi")
    args = parser.parse_args()
    converter = PGNtoOpeningBook(
        pgn_file=args.pgn,
        opening_book_file=args.book,
        max_moves=args.max_moves,
        min_elo=args.min_elo
    )
    if args.pgn:
        converter.process_pgn_file()
        converter.save_opening_book()
        stats = converter.get_statistics()
        print("Thống kê Opening Book:")
        print(f"- Số vị trí: {stats['positions']}")
        print(f"- Số nước đi độc nhất: {stats['unique_moves']}")
        print(f"- Tổng số nước đi: {stats['total_moves']}")
    else:
        print("Hãy chỉ định file PGN với tham số --pgn")

if __name__ == "__main__":
    main()
