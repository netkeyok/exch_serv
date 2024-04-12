from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
import json
from cm_datamining import parse_ui, parse_wi, parse_rl, parse_or
from api_requests.Send_to_CV import send_postuplenie, clear_postuplenie
from api_requests.Send_to_SM import send_wi
from api_requests.Get_from_SM import get_card


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
        doclist = parse_or(dictionary)
        for docid in doclist:
            await send_postuplenie(docid)
            print(docid)
        print('end receiving OR')
    else:
        print('---------------------------------------')
        print(docdict[0].keys())
        print('wrong data!!!')
        print(docdict)


@app.post("/v1/func")
async def clear_docs(swith):
    await clear_postuplenie(swith)
    return 'Ok'


@app.post("/v1/get_card")
async def get_SMcard(bar: str):
    result = get_card(bar)
    # Предполагаем, что result - это список кортежей
    data = [{"article": item[0], "name": item[1]} for item in result]
    return JSONResponse(content=data)

