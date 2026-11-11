from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query, status

from mock_ai.generator import APIMockGenerator

app = FastAPI(title="AI Mock Studio", version="0.1.0")
gen = APIMockGenerator()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/mock/{schema_name}")
def get_mock(
    schema_name: str,
    count: int = Query(default=1, ge=1, le=50),
    seed: int | None = Query(default=None),
) -> dict:
    try:
        return gen.generate_mock_for_schema(schema_name, count=count, seed=seed)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
