"""Ejemplo ejecutable de extremo a extremo del briefing con evidencia.

Uso::

    python examples/uso.py

Requiere el paquete instalado (``python -m pip install -e .``). Usa el corpus
incluido en ``web/corpus.json`` y ejecuta el flujo completo: recuperación léxica
-> respuesta anclada a las fuentes recuperadas. No hay Atlas ni proveedor de
modelos configurados, así que la respuesta es extractiva y se etiqueta como tal.
"""

from __future__ import annotations

from app.config import Settings
from app.rag_banxico.service import BriefingBanxico

PREGUNTA = "¿Cuál fue la decisión sobre la tasa y desde cuándo aplica?"


def main() -> int:
    briefing = BriefingBanxico(db=None, settings=Settings())

    salud = briefing.salud()
    print(f"Fragmentos del corpus: {salud['corpus_chunks']}")
    print(f"Snapshot del corpus: {salud['corpus_snapshot']}")
    print(f"Recuperación: {salud['retrieval']} · búsqueda vectorial: {salud['vector_search']}")
    print(f"Pregunta: {PREGUNTA}")

    salida = briefing.consultar(PREGUNTA)

    print(f"Modo de respuesta: {salida['mode']}")
    print(f"Modo de recuperación: {salida['retrieval_mode']}")
    print(f"Evidencias recuperadas: {len(salida['evidence'])}")
    for fragmento in salida["evidence"]:
        print(f"  · {fragmento['chunk_id']} · {fragmento['heading']}")
    print(f"Respuesta ({len(salida['answer'])} caracteres):")
    print(salida["answer"])

    # Comprobación explícita de lo que se acaba de imprimir.
    assert salud["corpus_chunks"] == 7, salud["corpus_chunks"]
    assert salida["mode"] == "extractiva", salida["mode"]
    assert salida["retrieval_mode"] == "corpus-local", salida["retrieval_mode"]
    assert any(item["chunk_id"] == "BM-2026-11-05-TASA" for item in salida["evidence"]), salida[
        "evidence"
    ]

    print("OK · recuperación con cita verificada")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
