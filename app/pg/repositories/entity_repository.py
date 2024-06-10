from sqlalchemy.dialects.postgresql import insert

from base.repository import PgRepository, TBase


class EntityRepository(PgRepository):
    def __init__(self, model: type[TBase]):
        super().__init__()
        self.model = model

    async def add_entity(self, values: dict[str, str]):
        insert_stmt = insert(self.model).returning(self.model)
        entity_pk = await self.session.execute(insert_stmt, values)
        return entity_pk.scalar_one()
