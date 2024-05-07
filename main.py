from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
import json
from cm_datamining import parse_ui, parse_wi, parse_rl
from parsing.OR import parse_or
from api_requests.Send_to_CV import clear_postuplenie, send_articles
from db_connections.Get_from_SM import get_card

app = FastAPI()


@app.post("/v1/json_in/docs")
async def upload_data(file: bytes = File()):
    # преобразуем байты в строку
    string = file.decode("utf-8-sig")
    # преобразуем строку в словарь
    dictionary = json.loads(string)
    # передаем словарь в модель Pydantic
    docdict = dictionary['PACKAGE']['POSTOBJECT']
    if 'UI' in docdict[0].keys():
        print('start')
        parse_ui(dictionary)
        print('end')
    elif 'WI' in docdict[0].keys():
        print('start')
        parse_wi(dictionary)
        print('end')
    elif 'RL' in docdict[0].keys():
        print('start')
        parse_rl(dictionary)
        print('end')
    elif 'OR' in docdict[0].keys():
        print('start receiving OR')
        await parse_or(dictionary)
        print('end receiving OR')
    else:
        print('---------------------------------------')
        print(docdict[0].keys())
        print('wrong data!!!')
        print(docdict)


@app.post("/v1/func/clear")
async def clear_docs(days):
    await clear_postuplenie(days)
    return 'Ok'


@app.get("/v1/get_card")
async def get_SMcard(bar: str):
    result = get_card(bar)
    # Предполагаем, что result - это список кортежей

    return JSONResponse(content=result)


@app.post("/v1/func/send_sku")
async def send_sku():
    result = await send_articles()
    return result
