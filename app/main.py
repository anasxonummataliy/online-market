from contextlib import contextmanager
from fastapi import FastAPI


app = FastAPI()
# @contextmanager
def lifespan(app: FastAPI):
    pass
    # await start_bot()
    # yield
    # await stop_bot()
