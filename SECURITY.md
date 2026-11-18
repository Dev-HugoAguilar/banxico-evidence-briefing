# Política de seguridad

## Alcance

La demo se ejecuta por completo en el navegador y funciona solo con
`web/corpus.json`. El servicio de dominio lee el corpus y, opcionalmente, una
colección de MongoDB y un proveedor de modelos.

El repositorio **no contiene credenciales**: la configuración usa valores por
omisión inocuos y espera variables de entorno para cualquier integración. El
diagnóstico de salud publica si hay Atlas o modelo activos, pero nunca la URI de
MongoDB ni claves.

## Cómo reportar

Si encuentras una vulnerabilidad, usa los **avisos privados de seguridad** de
GitHub: pestaña *Security* → *Report a vulnerability*. Evita abrir un *issue*
público con detalles explotables.

Incluye, cuando aplique:

- versión o commit afectado;
- pasos mínimos para reproducir;
- impacto esperado y observable;
- cualquier mitigación que ya hayas probado.

## Riesgos conocidos y decisiones

- **Fuga de secretos en la salud**: las pruebas verifican que `salud()` no
  serialice la URI ni la clave. Cualquier campo nuevo se prueba con la misma
  aserción.
- **Contenido no confiable**: los fragmentos del corpus son datos, no
  instrucciones. El servicio no ejecuta acciones a partir del texto recuperado.
- **Proveedor de modelos**: si se configura, recibe únicamente evidencia
  recuperada y su respuesta se contrasta con los identificadores citados. Un
  fallo del proveedor degrada a modo extractivo en lugar de fallar en silencio.

## Buenas prácticas para quien despliega

- No añadas credenciales al repositorio; usa variables de entorno.
- Sirve la demo detrás de HTTPS si la expones fuera de `127.0.0.1`.
- Usa una colección dedicada y un usuario de MongoDB con permiso de solo lectura.
- Revisa el resultado de la verificación de credenciales de la integración
  continua antes de fusionar cambios.
