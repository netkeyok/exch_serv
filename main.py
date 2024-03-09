from fastapi import FastAPI, File
from cm_datamining import parse_ui, parse_wi, parse_rl
import json

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
    else:
        print('---------------------------------------')
        print(docdict[0].keys())
        print('wrong data!!!')
        print(docdict)
