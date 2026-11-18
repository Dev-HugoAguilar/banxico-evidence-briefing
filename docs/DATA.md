# Datos: fuentes, transcripción y límites

## Fuentes

| `source_id` | Documento | Fecha | Tipo |
|---|---|---|---|
| `BM-2026-11-05` | Anuncio de Política Monetaria | 2026-11-05 | Comunicado |
| `BM-2026-08-26` | Informe trimestral, abril–junio 2026 | 2026-08-26 | Informe |

Cada fuente conserva en `web/corpus.json` su título, fecha, tipo y URL oficial.
El snapshot del corpus es del **2026-11-15**.

## Fragmentos

Siete fragmentos, cada uno con `chunk_id`, `source_id`, encabezado, contenido y
palabras clave.

| `chunk_id` | Encabezado |
|---|---|
| `BM-2026-11-05-TASA` | Decisión sobre la tasa |
| `BM-2026-11-05-INFLACION` | Inflación de septiembre a octubre |
| `BM-2026-11-05-RIESGOS` | Balance de riesgos para la inflación |
| `BM-2026-11-05-PRONOSTICO` | Pronósticos trimestrales de inflación general |
| `BM-2026-08-26-INFLACION-TRIMESTRAL` | Inflación entre el primer y segundo trimestre |
| `BM-2026-08-26-META` | Meta de inflación |
| `BM-2026-08-26-ACTIVIDAD` | Actividad económica nacional |

## Serie de inflación

`forecast` conserva la meta general de **3%** y dos trayectorias (general y
subyacente) con cuatro trimestres observados —2025-T4 a 2026-T3— y el pronóstico
publicado desde **2026-T4**.

El campo `status` distingue `observado` de `pronóstico`. La interfaz usa línea
discontinua y puntos huecos para el pronóstico, y la tabla accesible repite
periodo, valor, estatus y fuente. Ningún valor se interpola ni se extrapola.

## Naturaleza del corpus

El corpus es una **transcripción resumida** de los documentos citados, no una
reproducción literal ni una base de datos oficial. Para una decisión real debe
consultarse el documento original enlazado en cada fuente.

## Atribución

> Banco de México. *Anuncio de Política Monetaria* (5 de noviembre de 2026) e
> *Informe trimestral abril–junio 2026*. Se cita el documento y el fragmento en
> cada respuesta.

`web/vendor/d3.min.js` corresponde a D3 **v7.9.2**, distribuido bajo licencia
**ISC** por Mike Bostock y colaboradores.

Este repositorio no incluye un archivo `LICENSE` propio. Las condiciones de las
fuentes citadas se respetan y se documentan aquí.

## Límites de interpretación

- La recuperación es léxica: no comprende sinónimos ni paráfrasis fuera del
  vocabulario del corpus.
- El corpus cubre dos documentos; no es una cobertura de la economía mexicana.
- La demo no genera pronósticos propios, no recalcula tasas implícitas y no
  modela escenarios.
- Las cifras mostradas corresponden al corte publicado; no se actualizan solas.
- Una pregunta sin coincidencias recibe una abstención explícita, no una
  aproximación.
