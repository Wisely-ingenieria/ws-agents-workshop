# Agents Workshop

Este repositorio contiene los scripts utilizados en el taller de Agentes.

## Variables de entorno

Las variables de entorno en el archivo `.env` estan referenciados en `.env.reference`. Estos incluyen:

| Variable de Entorno | Descripción |
| --- | --- |
| `OPENAI_API_TYPE` | El tipo de API de OpenAI. |
| `OPENAI_API_KEY` | La clave de la API de OpenAI. |
| `OPENAI_EMBEDDING_MODEL` | El nombre del modelo de incrustación de OpenAI utilizado para generar vectores de incrustación. |
| `OPENAI_GPT35_MODEL` | El nombre del modelo GPT-3.5 de OpenAI utilizado para generar texto. |
| `OPENAI_GPT35_16K_MODEL` | El nombre del modelo GPT-3.5 16K de OpenAI utilizado para generar texto. |
| `OPENAI_GPT4_MODEL` | El nombre del modelo GPT-4 de OpenAI utilizado para generar texto. |
| `GITHUB_PAT` | Personal Access Token (PAT) para acceder a la API de GitHub |

## Requisitos

Para ejecutar los scripts de este proyecto, necesitarás:

- Credenciales de API de OpenAI.
- Acceso a modelo GPT-4 de OpenAI.
- Utilizar Python 3.10+.
- Instalar las bibliotecas de Python 

    `#! pip install -r requirements.txt`
