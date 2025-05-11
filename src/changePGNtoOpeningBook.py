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
    def __init__(self, pgn_file=None, opening_book_file="opening_book.json", max_moves=10, min_elo=2000):
        """
        Khởi tạo công cụ chuyển đổi
        Args:
            pgn_file: Đường dẫn đến file PGN
            opening_book_file: Đường dẫn đến file opening book (JSON)
            max_moves: Số nước đi tối đa để lấy từ mỗi ván cờ
            min_elo: Điểm Elo tối thiểu của người chơi
        """
        self.pgn_file = pgn_file
        self.opening_book_file = opening_book_file
        self.max_moves = max_moves
        self.min_elo = min_elo
        self.openings = defaultdict(list)
        self.load_existing_book()

    def load_existing_book(self):
        """Tải opening book hiện có nếu có"""
        if os.path.exists(self.opening_book_file):
            try:
                with open(self.opening_book_file, 'r') as f:
                    book_data = json.load(f)
                    for fen, moves in book_data.items():
                        self.openings[fen] = moves
                print(f"Đã tải opening book từ {self.opening_book_file}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Lỗi khi tải opening book: {e}")
                # Tạo mới nếu file bị lỗi
                self.openings = defaultdict(list)

    def process_game(self, game):
        """
        Xử lý một ván cờ và trích xuất các nước đi khai cuộc
        Args:
            game: Đối tượng game từ chess.pgn
        """
        # Kiểm tra điểm Elo của người chơi
        white_elo = int(game.headers.get("WhiteElo", 0))
        black_elo = int(game.headers.get("BlackElo", 0))
        
        if min(white_elo, black_elo) < self.min_elo:
            return
        
        board = game.board()
        moves = []
        move_count = 0
        
        # Duyệt các nước đi
        for move in game.mainline_moves():
            if move_count >= self.max_moves:
                break
                
            # Thêm nước đi vào opening book
            fen = board.fen().split(' ')[0]  # Chỉ lấy phần vị trí quân cờ
            uci_move = move.uci()
            san_move = board.san(move)
            
            # Lưu thông tin nước đi
            move_info = {
                "uci": uci_move,
                "san": san_move,
                "count": 1
            }
            
            # Kiểm tra nếu nước đi đã tồn tại thì tăng số lần xuất hiện
            move_exists = False
            for existing_move in self.openings[fen]:
                if existing_move["uci"] == uci_move:
                    existing_move["count"] += 1
                    move_exists = True
                    break
                    
            if not move_exists:
                self.openings[fen].append(move_info)
            
            # Thực hiện nước đi trên bàn cờ
            board.push(move)
            move_count += 1

    def process_pgn_file(self):
        """Xử lý toàn bộ file PGN"""
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
        """
        Xử lý chuỗi PGN
        Args:
            pgn_string: Chuỗi định dạng PGN
        """
        pgn_file = io.StringIO(pgn_string)
        game_count = 0
        
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
                
            self.process_game(game)
            game_count += 1
            
        print(f"Đã xử lý {game_count} ván cờ từ chuỗi PGN.")

    def save_opening_book(self):
        """Lưu opening book vào file JSON"""
        try:
            with open(self.opening_book_file, 'w') as f:
                json.dump(dict(self.openings), f, indent=2)
            print(f"Đã lưu opening book vào {self.opening_book_file}")
        except IOError as e:
            print(f"Lỗi khi lưu opening book: {e}")

    def get_statistics(self):
        """Trả về thống kê về opening book"""
        total_positions = len(self.openings)
        total_moves = sum(len(moves) for moves in self.openings.values())
        total_counts = sum(move["count"] for position in self.openings.values() for move in position)
        
        return {
            "positions": total_positions,
            "unique_moves": total_moves,
            "total_moves": total_counts
        }
    
    def search_position(self, fen):
        """
        Tìm kiếm các nước đi cho một vị trí cụ thể
        Args:
            fen: Chuỗi FEN (có thể là FEN đầy đủ hoặc chỉ phần vị trí)
        Returns:
            Danh sách các nước đi có thể cho vị trí này
        """
        # Chỉ cần phần vị trí của FEN
        fen_position = fen.split(' ')[0]
        
        # Tìm tất cả các vị trí phù hợp
        matching_moves = []
        for book_fen, moves in self.openings.items():
            if book_fen == fen_position:
                # Sắp xếp theo số lần xuất hiện giảm dần
                sorted_moves = sorted(moves, key=lambda x: x["count"], reverse=True)
                matching_moves = sorted_moves
                break
                
        return matching_moves

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
        print(f"Thống kê Opening Book:")
        print(f"- Số vị trí: {stats['positions']}")
        print(f"- Số nước đi độc nhất: {stats['unique_moves']}")
        print(f"- Tổng số nước đi: {stats['total_moves']}")
    else:
        print("Hãy chỉ định file PGN với tham số --pgn")

if __name__ == "__main__":
    main()