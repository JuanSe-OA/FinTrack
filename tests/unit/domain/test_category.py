def test_category_raises_if_name_is_empty():
    with pytest.raises(ValueError, match="Category name cannot be empty"):
        Category(
            id=uuid4(),
            user_id=uuid4(),
            name="",
            type=CategoryType.EXPENSE
        )

def test_category_raises_if_name_is_whitespace():
    with pytest.raises(ValueError, match="Category name cannot be empty"):
        Category(
            id=uuid4(),
            user_id=uuid4(),
            name="   ",
            type=CategoryType.EXPENSE
        )

def test_category_created_successfully():
    category = Category(
        id=uuid4(),
        user_id=uuid4(),
        name="Comida",
        type=CategoryType.EXPENSE
    )
    assert category.name == "Comida"
    assert category.type == CategoryType.EXPENSE