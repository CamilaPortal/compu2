import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Servidor asincrónico de procesamiento de imágenes.")
    parser.add_argument("--host", type=str, default="::", help="Host del servidor (IPv4 o IPv6).")
    parser.add_argument("--port", type=int, default=8080, help="Puerto del servidor.")
    return parser.parse_args()

