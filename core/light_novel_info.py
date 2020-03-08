from pydantic import BaseModel
from typing import List


class LightNovelInfo:

    def __init__(self, title=None, author=None, illustrator=None, plot="", genre=None, volumes=None, lndb_link=None,
                 covers=None):
        self.title = title
        self.author = author
        self.illustrator = illustrator
        self.plot = plot
        self.genre = genre
        self.volumes = volumes
        self.lndb_link = lndb_link
        self.covers = covers


class LightNovelInfoModel(BaseModel):
    title: str
    author: str
    illustrator: str
    plot: str
    genre: List[str]
    volumes: str
    lndb_link: str
    covers: List[list]
