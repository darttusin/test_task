from elasticsearch import AsyncElasticsearch
from typing import Any


class ElasticSearchConnector:
    
    def __init__(self) -> None:
        self.es: AsyncElasticsearch = AsyncElasticsearch(
            [{"host": "elasticsearch", "port": 9200, 
              "scheme": "http", "use_ssl" : False}]
        )

    async def create_index(self, name: str) -> None:
        if await self.es.indices.exists(index=name):
            await self.es.indices.delete(index=name)
        await self.es.indices.create(index=name)

    async def add_body(self, 
                       index_name: str, text: str) -> None:
        if await self.es.indices.exists(index=index_name):
            await self.es.index(index=index_name, body=text)

    async def search(self, 
                     index_name: str, text: str) -> Any:
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
        if await self.es.indices.exists(index=index_name):
            return await self.es.search(index=index_name, body=payload)
        return None
    
    async def delete(self,
                     index_name: str,
                     text_id: str
                     ) -> None:
        if await self.es.indices.exists(index=index_name):
            payload = {
                "query": { 
                    "match": {
                        "text_id": text_id
                    }
                }
            }
            r = await es.index(index="texts", body=payload) # type: ignore
            await self.es.delete(index=index_name, id=r['_id'])
