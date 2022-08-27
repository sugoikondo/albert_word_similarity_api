from fastapi import FastAPI
from containers import Container
import endpoints


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()


@app.get("/healthcheck")
def health_check():
    return {"Hello": "World"}
