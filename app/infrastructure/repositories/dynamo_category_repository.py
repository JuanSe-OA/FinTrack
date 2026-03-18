from uuid import UUID

from boto3.dynamodb.conditions import Attr, Key 
from app.domain.entities.category import Category, CategoryType
from app.domain.repositories.category_repository import CategoryRepository


class DynamoCategoryRepository(CategoryRepository):

    def __init__(self, table):
        self.table = table

    def add(self, category: Category) -> None:
        self.table.put_item(Item={
            "PK": f"USER#{category.user_id}",
            "SK": f"CATEGORY#{category.id}",
            "id": str(category.id),
            "name": category.name, 
            "user_id": str(category.user_id),
            "type" : category.type.value
        })

    def get_by_id(self, user_id: UUID, category_id: UUID) -> Category | None:
        response = self.table.get_item(Key={
            "PK": f"USER#{user_id}",
            "SK": f"CATEGORY#{category_id}"
        })
        item = response.get("Item")
        if not item:
            return None
        return self._to_entity(item)
    

    def get_by_name(self, name: str) -> Category | None:
        response = self.table.scan(
            FilterExpression=Attr("name").eq(name)
        )
        items = response.get("Items", [])
        return self._to_entity(items[0]) if items else None
    


    def get_all_by_user_id(self, user_id: UUID) -> list[Category]:
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("CATEGORY#")
        )
        return [self._to_entity(item) for item in response.get("Items", [])]
    

    def get_all_by_user_id_and_type(self, user_id: UUID, type: CategoryType) -> list[Category]:
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("CATEGORY#"),
            FilterExpression=Attr("type").eq(type.value)
        )
        return [self._to_entity(item) for item in response.get("Items", [])]
    

    def delete(self, category_id: UUID, user_id: UUID) -> None:
        self.table.delete_item(Key={
            "PK": f"USER#{user_id}",
            "SK": f"CATEGORY#{category_id}"
        })

    def _to_entity(self, item: dict) -> Category:
        return Category(
            id=UUID(item["id"]),
            user_id=UUID(item["PK"].replace("USER#", "")),
            name=item["name"],
            type=CategoryType(item["type"]),
        )
    

    def get_by_user_and_name(self, user_id: UUID, name: str) -> Category | None:
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("CATEGORY#"),
            FilterExpression=Attr("name").eq(name)
        )
        items = response.get("Items", [])
        return self._to_entity(items[0]) if items else None