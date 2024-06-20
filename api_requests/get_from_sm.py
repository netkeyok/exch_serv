import asyncio
import json

from api_models.Supermag import USIOMESABBREVINFO
from config_urls import smcard_sm_url
from utils.requests import get_request


async def get_mesabbrev(article):
    url = f'{smcard_sm_url}{article}'
    data_request = await get_request(url)
    if 'data_text' in data_request:
        # print(data_request[1])
        dictionary = json.loads(data_request[1])
        print(dictionary)
        data_model = USIOMESABBREVINFO.DataModel(**dictionary)
        for js_data in data_model:
            mesabbrev = js_data[1].POSTOBJECT[0].IOUSIOMESABBREVINFO.USIOMESABBREVINFO[0].MESABBREV
            return mesabbrev


if __name__ == '__main__':
    data = asyncio.run(get_mesabbrev('000827'))
    print(data)
    pass
