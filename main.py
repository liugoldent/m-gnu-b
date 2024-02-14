from fastapi import FastAPI
from pydantic import BaseModel
from router.stock.index import router as stockRouter
from router.crawler.index import router as crawlerRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(stockRouter, prefix='/stock')
app.include_router(crawlerRouter, prefix='/crawler')


origins = [
    "http://localhost:3000",
    "https://golden-frontend-xi.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}
