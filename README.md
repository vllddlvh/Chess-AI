# BÀI TẬP LỚN CHESS AI
![Demo project](https://imgur.com/a/E5wIISN)

## Thành viên nhóm

| Họ và tên         | Mã số sinh viên |
|-------------------|-----------------|
| Đào Lê Long Vũ    | 23021750        |
| Bùi Hải Phương    | 23021666        |
| Kiều Đức Thắng    | 23021722        |

---

## Hướng dẫn cài đặt

Cài đặt thư viện Pygame:

```bash
pip install pygame

## Hướng dẫn sử dụng

### Chạy chương trình:

1. Mở terminal trong thư mục chứa mã nguồn.
2. Chạy file `main.py` bằng lệnh:

```bash
python main.py

### Điều khiển:

- **Nhấp chuột** để chọn và di chuyển quân cờ.
- **Nhấn `z`** để hoàn tác một nước đi.
- **Nhấn `r`** để đặt lại bàn cờ.
- Khi **phong cấp tốt**, chọn quân từ cửa sổ popup.

### Cài đặt AI:

- Trong `main.py`:  
  Đặt `SET_WHITE_AS_BOT = True` hoặc `SET_BLACK_AS_BOT = True` để bật AI cho bên trắng hoặc đen.

- Trong `engine.py`:  
  Đặt `playerWantsToPlayAsBlack = True` để lật bàn cờ và chơi với quân đen.

