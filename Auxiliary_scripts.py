import datetime


def get_date():
    current_date = datetime.datetime.now()
    rounded_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return rounded_date


def link_holder(id):
    list_start_links = ["https://store.steampowered.com", "https://steamcommunity.com/app/"]
    return list_start_links[id]


def extract_titles(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'title':
                yield v
            elif isinstance(v, (dict, list)):
                yield from extract_titles(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from extract_titles(item)