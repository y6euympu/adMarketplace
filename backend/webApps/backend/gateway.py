from fastapi import FastAPI
import uvicorn

from core.container import Container
from core.config import settings


class Gateway:
    def __init__(self, container: Container, handlers: list) -> None:
        self.project = FastAPI()
        self.project.state.container = container

    async def host(
        self, host: str = "localhost", port: int = 8888, reload: bool = False
    ) -> None:
        config = uvicorn.Config(
            app=self.project, host=host, port=port, reload=reload
        )
        
        await uvicorn.Server(config).serve()


gateway = Gateway(container=Container(settings), handlers=handlers)