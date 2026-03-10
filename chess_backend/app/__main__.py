"""Run the API with `python -m app`."""

import uvicorn

from app.core.settings import get_settings


# PUBLIC_INTERFACE
def main() -> None:
    """Run a development uvicorn server."""
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        workers=1,
        reload=True,
    )


if __name__ == "__main__":
    main()
