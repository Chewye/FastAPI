from enum import Enum
from fastapi import FastAPI, Path
from pydantic import BaseModel


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return 'string'


@app.post('/post', response_model=Timestamp)
def get_post_():   
    return post_db[0]


@app.get('/dog', response_model=list[Dog])
def get_dogs(kind: DogType):
    
    result = [{'name': i.name, 'pk': i.pk, 'kind': i.kind.value} for i in dogs_db.values() if i.kind.value==kind]
    return result


@app.post('/dog', response_model=Dog)
def create_dog(body: Dog):
    dogs_db[body.pk] = body
    return body


@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int= Path(..., gt=min(dogs_db.keys()), le=max(dogs_db.keys()))):
    return dogs_db[pk]


@app.patch('/dog/{pk}', response_model=Dog)
def update_dog(body: Dog, pk: int= Path(..., gt=min(dogs_db.keys()), le=max(dogs_db.keys()))):
    dogs_db[pk] = body
    return body

