import zstandard as zstd

def decompress_pgn_zst(input_file, output_file):
    try:
        with open(input_file, 'rb') as compressed_file:
            dctx = zstd.ZstdDecompressor()
            with open(output_file, 'wb') as decompressed_file:
                dctx.copy_stream(compressed_file, decompressed_file)
        print(f"Successfully decompressed {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# Thay đổi tên file đầu vào và đầu ra theo nhu cầu
input_file = 'lichess_db_standard_rated_2023-08.pgn.zst'  # File .pgn.zst của bạn
output_file = 'output.pgn'  # File PGN đầu ra
decompress_pgn_zst(input_file, output_file)