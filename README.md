# Briefing con evidencia · Banco de México

**IA generativa con recuperación documental y citas verificables.** Responde
preguntas sobre dos publicaciones oficiales del Banco de México y muestra los
fragmentos exactos que respaldan cada afirmación. Si no encuentra evidencia, lo
dice: no inventa.

[![Pruebas](https://github.com/Dev-HugoAguilar/banxico-evidence-briefing/actions/workflows/tests.yml/badge.svg)](https://github.com/Dev-HugoAguilar/banxico-evidence-briefing/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Recuperación léxica](https://img.shields.io/badge/retrieval-lexical-2f855a)](#cómo-funciona-la-recuperación)

> **Alcance.** La recuperación es **léxica** (coincidencia de términos), no un
> RAG semántico con *embeddings*. La demo funciona sin Atlas y sin proveedor de
> modelos; ambas integraciones son opcionales y están apagadas por omisión.
> El corpus es una transcripción resumida de dos documentos, no una cobertura de
> la economía mexicana.

---

## Qué demuestra

- **Respuestas ancladas**: cada salida cita identificadores `[BM-…]` que apuntan a
  un fragmento concreto del corpus. Sin fragmentos, no hay respuesta.
- **Abstención explícita**: ante una pregunta fuera del corpus, el modo pasa a
  `sin-coincidencias` en lugar de improvisar.
- **Degradación controlada**: si el proveedor de modelos falla, la respuesta cae a
  modo extractivo y conserva la evidencia recuperada.
- **Cero filtración de secretos**: el diagnóstico de salud publica si hay Atlas o
  modelo activo, nunca la URI de MongoDB ni claves.
- **Serie reproducible**: la gráfica de inflación distingue dato observado de
  pronóstico publicado, y la tabla accesible repite periodo, valor, estatus y
  fuente.

## Demo local

```bash
git clone https://github.com/Dev-HugoAguilar/banxico-evidence-briefing.git
cd banxico-evidence-briefing
python -m http.server 8000 --directory web
```

Abre <http://127.0.0.1:8000/>. No hay compilación ni `npm install`: D3 se sirve
desde `web/vendor/`, sin CDN.

Prueba preguntas como *«¿Cuál fue la decisión sobre la tasa y desde cuándo
aplica?»* o *«¿Cuáles son los riesgos al alza para la inflación?»*. Y una fuera
de alcance, como *«¿Cuál es la capital de Francia?»*, para ver la abstención.

![Portada del briefing con evidencia](docs/cover.jpg)

## Instalación

El paquete de dominio (`src/app`) se instala en el entorno activo; requiere
Python 3.11 o superior.

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows · en Linux/macOS: source .venv/bin/activate
python -m pip install -e .        # con pytest: python -m pip install -e ".[dev]"
python examples/uso.py            # recuperación real sobre el corpus incluido
python -m pytest -q
```

`python -m pip install -e .` deja `app` importable desde cualquier directorio y ya
no depende de la opción `pythonpath` de pytest (que se conserva para poder correr
las pruebas sin instalar). `examples/uso.py` usa `web/corpus.json` tal cual: no
descarga nada ni necesita Atlas ni un proveedor de modelos.

**Demo estática (`web/`) frente a servicio de dominio (`src/`).** `web/` es la
aplicación que se sirve con un servidor de archivos estático: HTML, CSS y
JavaScript leen `web/corpus.json` y dibujan la respuesta con sus citas, sin Python
ni instalación. `src/app` es el servicio de dominio: recuperación léxica,
respuesta anclada a la evidencia y diagnóstico de salud. Instalar solo es
necesario para usar `src/app` como biblioteca o para correr las pruebas.

## Servicio de dominio

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Las pruebas cubren recuperación con cita, abstención, salud sin secretos,
puntuación léxica, respuesta del modelo condicionada a la evidencia y
degradación ante un proveedor que falla.

### Uso directo

```python
from app.config import Settings
from app.rag_banxico.service import BriefingBanxico

briefing = BriefingBanxico(db=None, settings=Settings())
salida = briefing.consultar("¿Cuál fue la decisión sobre la tasa?")

print(salida["mode"])                       # extractiva
print(salida["retrieval_mode"])             # corpus-local
print(salida["vector_search"])              # False
print(salida["answer"])                     # respuesta con citas [BM-…]
print(salida["evidence"][0]["chunk_id"])    # BM-2026-11-05-TASA
```

## Cómo funciona la recuperación

1. **Normalización** — minúsculas, sin acentos y sin signos, para que «decisión»
   y «decision» coincidan.
2. **Términos** — se extraen palabras de contenido y se descartan vacías.
3. **Puntuación** — cada fragmento acumula coincidencias de términos y de
   palabras clave declaradas en el corpus.
4. **Corte** — solo pasan los fragmentos con puntuación positiva; el resto se
   descarta.
5. **Respuesta** — sin modelo configurado, se concatenan los fragmentos
   recuperados y la salida se etiqueta `extractiva`. Con modelo configurado, se
   envía únicamente la evidencia recuperada y se exige citar `[BM-…]`; si el
   proveedor falla, se conserva la respuesta extractiva.

### Modos de respuesta

| `mode` | Cuándo aparece |
|---|---|
| `extractiva` | Hay evidencia y no hay proveedor de modelos. |
| `llm-grounded` | Hay evidencia y el proveedor respondió citando la fuente. |
| `extractiva-respaldo` | Hay evidencia pero el proveedor falló o no citó. |
| `sin-coincidencias` | Ningún fragmento supera el umbral de puntuación. |

## Corpus

`web/corpus.json` reúne **dos fuentes oficiales y siete fragmentos**:

| Fuente | Documento | Fragmentos |
|---|---|---|
| `BM-2026-11-05` | Anuncio de Política Monetaria, 5 nov 2026 | 4 |
| `BM-2026-08-26` | Informe trimestral, abril–junio 2026 | 3 |

La serie de inflación general conserva la meta de **3%**, cuatro trimestres
observados (2025-T4 a 2026-T3) y el pronóstico publicado desde **2026-T4**. La
línea discontinua y los puntos huecos identifican el pronóstico; la tabla
accesible repite periodo, valor, estatus y fuente. Detalle y límites en
[`docs/DATA.md`](docs/DATA.md).

## Estructura

```text
web/                        Aplicación estática (sin compilación)
  index.html                Estructura y contenido editorial
  styles.css                Sistema visual
  app.js                    Búsqueda, respuesta y gráfica
  corpus.json               Dos fuentes oficiales, siete fragmentos
  vendor/d3.min.js          D3 v7.9.2 (ISC), servido localmente
src/app/config.py           Configuración sin secretos ni rutas absolutas
src/app/rag_banxico/        Recuperación léxica, respuesta y salud
examples/uso.py             Ejemplo ejecutable sobre el corpus incluido
tests/test_service.py       Pruebas sin Atlas ni proveedor
docs/ARCHITECTURE.md        Flujo de recuperación y contrato HTTP
docs/DATA.md                Fuentes, transcripción y límites
```

La capa HTTP y la carga del corpus en MongoDB Atlas se publican por separado, en
el repositorio de infraestructura `portfolio-api`. Este repositorio contiene la
aplicación, el corpus y el servicio de dominio.

## Integraciones opcionales

Atlas y el modelo de lenguaje no son necesarios para la demo. Cuando se habilitan:

- La colección por omisión es `portfolio_demos.rag_banxico_chunks`; no se usa la
  base del portafolio ni se tocan otras colecciones.
- La carga es idempotente por `chunk_id`.
- El diagnóstico de salud informa `target` (`local` o `atlas`) sin revelar la URI
  ni las claves.

## Límites

- La recuperación léxica no comprende paráfrasis fuera del vocabulario del corpus.
- El corpus es una transcripción resumida de dos documentos; no cubre toda la
  economía mexicana ni sustituye la lectura del original.
- La demo no estima pronósticos propios: reproduce el cuadro publicado.
- La disponibilidad de Atlas y del modelo depende del entorno local; la interfaz
  siempre informa qué modo está activo.

## Datos y atribución

Fuentes: Banco de México, *Anuncio de Política Monetaria* (5 nov 2026) e *Informe
trimestral abril–junio 2026*. Cada fragmento conserva su `source_id`, título y
URL. D3 v7.9.2 se distribuye bajo licencia ISC desde `web/vendor/`. Este
repositorio no incluye un archivo `LICENSE` propio; se respetan las condiciones de
las fuentes citadas.

## Contribuir y seguridad

Convenciones y flujo de revisión en [`CONTRIBUTING.md`](CONTRIBUTING.md). Para
reportar un problema de seguridad, usa los avisos privados descritos en
[`SECURITY.md`](SECURITY.md).
