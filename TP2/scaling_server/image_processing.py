from PIL import Image
import io

async def convert_to_grayscale(image_data):
    """Convierte una imagen a escala de grises."""
    try:
        # Cargar la imagen desde los datos binarios
        image = Image.open(io.BytesIO(image_data))
        grayscale_image = image.convert("L")  # Convertir a escala de grises
        
        output = io.BytesIO()
        grayscale_image.save(output, format="PNG")
        
        # Retornar los datos binarios de la imagen en escala de grises
        return output.getvalue()
    except Exception as e:
        print(f"Error en convert_to_grayscale: {e}")
        raise

def scale_image(image_data):
    """Redimensiona la imagen de acuerdo con el factor de escala."""
    image = Image.open(io.BytesIO(image_data))
    scale_factor=0.5
    new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
    scaled_image = image.resize(new_size)
    output = io.BytesIO()
    scaled_image.save(output, format='PNG')
    return output.getvalue()
