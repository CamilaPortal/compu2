import socket
import multiprocessing
import socketserver
import argparse
import logging
import signal
from image_processing import scale_image
from utils import parse_args


class ImageScalingHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Recibe los datos de la imagen
        image_data = self.request.recv(1024*1024)
        scaled_image_data = scale_image(image_data)
        
        self.request.sendall(scaled_image_data)


def start_scaling_server(host=None, port=9090):
    try:
        with socketserver.TCPServer((host, port), ImageScalingHandler, bind_and_activate=False) as server:
            # Permite IPv4 e IPv6 automáticamente
            server.address_family = socket.AF_INET6 if socket.has_ipv6 and ':' in host else socket.AF_INET
            server.server_bind()
            server.server_activate()
            print(f"Servidor de Escalado de Imágenes ejecutándose en {host}:{port}")
            server.serve_forever()
    except OSError as e:
        print(f"Error al iniciar el servidor: {e}")


def handle_sigint(signal_number, frame, server_process):
    logging.info("\nSIGINT recibido. Finalizando el servidor...")
    server_process.terminate()
    server_process.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    # El servidor escuchará en la dirección y puerto especificados
    server_process = multiprocessing.Process(target=start_scaling_server, args=(args.host, args.port))
    server_process.start()

    # Registrar el manejador de SIGINT para el proceso principal
    signal.signal(signal.SIGINT, lambda s, f: handle_sigint(s, f, server_process))

    try:
        server_process.join()
    except KeyboardInterrupt:
        logging.info("\nProceso del servidor finalizado por el usuario.")
        server_process.terminate()
        server_process.join()
