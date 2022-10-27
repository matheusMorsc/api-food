from urllib import response
from typing import List
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel
 
DATABASE_URL = "postgresql://kvlbqwzwyclxdr:cea72d3c43d03759206e20040f6e30363d11543223ff69ed311628471e5f87cb@ec2-44-209-57-4.compute-1.amazonaws.com:5432/d96saoa1b6nr5k"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean)
)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)

metadata.create_all(engine)

class Note(BaseModel):
    id: int
    text: str
    completed: bool

class NoteIn(BaseModel):
    text: str
    completed: bool


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
async def create_notes(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}