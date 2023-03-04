from datetime import datetime
import asyncpg

from app.database.dals import TextsDAL
from app.utils.utils import generate_text_id
from app.constants.enviroment import DBHOST, DBNAME, DBPASSWORD, DBPORT, DBUSER
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker


# создание базы данных при инициализации
async def create_db() -> None:
    connection: asyncpg.Connection = await asyncpg.connect(
        user=DBUSER, 
        password=DBPASSWORD, 
        database=DBNAME, 
        host=DBHOST
    )
    try:
        await connection.execute("SELECT * FROM texts;")
        await connection.execute("DROP TABLE texts;")
    except:
        pass
    await connection.execute("CREATE TABLE texts(text_id TEXT PRIMARY KEY, rubrics TEXT, text_ TEXT, created_date TIMESTAMP WITH TIME ZONE);")


# подключение к бд
url: str = f"postgresql+asyncpg://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"
engine: AsyncEngine = create_async_engine(url, future=True, echo=False)
async_session: sessionmaker = sessionmaker(
                        engine, expire_on_commit=False, class_=AsyncSession)


# добавление текстов из csv и создание бд
async def add_new_texts(df) -> None:
    
    await create_db()

    async with async_session() as session: # type: ignore
        async with session.begin():
            dal = TextsDAL(session)
            for row in df.itertuples():
                text_id = await generate_text_id()
                await dal.add_new_text(
                    text_id=text_id,
                    text_=row.text,
                    created_date=datetime.strptime(row.created_date, "%Y-%m-%d %H:%M:%S"),
                    rubrics=row.rubrics
                )

# получить все тексты для добавления в index
async def get_all_texts() -> dict:

    async with async_session() as session: #type: ignore
        async with session.begin():
            dal = TextsDAL(session)
            return await dal.get_all_texts()
        

# получить текст по айди
async def get_text_by_id(text_id: str) -> dict:

    async with async_session() as session: #type: ignore
        async with session.begin():
            dal = TextsDAL(session)
            return await dal.get_text_by_id(text_id)


# удалить текст и бд
async def delete_text_db(text_id: str) -> None:

    async with async_session() as session: #type: ignore
        async with session.begin():
            dal = TextsDAL(session)
            await dal.delete_text_db(text_id)
