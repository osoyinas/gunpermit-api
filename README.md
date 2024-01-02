# gunpermit API

API brinda acceso a las preguntas tipo test y los temas relacionados con el permiso de armas en España. Toda la información ha sido recopilada de los PDF oficiales proporcionados por el programa de la Guardia Civil.

# Endpoints

### Obtener temas disponibles

```http
GET /api/v1/topics
```

Devuelve una lista de temas disponibles con enlaces a los detalles de cada tema. Cada tema contiene subtemas, la cantidad total de preguntas, y la fuente oficial del material.

```json
{
  "topics": [
    {
      "id": 1,
      "topic": "Tema 1",
      "subtopics": [
        {"subtopic": "FUNCIONAMIENTO DE LAS ARMAS", "questions": 10 },
        {"subtopic": "PIEZAS FUNDAMENTALES Y MECANISMOS DE DISPARO Y SEGURIDAD", "questions": 10 },
        {"subtopic": "CONSERVACIÓN Y LIMPIEZA DE LAS ARMAS", "questions": 10 },
        {"subtopic": "MEDIDAS DE SEGURIDAD ADOPTAR EN LA TENENCIA DE LAS ARMAS", "questions": 10 }
      ],
      "questions": 68,
      "source": "https://www.guardiacivil.es/documentos/iarmas/temarios/tema1_es.pdf"
    },
    {
      "topic": "Tema 2",
      "topic_index": 2,
      "subtopics": [
        {"subtopic": "CATEGORÍA DE LAS ARMAS SEGÚN EL VIGENTE REGLAMENTO DE ARMAS", "questions": 10 },
        {"subtopic": "ARMAS SEMIAUTOMÁTICAS, ARMAS DE REPETICIÓN, ARMAS PROHIBIDAS", "questions": 10 }
      ],
      "questions": 68,
      "source": "https://www.guardiacivil.es/documentos/iarmas/temarios/tema1_es.pdf"
    }
    // ...
  ]
}
```

### Obtener detalles de un tema específico

```http
GET /api/v1/topics/1
```

Devuelve los detalles de un tema específico, incluyendo sus subtemas, cantidad total de preguntas y la fuente oficial del material.

```json
{
  "topic_index": 1,
  "topic": "Tema 1",
  "subtopics": [
    {"subtopic": "FUNCIONAMIENTO DE LAS ARMAS", "questions": 10 },
    {"subtopic": "PIEZAS FUNDAMENTALES Y MECANISMOS DE DISPARO Y SEGURIDAD", "questions": 10 },
    {"subtopic": "CONSERVACIÓN Y LIMPIEZA DE LAS ARMAS", "questions": 10 },
    {"subtopic": "MEDIDAS DE SEGURIDAD ADOPTAR EN LA TENENCIA DE LAS ARMAS", "questions": 10 }
  ],
  "questions": 68,
  "source": "https://www.guardiacivil.es/documentos/iarmas/temarios/tema1_es.pdf"
}
```

### Obtener preguntas de un tema específico

```http
GET /api/v1/<topic_id>/questions
```

Devuelve la lista de preguntas asociadas a un tema específico, incluyendo la información sobre cada pregunta y sus posibles respuestas.

```json
{
  "topic": {
    "id": 1,
    "topic": "Tema 1",
    "subtopics": [
      {"subtopic": "FUNCIONAMIENTO DE LAS ARMAS", "questions": 10 },
      {"subtopic": "PIEZAS FUNDAMENTALES Y MECANISMOS DE DISPARO Y SEGURIDAD", "questions": 10 },
      {"subtopic": "CONSERVACIÓN Y LIMPIEZA DE LAS ARMAS", "questions": 10 },
      {"subtopic": "MEDIDAS DE SEGURIDAD ADOPTAR EN LA TENENCIA DE LAS ARMAS", "questions": 10 }
    ],
    "questions": 68,
    "source": "https://www.guardiacivil.es/documentos/iarmas/temarios/tema1_es.pdf"
  },
  "questions": [
    {
      "id": 1,
      "topic": 1,
      "question": "La clasificación de un arma dentro de una categoría, se determina en base a:",
      "answers": [
        {"answer": "Su grado de peligrosidad", "is_true": false },
        {"answer": "Sus características, destino o utilización y a veces por la licencia que la ampare", "is_true": false },
        {"answer": "Ambas respuestas son correctas", "is_true": true }
      ]
    }
    // ...
  ]
}
```
# Instalación de gunpermit-API

Siga estos pasos para realizar la instalación de la API gunpermit en su entorno local.

## Clonar el Repositorio

Primero, clone el repositorio de gunpermit-API desde GitHub utilizando el siguiente comando:

```shell
git clone https://github.com/osoyinas/gunpermit-API.git
```

## Configuración del Entorno Virtual

Acceda al directorio recién clonado e inicie un entorno virtual utilizando `virtualenv`. Esto asegurará que las dependencias del proyecto se manejen de manera aislada.

```shell
cd gunpermit-API
virtualenv venv
```

Active el entorno virtual:

```shell
source venv/bin/activate
```

## Instalación de Dependencias

Instale las dependencias del proyecto utilizando el siguiente comando:

```shell
pip install -r requirements.txt
```

## Migraciones de la Base de Datos

Realice las migraciones necesarias para configurar la base de datos:

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

## Ejecución del Servidor

Finalmente, inicie el servidor de desarrollo:

```shell
python3 manage.py runserver
```

Después de ejecutar este comando, la API debería estar disponible en `http://127.0.0.1:8000/`. ¡Listo! Ahora puede comenzar a trabajar con la API gunpermit en su entorno local.

¡Explora la gunpermitAPI y potencia tus conocimientos sobre el permiso de armas en España!