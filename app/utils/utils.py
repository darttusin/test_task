import uuid


# генерация айди текста
async def generate_text_id() -> str:
    text_id: str = 'text_' + str(uuid.uuid4().int)
    return text_id
