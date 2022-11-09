from urllib import response
from typing import List
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel
 
DATABASE_URL = "postgresql://qvqtkcccqbhixf:07767eb05b3f44bbfea04d029da3a3ac390e7dc9122331d497c8ad1482e1c7f6@ec2-107-23-76-12.compute-1.amazonaws.com:5432/d6qrgl98nj9om6"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

menus = sqlalchemy.Table(
    "menus",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nome", sqlalchemy.String),
    sqlalchemy.Column("img", sqlalchemy.String),
    sqlalchemy.Column("preco", sqlalchemy.Integer),
    sqlalchemy.Column("revisao", sqlalchemy.Integer),
    sqlalchemy.Column("avaliacao", sqlalchemy.Integer),
    sqlalchemy.Column("categorias", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

class Menu(BaseModel):
    id: int
    nome: str
    img: str
    preco: str
    revisao: int
    avaliacao: int
    categoria: str

class MenuIn(BaseModel):
    nome: str
    img: str
    preco: str
    revisao: int
    avaliacao: int
    categoria: str


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
  

@app.get("/menu/", response_model=List[Menu])   
async def read_restaurantes():
    query = menus.select()
    return await database.fetch_all(query) 

@app.post("/menu/", response_model=Menu)   
async def create_restaurantes(menu: MenuIn):
    query = menus.insert().values(nome=menu.nome, img=menu.img, preco=menu.preco, revisao=menu.revisao, avaliacao=menu.avaliacao, categoria=menu.categoria)
    last_record_id = await database.execute(query)
    return {**menu.dict(), "id": last_record_id}