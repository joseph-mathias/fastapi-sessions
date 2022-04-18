from random import randrange
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
import psycopg2

app = FastAPI()


class List(BaseModel):
    name: str
    title: str
    sports: bool = False
    status: Optional[str] = None


peoples_list = [{"name": "Joseph", "title": "Mr", "status": "single", "id": 1}, {"name": "Ruth", "title": "Ms", "id": 2}]


def find_id(id):
    for i in peoples_list:
        if i['id'] == id:
            return i


def find_index(id):
    for i, p in enumerate(peoples_list):
        if p['id'] == id:
            return i


@app.get("/lists")
async def get_all():
    return {"data": peoples_list}


@app.post("/lists", status_code=status.HTTP_201_CREATED)
def create(list: List):
    list_dict = list.dict()
    list_dict['id'] = randrange(0, 100000)
    peoples_list.append(list_dict)
    return {"data": peoples_list}


@app.get("/lists/{id}")
def get_single(id: int):
    data = find_id(id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Data with id: {id} was not found!")
    return {"data": data}


@app.delete("/lists/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data with ID: {id} was not found")
    peoples_list.pop(index)
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.put("/lists/{id}")
async def update(id: int, list: List):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data with ID: {id} was not found")
    list_dict = list.dict()
    list_dict['id'] = id
    peoples_list[index] = list_dict
    return {"data": list_dict}