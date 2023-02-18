from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn

from app.adapter.api.health.endpoints import router as health_router

def create_app():
    """create fastapi app
    Returns:
        FastAPI: fastapi application
    """

    fastapi_app = FastAPI()
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @fastapi_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):  # pylint: disable=W0613
        return JSONResponse(
            content=jsonable_encoder(
                {
                    "detail": f'{exc.errors()[0]["loc"][-1]} {exc.errors()[0]["msg"]}',
                    "message": "Bad request",
                    "result": None,
                }
            ),
            status_code=400,
        )

    fastapi_app.include_router(router=health_router, tags=['health'])

    return fastapi_app

app = create_app()

@app.on_event("startup")
async def startup() -> None:
    """startup method
    """
    pass    # pylint: disable=W0107

@app.on_event("shutdown")
async def on_shutdown() -> None:
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0")