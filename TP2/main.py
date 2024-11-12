import multiprocessing
import argparse
import signal
import atexit
from scaling_server.scale_server import start_scaling_server
from scaling_server.server_a import create_app
from aiohttp import web

def start_server_a(host, port, scale_host, scale_port):
    """Inicia el servidor principal (server_a)."""
    app = create_app(scale_host, scale_port)
    web.run_app(app, host=host, port=port)

def start_servers(server_a_host, server_a_port, scale_host, scale_port):
    """Inicia ambos servidores en procesos separados."""
    # Proceso para el servidor de escalado
    scaling_server_process = multiprocessing.Process(
        target=start_scaling_server, args=(scale_host, scale_port)
    )
    scaling_server_process.start()

    # Proceso para el servidor principal
    server_a_process = multiprocessing.Process(
        target=start_server_a, args=(server_a_host, server_a_port, scale_host, scale_port)
    )
    server_a_process.start()

    termination_handled = False

    # Función para manejar SIGINT y terminar ambos procesos
    def handle_sigint(signum, frame):
        nonlocal termination_handled
        if not termination_handled:
            print("\nTerminando procesos...")
            scaling_server_process.terminate()
            server_a_process.terminate()
            scaling_server_process.join()
            server_a_process.join()
            termination_handled = True

    signal.signal(signal.SIGINT, handle_sigint)

    atexit.register(handle_sigint, None, None)

    # Espera a que ambos procesos terminen
    scaling_server_process.join()
    server_a_process.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Iniciar ambos servidores.")
    parser.add_argument('--server_a_host', default='127.0.0.1', help="Host para server_a")
    parser.add_argument('--server_a_port', type=int, default=8080, help="Puerto para server_a")
    parser.add_argument('--scale_host', default='127.0.0.1', help="Host para el servidor de escalado")
    parser.add_argument('--scale_port', type=int, default=9090, help="Puerto para el servidor de escalado")
    args = parser.parse_args()

    start_servers(args.server_a_host, args.server_a_port, args.scale_host, args.scale_port)
