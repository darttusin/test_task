from datetime import datetime
from app.database.models import Texts
from sqlalchemy import select, delete
from sqlalchemy.orm import Session


# далс для взаимодействия с бд
class TextsDAL:
    def __init__(self, db_session: Session)  -> None:
        self.db_session: Session = db_session


    # добавление нового текста
    async def add_new_text(self, text_id: str, rubrics: str, 
                            text_: str, created_date: datetime) -> None:

        request: Texts = Texts(
            text_id=text_id,
            rubrics=rubrics,
            text_=text_,
            created_date=created_date
        )
            
        self.db_session.add(request)
        await self.db_session.flush() # type: ignore


    # получение всех текстов
    async def get_all_texts(self) -> dict:

        request = await self.db_session.execute(
            select(
                Texts.text_id, 
                Texts.text_
            )
        ) # type: ignore
        # запись запроса в словарь
        text_num = 1
        data = {}
        for row in request:
            data[str(text_num)] = row._asdict()
            text_num += 1

        return data


    # получение текста по айди
    async def get_text_by_id(self, text_id: str) -> dict:

        request = await self.db_session.execute(
            select(
                Texts.text_id, 
                Texts.text_,
                Texts.rubrics,
                Texts.created_date
            ).where(
                Texts.text_id==text_id
            )
        ) # type: ignore

        # добавление запроса в словарь, с редактированием некоторых полей
        data = {}
        for row in request:
            data = row._asdict()
            data['created_date'] = \
                data['created_date'].strftime("%Y-%m-%d %H:%M:%S")
            data['rubrics'] = \
                list(data['rubrics'][2:len(data['rubrics']) - 2].split("', '"))
        return data


    # удаление текста из бд
    async def delete_text_db(self, text_id: str) -> None:
        
        await self.db_session.execute(
            delete(Texts).where(Texts.text_id==text_id)
        ) #type: ignore
