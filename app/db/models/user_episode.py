from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, ForeignKey, DateTime
from .base import Base

class UserEpisode(Base):
    __tablename__ = 'user_episode'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    episode_id: Mapped[int] = mapped_column(ForeignKey('tv_episode.id'), index=True)
    like: Mapped[bool] = mapped_column(default=False)
    bookmark: Mapped[bool] = mapped_column(default=False)