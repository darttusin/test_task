import pandas as pd # type: ignore
from app.database.db import (
    add_new_texts, get_all_texts, 
    get_text_by_id, delete_text_db
)
from fastapi import APIRouter
from app.utils.es_connector import ElasticSearchConnector

router: APIRouter = APIRouter()

es: ElasticSearchConnector = ElasticSearchConnector()


# инициализация сервиса, добавление текста в бд и в index
@router.get("/initialize")
async def create_index() -> dict:

    # добавление текстов в бд
    data = pd.read_csv(r'./app/files/posts.csv')   
    df = pd.DataFrame(data)
    await add_new_texts(df)

    await es.create_index("texts")

    # создание и заполнение index
    all_texts = await get_all_texts()
    for i in all_texts:
        current_text = all_texts[i]
        await es.create_index("texts", current_text) #type: ignore

    return {"detail" : "successful"}


# поиск текста по индексу
@router.get("/find={text}")
async def find_docs(text: str) -> dict:

    resp = await es.search("texts", text)
    if resp is None:
        return {"error": "no index"}
    # добавление результата в словарь
    responces = {}
    num = 1
    for i in resp['hits']['hits']:
        text_id = i['_source']['text_id']
        responces[num] = await get_text_by_id(text_id)
        num += 1

    return dict(sorted(responces.items(), 
                       key= lambda x: x[1].get("created_date"), 
                       reverse=True)
    )


# удаление по text_id текста из index и бд
@router.get("/delete={text_id}")
async def delete_text(text_id: str) -> str:
    await es.delete("texts", text_id)
    await delete_text_db(text_id)

    return "successful delete text"
