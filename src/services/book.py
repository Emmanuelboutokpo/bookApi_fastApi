from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.book import BookSchema
from sqlmodel import select, desc
from src.model.book import Book as BookModel
from datetime import datetime

class BookService:
    async def create_book(self, book_data: BookSchema, user_uid: str, session : AsyncSession):
        book_data_dict = book_data.model_dump()
        for field in ["published_date", "created_at", "updated_at"]:
             value = book_data_dict.get(field)
             if isinstance(value, str):
                clean_date = value.replace("Z", "+00:00")
                book_data_dict[field] = datetime.fromisoformat(clean_date)
        new_book = BookModel(**book_data_dict)
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        return new_book

    async def get_book(self, book_id: str, session : AsyncSession):
        statement = select(BookModel).where(BookModel.id == book_id)
        result = await session.execute(statement)
        book = result.scalar()
        if book is None:
            return None
        return book

    async def get_books(self, session : AsyncSession):
        statement = select(BookModel).order_by(desc(BookModel.created_at))
        execution = await session.execute(statement)
        result = execution.scalars().all()
        return result
    
    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = (
            select(BookModel)
            .where(BookModel.user_uid == user_uid)
            .order_by(desc(BookModel.created_at))
        )

        result = await session.exec(statement)

        return result.all()

    async def update_book(self, book_id: str, book_data: BookSchema, session: AsyncSession):
        book_to_update = await self.get_book(book_id, session)
    
        if not book_to_update:
            return None

        book_data_dict = book_data.model_dump(exclude_unset=True)

        for key, value in book_data_dict.items():
          if key in ["published_date"] and isinstance(value, str):
             value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        
          setattr(book_to_update, key, value)

        await session.commit()
        return book_to_update

    async def delete_book(self, book_id: str, session : AsyncSession):
        book_to_delete = await self.get_book(book_id, session)
        if not book_to_delete:
            return None
        await session.delete(book_to_delete)
        await session.commit()
        return book_to_delete