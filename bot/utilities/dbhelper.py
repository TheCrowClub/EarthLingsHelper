from mongox import Model

from bot import db


class Helper(Model, db=db):
    help_keyword: str
    help_text: str
