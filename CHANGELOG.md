# Historial de cambios

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
las versiones usan [Versionado Semántico](https://semver.org/lang/es/).

## [1.0.0] — 2026-11-26

### Añadido

- Primera publicación como repositorio independiente.
- Aplicación estática de *briefing* con búsqueda, respuesta citada, panel de
  evidencia y gráfica de inflación con datos observados y pronóstico.
- Corpus versionado con dos fuentes oficiales del Banco de México y siete
  fragmentos con palabras clave.
- Recuperación léxica determinista con abstención explícita cuando no hay
  evidencia.
- Cuatro modos de respuesta (`extractiva`, `llm-grounded`, `extractiva-respaldo`,
  `sin-coincidencias`) y degradación controlada ante fallos del proveedor.
- Integración opcional con una colección dedicada de MongoDB Atlas; apagada por
  omisión.
- Diagnóstico de salud que informa capacidades sin exponer URI ni claves.
- Seis pruebas de dominio sin red obligatoria.
- Integración continua que ejecuta las pruebas y verifica que no se publiquen
  credenciales.

### Nota

El repositorio se extrae del portafolio de datos de Hugo Aguilar. La capa HTTP y
la carga del corpus en Atlas permanecen en el repositorio de infraestructura
`portfolio-api`.
