from PIL import Image
import io

async def convert_to_grayscale(image_data):
    """Convierte una imagen a escala de grises."""
    try:
        # Cargar la imagen desde los datos binarios
        image = Image.open(io.BytesIO(image_data))
        grayscale_image = image.convert("L")  # Convertir a escala de grises
        
        # Guardar la imagen convertida en un buffer de bytes
        output = io.BytesIO()
        grayscale_image.save(output, format="PNG")
        
        # Retornar los datos binarios de la imagen en escala de grises
        return output.getvalue()
    except Exception as e:
        print(f"Error en convert_to_grayscale: {e}")
        raise
