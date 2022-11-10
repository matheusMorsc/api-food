from urllib import response
from typing import List
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel
 
DATABASE_URL = "postgresql://ftrhsjtstmpeje:17df4f3741976fb20e3905810153598ba865061e72b65f7954a94832f1231c92@ec2-18-215-41-121.compute-1.amazonaws.com:5432/d3am4gch1nbf8m"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

menus = sqlalchemy.Table(
    "menus",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nome", sqlalchemy.String),
    sqlalchemy.Column("img", sqlalchemy.String),
    sqlalchemy.Column("preco", sqlalchemy.String),
    sqlalchemy.Column("revisao", sqlalchemy.Integer),
    sqlalchemy.Column("avaliacao", sqlalchemy.Integer),
    sqlalchemy.Column("categoria", sqlalchemy.String),
)

itens = sqlalchemy.Table(
    "itens",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("subid", sqlalchemy.Integer),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.String),
    sqlalchemy.Column("image", sqlalchemy.String),
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

class Item(BaseModel):
    id: int
    subid: int
    title: str
    description: str
    price: str
    image: str

class ItemIn(BaseModel):
    subid: int
    title: str
    description: str
    price: str
    image: str

app = FastAPI()

## INCICIO E FIM

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    
## RESTAURANTES
  
@app.get("/menu/", response_model=List[Menu])   
async def read_restaurantes():
    query = menus.select()
    return await database.fetch_all(query) 

@app.post("/menu/", response_model=Menu)   
async def create_restaurantes(menu: MenuIn):
    query = menus.insert().values(nome=menu.nome, img=menu.img, preco=menu.preco, revisao=menu.revisao, avaliacao=menu.avaliacao, categoria=menu.categoria)
    last_record_id = await database.execute(query)
    return {**menu.dict(), "id": last_record_id}

## ITENS

@app.get("/item/", response_model=List[Item])   
async def read_item():
    query = itens.select()
    return await database.fetch_all(query)

@app.get("/item/{subid}", response_model=List[Item])   
async def read_item_by_id(subid:int):
    query = itens.select().where(itens.c.subid == subid)
    return await database.fetch_all(query)
    
@app.post("/item/", response_model=Item)   
async def create_item(item: ItemIn):
    query = itens.insert().values(title=item.title, image=item.image, price=item.price, description=item.description, subid=item.subid)
    last_record_id2 = await database.execute(query)
    return {**item.dict(), "id": last_record_id2}