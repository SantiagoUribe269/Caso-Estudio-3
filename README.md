# POC 3

## Descripción del POC
-	Recibir un nuevo caso y cobrar al cliente por la revision de este caso.

## Configuración del entorno

### 1. Crear y activar entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos
1. Crear una base de datos en PostgreSQL llamada `caso3`  
2. Ejecutar el script `tables.sql` para crear las tablas necesarias  
3. Configurar las credenciales en el archivo `.env`:
```env
DB_HOST=localhost
DB_NAME=caso3 
DB_USER=postgres
DB_PASSWORD=tu_contraseña  # Cambiar si es necesario
```

## Endpoints disponibles

### Clientes
- `POST /clients/` - Crear nuevo cliente  
- `GET /clients/` - Listar todos los clientes  
- `GET /clients/{client_id}` - Obtener cliente específico  

### Abogados  
- `POST /lawyers/` - Crear nuevo abogado  
- `GET /lawyers/` - Listar todos los abogados  
- `GET /lawyers/{lawyer_id}` - Obtener abogado específico  

### Casos  
- `POST /cases/` - Crear nuevo caso  
- `GET /cases/` - Listar todos los casos  
- `GET /cases/{case_id}` - Obtener caso específico  

### Recibos/Pagos  
- `POST /receipts/` - Crear nuevo recibo  
- `GET /receipts/` - Listar todos los recibos  
- `GET /receipts/{receipt_id}` - Obtener recibo específico  

## Flujo para probar el POC

### 1. Registrar un cliente
```bash
POST /clients/
{
    "names": "Juan",
    "lastname": "Perez", 
    "document_type": "DNI",
    "document_number": "87654321",
    "email": "juan.perez@example.com",
    "phone": "987654321"
}
```

### 2. Registrar un abogado  
```bash
POST /lawyers/ 
{
    "names": "Ana",
    "lastnames": "Gomez",
    "field": "Derecho Laboral",
    "email": "ana.gomez@example.com"
}
```

### 3. Obtener IDs (para usar en el caso)
```bash
GET /clients/  # Anotar el ID del cliente creado
GET /lawyers/  # Anotar el ID del abogado creado
```

### 4. Crear un caso
```bash
POST /cases/
{
    "title": "Despido injustificado",
    "description": "Cliente fue despedido sin causa justificada",
    "lawyer_id": "<lawyer_id_obtenido>",
    "client_id": "<client_id_obtenido>", 
    "state": "open",
    "priority": 2
}
```

### 5. Obtener ID del caso (para el recibo)
```bash
GET /cases/  # Anotar el ID del caso creado
```

### 6. Registrar un pago/recibo
```bash
POST /receipts/
{
    "case_id": "<case_id_obtenido>",
    "amount": 750.50,
    "ruc_enterprise": "20123456789",
    "ruc_client": "10456789123"
}
```

## Ejecutar la aplicación
```bash
uvicorn main:app 
```

La API estará disponible en `http://localhost:8000`

## Estructura del proyecto
```
Caso-Estudio-3/
├── main.py            # Aplicación principal FastAPI
├── models.py          # Modelos Pydantic
├── requirements.txt   # Dependencias
├── tables.sql         # Script SQL para crear tablas
└── .env               # Configuración de entorno
```

