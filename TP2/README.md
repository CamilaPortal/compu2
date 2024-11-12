# TP2 - Computacion 2

Este repositorio contiene el código para el TP2. Para ejecutar el servidor, sigue los siguientes pasos:

## Instrucciones de uso

1. **Clona el repositorio**:

   Abre una terminal y ejecuta el siguiente comando para clonar el repositorio:

   ```bash
   git clone https://github.com/CamilaPortal/compu2.git
   cd compu2/TP2

2. **Instala las dependencias**:

    ```bash
    pip install -r requirements.txt

3. **Iniciar los servidores**:

    ```bash
    python3 main.py

4. **Ejemplo para probar el funcionamiento**:    
    
    ```bash
    curl -X POST --data-binary "@TP2/UM_logo.png" http://localhost:8080/process-image --output output_image.png

