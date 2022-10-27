from urllib import response
from typing import List
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel
 
DATABASE_URL = "postgresql://qlulfgqisaplnd:38f7bf02196cb17600a3fa97329848a2c628c73856182ce4f8e40582387042b1@ec2-44-195-132-31.compute-1.amazonaws.com:5432/d1eivhichip29"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("name", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("img", sqlalchemy.String),
    sqlalchemy.Column("level", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

class Note(BaseModel):
    name: str
    img: str
    level: str


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
  

@app.get("/notes/", response_model=List[Note])   
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query) 

@app.post("/notes/", response_model=List[Note])   
async def create_notes(note: Note):
    query = notes.insert().values(name=note.name, img=note.img, level=note.level)
    last_record_name = await database.execute(query)
    return {**note.dict(), "name": last_record_name}