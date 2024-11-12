import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Servidor de procesamiento de imágenes")
    parser.add_argument('--host', type=str, default='localhost', help='Host del servidor principal')
    parser.add_argument('--port', type=int, default=8080, help='Puerto del servidor principal')
    parser.add_argument('--scale-host', type=str, default='localhost', help='Host del servidor de escalado')
    parser.add_argument('--scale-port', type=int, default=9090, help='Puerto del servidor de escalado')
    return parser.parse_args()