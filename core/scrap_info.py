import bs4
import cfscrape
import logging

from core.light_novel_info import LightNovelInfo


def create_light_novel_info(match, scrape_instance):
    content_url = match.get("href")
    view_url = "http://lndb.info/light_novel/view/{}".format(content_url.split("/")[-1])
    fetch_message = "Fetch information from: {}".format(view_url)
    logging.info(fetch_message)
    light_novel_page = scrape_instance.get(view_url, headers={
        "Referer": content_url,
        "Connection": "keep-alive",
        "host": "lndb.info",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    })
    light_novel_page_soup = bs4.BeautifulSoup(light_novel_page.content, "html.parser")

    light_novel_title = content_url.split("/")[-1].replace("_", " ")
    information_message = "Fetch information from light novel: {}".format(light_novel_title)
    logging.info(information_message)
    light_novel_info = LightNovelInfo(title=light_novel_title, lndb_link=content_url)
    secondary_info = light_novel_page_soup.find("div", {"class": "secondary-info"})
    if secondary_info is not None:
        info_values = secondary_info.findAll("td", {"class": "secondary-info-value"})

        for info_value in info_values:
            info_key = info_value.parent.find("td")
            if "Author" in info_key.text:
                light_novel_info.author = info_value.text.strip()
            if "Illustrator" in info_key.text:
                light_novel_info.illustrator = info_value.text.strip()
            if "Genre" in info_key.text:
                genres = info_value.text.split(",")
                light_novel_info.genre = [genre.lstrip() for genre in genres]
            if "Volumes" in info_key.text:
                light_novel_info.volumes = info_value.text

    cover_section = light_novel_page_soup.find("div", {"class": "lightnovelcovers"})
    cover_element_list = cover_section.findAll("a", {"class": "highslide"}) if cover_section is not None else []
    covers = {}
    for volume_number, cover_element in enumerate(cover_element_list, start=1):
        covers[volume_number] = "http://lndb.info/{}".format(cover_element.get("href"))

    light_novel_info.covers = covers

    return light_novel_info


def get_light_novel_info(title, first_match_flag=True):
    scrape = cfscrape.create_scraper()
    lndb_info_query = "http://lndb.info/search?text={}".format(title)
    logging.info("Requesting: {}".format(lndb_info_query))
    page = scrape.get(lndb_info_query,
                      headers={"connection": "keep-alive", "host": "lndb.info"})
    search_result = bs4.BeautifulSoup(page.content, "html.parser")

    light_novels = []
    if "search?text=" in page.url:
        light_novel_list = search_result.find("div", {"id": "bodylightnovelscontentid"})

        matches = []
        if light_novel_list is not None:
            matches = light_novel_list.findAll("a")

        if len(matches) > 0:
            if first_match_flag:
                match = matches[0]
                light_novels.append(create_light_novel_info(match, scrape))
            else:
                for match in matches:
                    light_novels.append(create_light_novel_info(match, scrape))
    else:
        # Only exist one match, and that page is returned
        match = {"href": page.url}
        light_novels.append(create_light_novel_info(match, scrape))

    return light_novels


if __name__ == "__main__":
    infos = get_light_novel_info("goblin slayer", first_match_flag=False)
    for info in infos:
        print(info.__dict__)
