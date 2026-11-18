# Arquitectura y flujo de evidencia

## Capas

```text
┌─────────────────────────────────────────────┐
│ web/  aplicación estática                   │
│  · búsqueda, respuesta, panel de evidencia  │
│  · lee corpus.json, no consulta la API      │
└───────────────────┬─────────────────────────┘
                    │ mismo contrato
┌───────────────────▼─────────────────────────┐
│ src/app/rag_banxico/service.py              │
│  · normalización y puntuación léxica        │
│  · respuesta extractiva o condicionada      │
│  · Atlas opcional, nunca obligatorio        │
└───────────────────┬─────────────────────────┘
                    │ opcional
┌───────────────────▼─────────────────────────┐
│ portfolio-api  (repositorio aparte)         │
│  · expone el servicio por HTTP              │
│  · carga idempotente del corpus en Atlas    │
└─────────────────────────────────────────────┘
```

La interfaz no necesita el servicio: la demo se sostiene con el corpus. Esta
separación permite publicar la demostración sin backend y, a la vez, mantener un
servicio auditable con pruebas propias.

## Flujo de una consulta

1. **Carga del corpus** — se valida que existan `sources`, `chunks` y `forecast`.
   Un corpus incompleto produce `CorpusError` en lugar de una respuesta parcial.
2. **Atlas opcional** — si hay base de datos y responde, se leen hasta 500
   documentos de la colección dedicada. Cualquier excepción se absorbe: la demo no
   falla por una integración ausente.
3. **Normalización** — minúsculas, sin diacríticos y sin signos.
4. **Puntuación léxica** — coincidencia de términos de la pregunta y de las
   palabras clave del fragmento. Solo pasan los fragmentos con puntuación
   positiva.
5. **Abstención** — sin evidencia, `mode = "sin-coincidencias"` y un mensaje
   explícito. No se genera texto libre.
6. **Respuesta** — sin proveedor configurado, se concatenan los fragmentos
   recuperados y se etiqueta `extractiva`. Con proveedor, se envían únicamente los
   fragmentos y se exige la cita `[BM-…]`.
7. **Verificación de cita** — si la respuesta del proveedor no cita las fuentes
   recuperadas, se descarta y se usa la respuesta extractiva
   (`extractiva-respaldo`).

## Modos y señales

| Señal | Significado |
|---|---|
| `retrieval_mode` | `corpus-local` cuando la evidencia vino del corpus. |
| `vector_search` | Siempre `false`: no hay índice vectorial. |
| `mode` | `extractiva`, `llm-grounded`, `extractiva-respaldo`, `sin-coincidencias`. |
| `evidence` | Lista de fragmentos con `chunk_id`, `source_id` y encabezado. |

## Postura de seguridad

- El diagnóstico de salud publica capacidades, no credenciales: expone
  `target` (`local` / `atlas`) y `configured`, nunca la URI ni la clave.
- El corpus se trata como **datos**: el servicio no interpreta su contenido como
  instrucciones.
- La integración con MongoDB es de solo lectura durante una consulta.

## Contrato HTTP (implementado en `portfolio-api`)

| Método | Ruta | Respuesta |
|---|---|---|
| `GET` | `/api/v1/briefing-banxico/health` | Salud, conteo del corpus y capacidades. |
| `GET` | `/api/v1/briefing-banxico/corpus` | Corpus servido por la API. |
| `GET` | `/api/v1/briefing-banxico/query?question=…` | Respuesta con evidencia. |

El cuerpo de estas rutas es exactamente el diccionario que devuelve
`consultar()` en `service.py`; la API solo añade validación de parámetros.

## No objetivos

- No es un sistema de recuperación semántica ni un índice vectorial.
- No estima pronósticos propios: reproduce el cuadro publicado.
- No cubre la economía mexicana: cubre dos documentos y lo declara.
