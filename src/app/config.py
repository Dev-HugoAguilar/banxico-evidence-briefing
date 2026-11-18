"""Configuración mínima del briefing con evidencia.

Solo dos cosas son necesarias para que la demo funcione: el corpus y un objeto
de base de datos (opcional). Este módulo declara los campos que el servicio
consume y deja todas las integraciones externas apagadas por omisión.

Decisiones deliberadas:

- ``env_file=None``: nunca se descubre un ``.env`` del sistema.
- ``mongodb_uri`` apunta a una instancia local y solo se usa para derivar una
  etiqueta (``local`` / ``atlas``); nunca se serializa en una respuesta.
- Las credenciales del proveedor de modelos son ``None`` por omisión, de modo
  que un clon limpio responde en modo extractivo.
"""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

#: Raíz del repositorio (``src/app/config.py`` → tres niveles arriba).
REPO_ROOT = Path(__file__).resolve().parents[2]
#: Aplicación estática incluida en el repositorio.
WEB_APP = REPO_ROOT / "web"
#: Documentación y material de apoyo.
DOCS_DIR = REPO_ROOT / "docs"


class Settings(BaseSettings):
    """Ajustes del servicio.

    Todos los campos tienen un valor por omisión válido para un clon limpio; la
    demo no necesita Atlas ni un proveedor de modelos para funcionar.
    """

    model_config = SettingsConfigDict(
        env_file=None,
        env_prefix="",
        extra="ignore",
        case_sensitive=False,
    )

    #: Corpus documental versionado. Se abre en modo lectura.
    rag_banxico_corpus_path: str = str(WEB_APP / "corpus.json")
    #: URI de MongoDB. Solo se usa para derivar la etiqueta ``local`` / ``atlas``.
    mongodb_uri: str = "mongodb://127.0.0.1:27017/portfolio_demos"
    #: Base y colección de Atlas usadas por la integración opcional.
    rag_banxico_mongodb_db: str = "portfolio_demos"
    rag_banxico_collection: str = "rag_banxico_chunks"
    #: Proveedor de modelos opcional. Sin las tres variables, la respuesta es
    #: extractiva y se etiqueta como tal.
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
