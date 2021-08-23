from Bot.Utils.Text import get_text
from Bot.Utils.Constance import LANG_EN
from Bot.Database import Base
from sqlalchemy import Column, String, Integer, BigInteger, Boolean


class Settings(Base):
    __tablename__ = "Settings"

    guild = Column(BigInteger, primary_key=True)
    prefix = Column(String(10), nullable=False)
    welcome_message = Column(String, nullable=False)
    delete_command_message = Column(Boolean, nullable=False)
    colour = Column(Integer, nullable=False)
    language = Column(String(5), nullable=False)

    @classmethod
    def get_default(cls, guild: BigInteger):
        return Settings(
            guild=guild,
            prefix="!",
            welcome_message="hello",
            delete_command_message=True,
            colour=0xFF55FF,
            language=LANG_EN,
        )

    def get_text_lang(self, key: str):
        return get_text(key, self.language)
