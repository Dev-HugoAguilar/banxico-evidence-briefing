# Cómo contribuir

Gracias por revisar este proyecto. Es una pieza de portafolio con alcance
deliberadamente acotado; las contribuciones más útiles son las que mejoran la
calidad de la evidencia, la claridad de la abstención o la accesibilidad de la
demo.

## Entorno

- Python 3.11 o superior para el servicio de dominio.
- Cualquier navegador moderno para la demo. No hay compilación ni `node_modules`.

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Para revisar la interfaz:

```bash
python -m http.server 8000 --directory web
```

## Estructura del paquete

`src/app` replica a propósito el espacio de nombres del backend del portafolio.
Así, sincronizar un cambio entre este repositorio y el proyecto original es una
copia directa del archivo, fácil de revisar en un *diff*. No renombres el paquete
sin actualizar ambos lados.

## Cambios en el corpus

El corpus es la fuente de verdad de las respuestas. Si editas `web/corpus.json`:

- añade o modifica `sources` antes de referenciarlas desde un `chunk`;
- conserva la estructura `chunk_id`, `source_id`, `heading`, `content`,
  `keywords`;
- no inventes cifras: transcribe del documento oficial y conserva su URL;
- mantén el pronóstico separado de lo observado mediante `status`;
- actualiza `docs/DATA.md` si cambia la cobertura o la fecha del snapshot.

Una respuesta nueva **no** debe construirse ampliando el vocabulario del corpus
con sinónimos que el documento no usa: la recuperación es léxica y declara esa
limitación a propósito.

## Convenciones

- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/).
  Prefijos usados: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `perf`,
  `ci`, `style`. Ámbito opcional en minúsculas, por ejemplo
  `fix(rag): descarta fragmentos sin coincidencia de términos`.
- **Idioma**: documentación y mensajes de interfaz en español; identificadores,
  mensajes de commit y nombres de archivo técnicos pueden ir en inglés.
- **Estilo**: 4 espacios en Python, 2 en CSS/JS/HTML, línea de 100 columnas.
- **Pruebas**: cualquier cambio de comportamiento necesita una prueba que falle
  antes del cambio y pase después.

## Reglas de alcance

Un cambio que introduzca cualquiera de las siguientes cosas debe discutirse antes
en un *issue*:

- un servicio de *embeddings* o un índice vectorial presentado como equivalente;
- una llamada de red obligatoria para que la demo funcione;
- credenciales, cadenas de conexión o datos personales en el repositorio;
- respuestas generadas sin evidencia recuperada.

## Flujo de revisión

1. Abre un *issue* que describa el problema observable.
2. Trabaja en una rama corta: `feat/…`, `fix/…` o `docs/…`.
3. Asegura `python -m pytest` en verde y la interfaz sin errores de consola.
4. Envía el *pull request* con contexto, decisión y evidencia del cambio.
