from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    published: Mapped[bool] = mapped_column()

 