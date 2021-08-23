from typing import List
from Bot.Database.Services.BaseService import BaseService
from sqlalchemy.orm.session import Session
from Bot.Models.Settings import Settings


class SettingsService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)

    def create_if_not_exists(self, id: int):
        if not self.exists_by_guild(Settings, id):
            self.create_default(id)

    def create_default(self, id: int):
        default = Settings.get_default(id)
        self.create(default)

    def get_settings(self, id: int) -> Settings:
        if self.exists_by_guild(Settings, id):
            return self.read_single(Settings, id)
