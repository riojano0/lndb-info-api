import json

from typing import List
from fastapi import FastAPI, Response
from core.light_novel_info import LightNovelInfoModel
from core.scrap_info import get_light_novel_info

light_novel_app = FastAPI()


@light_novel_app.get("/info", response_model=List[LightNovelInfoModel])
def light_novel_info(light_novel: str, first_match: bool = True):
    """
        This will execute internally the search operation on http://lndb.info</br>
        queryParams:</br>
            - light_novel: Title how what are you search, example 'Goblin Slayer'</br>
            - first_match: Normally you only want the first match, </br>
                but for example the title 'Goblin Slayer'</br>
                have another match like [Goblin Slayer! Side Story: Year One, Goblin Slayer: Year One] </br>
                and maybe you want that result, or the first one is wrong cause by some variation on the title
    """
    if light_novel is not None:
        light_novel_info_list = get_light_novel_info(light_novel, first_match)
        light_novel_info_list_json = json.dumps(light_novel_info_list, default=lambda o: o.__dict__, indent=4,
                                                ensure_ascii=False)
        return Response(light_novel_info_list_json, media_type="application/json")
    else:
        return "Please send the query lightNovel with firstMatch[optional]"