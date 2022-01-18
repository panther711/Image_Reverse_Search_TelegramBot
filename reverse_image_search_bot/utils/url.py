import re

from emoji import emojize
from telegram import InlineKeyboardButton
from yarl import URL


def fix_url(url: URL | str) -> URL:
    url = URL(url)

    match url.host:
        case "i.pximg.net":
            art_id_match = re.match(r"^\d+", next(reversed(url.parts)))
            if art_id_match:
                art_id = art_id_match[0]
                return URL("https://www.pixiv.net/artworks/" + art_id)

    return url


def url_icon(url: URL | str, with_icon: bool = True, with_text: bool = True, custom_text: str = None) -> str:
    url = URL(url)

    icon = ":globe_with_meridians:"
    match url.host:
        case "twitter.com":
            text = "Twitter"
            icon = ":bird:"
        case "www.pixiv.net" | "pixiv.net" | "i.pximg.net":
            text = "Pixiv"
            icon = ":P_button:"
        case "danbooru.donmai.us":
            text = "Danbooru"
            icon = ":package:"
        case "yande.re":
            text = "Yandere"
        case _:
            text = url.host.split(".")[-2].title()  # type: ignore

    if custom_text:
        text = custom_text
    if not with_text:
        text = ""
    if not with_icon:
        icon = ""
    return emojize(f"{icon} {text}", use_aliases=True)


def url_button(
    url: URL | str, with_icon: bool = True, with_text: bool = True, fix_url_: bool = True, text: str = None
) -> InlineKeyboardButton:
    if fix_url_:
        url = fix_url(url)
    return InlineKeyboardButton(text=url_icon(url, with_icon, with_text, text), url=str(url))
