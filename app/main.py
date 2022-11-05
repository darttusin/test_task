import pandas as pd
from app.database.db import add_new_texts, get_all_texts, get_text_by_id, delete_text_db
import asyncio
from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch


app = FastAPI()

es = AsyncElasticsearch("http://localhost:9200")


# инициализация сервиса, добавление текста в бд и в index
@app.get("/initiaize")
async def create_index() -> dict:

    if await es.indices.exists(index="texts"):
        await es.indices.delete(index="texts")

    # добавление текстов в бд
    data = pd.read_csv(r'./app/files/posts.csv')   
    df = pd.DataFrame(data)
    await add_new_texts(df)

    # создание и заполнение index
    await es.indices.create(index="texts")
    all_texts = await get_all_texts()
    for i in all_texts:
        current_text = all_texts[i]
        await es.index(index="texts", document=current_text, ignore=400)
    await es.close()

    return {"detail" : "successful"}


# поиск текста по индексу
@app.get("/find={text}")
async def find_docs(text: str) -> dict:
    payload = {
        "size": 20,
        "query": { 
            "bool": { 
                "must": [
                    { "match": { "text_": text}}
                ]
                }
            }
        }
    resp = await es.search(index="texts", body=payload)

    # добавление результата в словарь
    responces = {}
    num = 1
    for i in resp['hits']['hits']:
        text_id = i['_source']['text_id']
        responces[num] = await get_text_by_id(text_id)
        num += 1

    return dict(sorted(responces.items(), key= lambda x: x[1].get("created_date"), reverse=True))


# удаление по text_id текста из index и бд
@app.get("/delete={text_id}")
async def delete_text(text_id: str) -> dict:
    payload = {
    "query": { 
        "match": {
            "text_id": text_id
            }
        }
    }
    r = await es.index(index="texts", body=payload)
    await es.delete(index="texts", id=r['_id'])

    await delete_text_db(text_id)

    return "successful delete text"
