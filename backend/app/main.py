from fastapi import FastAPI

app = FastAPI(title="Sdone")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
