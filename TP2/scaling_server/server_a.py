import argparse
import asyncio
from aiohttp import web
from image_processing import convert_to_grayscale
from utils import parse_args

async def send_to_scaling_server(image_data, scale_host, scale_port):
    """Envía la imagen al servidor de escalado y recibe la imagen escalada."""
    # Configura un socket TCP para la comunicación
    reader, writer = await asyncio.open_connection(scale_host, scale_port)
    
    # Envía los datos de la imagen al segundo servidor
    writer.write(image_data)
    await writer.drain()
    
    # Lee la respuesta (imagen escalada)
    scaled_image_data = await reader.read()
    
    # Cierra la conexión
    writer.close()
    await writer.wait_closed()
    
    return scaled_image_data

async def handle_image_processing(request):
    """Maneja la solicitud de procesamiento de imagen y envía la respuesta."""
    scale_host = request.app['scale_host']
    scale_port = request.app['scale_port']

    image_data = await request.content.read()
    
    # Convertir la imagen a escala de grises
    grayscale_image_data = await convert_to_grayscale(image_data)
    
    # Enviar la imagen en escala de grises al segundo servidor para el escalado
    scaled_image_data = await send_to_scaling_server(grayscale_image_data, scale_host, scale_port)
    
    return web.Response(body=scaled_image_data, content_type='image/png')

async def create_app(scale_host, scale_port):
    """Crea y configura la aplicación de aiohttp."""
    app = web.Application()
    app['scale_host'] = scale_host
    app['scale_port'] = scale_port
    app.router.add_post('/process-image', handle_image_processing)
    return app

if __name__ == '__main__':
    args = parse_args()
    
    # Ejecuta el servidor, pasando los valores de host y puerto de escalado
    web.run_app(create_app(args.scale_host, args.scale_port), host=args.host, port=args.port)
