# 1. Imagen base oficial y ligera
FROM python:3.11-slim

# 2. Seguridad: Creamos un usuario sin privilegios root (Principio de Menor Privilegio)
RUN useradd -m -s /bin/bash appuser

# 3. Configuramos el directorio de trabajo
WORKDIR /app

# 4. Instalamos dependencias del sistema estrictamente necesarias
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiamos requerimientos e instalamos (aprovechando caché de capas de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el código del microservicio
COPY . .

# 7. Transferimos la propiedad de los archivos al usuario seguro
RUN chown -R appuser:appuser /app

# 8. Cambiamos al usuario sin privilegios
USER appuser

# 9. Exponemos el puerto 8080 (El estándar que Google Cloud Run espera)
EXPOSE 8080

# 10. Comando de arranque para producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]