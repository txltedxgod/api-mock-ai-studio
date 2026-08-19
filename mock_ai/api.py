from fastapi import FastAPI
from mock_ai.generator import APIMockGenerator

app = FastAPI(title="AI Mock Studio", version="0.1.0")
gen = APIMockGenerator()

@app.get("/api/v1/mock/{schema_name}")
def get_mock(schema_name: str):
    return gen.generate_mock_for_schema(schema_name)
