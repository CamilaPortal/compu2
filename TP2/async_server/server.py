from aiohttp import web
from image_processing import convert_to_grayscale
from utils import parse_args

async def handle_image_processing(request):
    """Maneja la solicitud de procesamiento de imagen y envía la respuesta."""
    image_data = await request.content.read()
    grayscale_image_data = await convert_to_grayscale(image_data)
    return web.Response(body=grayscale_image_data, content_type='image/png')

async def create_app():
    """Crea y configura la aplicación de aiohttp."""
    app = web.Application()
    app.router.add_post('/process-image', handle_image_processing)
    return app
   

if __name__ == '__main__':
    args = parse_args()

    web.run_app(create_app(), host=args.host, port=args.port)



