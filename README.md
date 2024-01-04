# gunpermit API

RESTful API which serves tests and topics related with Spain's gun permit. All the information is collected from the official [Guardia Civil program](https://www.guardiacivil.es/es/servicios/armasyexplosivo/controldearmas/autorizaci_armas/licencias_armas/). 

# Endpoints

## Get available topics

### Request
```http
GET /api/v1/topics
```

### Response
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

## Retrieve an specific topic

### Request
```http
GET /api/v1/topics/1
```

### Response
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

## Get questions from topic

### Request
```http
GET /api/v1/<topic_id>/questions
```
### Response
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
# Installation

Follow the next steps to run this API in a local enviroment.

## Clone the repository

```shell
git clone https://github.com/osoyinas/gunpermit-API.git
```

## Setup a python virtual enviroment

```shell
cd gunpermit-API
virtualenv venv
source venv/bin/activate
```


## Install project's dependencies

```shell
pip install -r requirements.txt
```

## Make django's migrations

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

## Run the server

```shell
python3 manage.py runserver
```

Después de ejecutar este comando, la API debería estar disponible en `http://127.0.0.1:8000/`. ¡Listo! Ahora puede comenzar a trabajar con la API gunpermit en su entorno local.

¡Explora la gunpermitAPI y potencia tus conocimientos sobre el permiso de armas en España!
