from fastapi import FastAPI, File
from fastapi.responses import JSONResponse
import json
from cm_datamining import parse_ui, parse_wi, parse_rl
from api_requests.send_to_cv import send_or_to_cv, clear_old_docs
from db_connections.get_from_sm import get_card
from tasks.tasks import start_send_articles, task_clear_old_doc_tables

app = FastAPI()


@app.post("/v1/json_in/docs")
async def upload_data(file: bytes = File()):
    # преобразуем байты в строку
    string = file.decode("utf-8-sig")
    # преобразуем строку в словарь
    dictionary = json.loads(string)
    # передаем словарь в модель Pydantic
    docdict = dictionary["PACKAGE"]["POSTOBJECT"]
    if "UI" in docdict[0].keys():
        print("start")
        parse_ui(dictionary)
        print("end")
    elif "WI" in docdict[0].keys():
        print("start")
        parse_wi(dictionary)
        print("end")
    elif "RL" in docdict[0].keys():
        print("start")
        parse_rl(dictionary)
        print("end")
    elif "OR" in docdict[0].keys():
        print("start receiving OR")
        # print(dictionary)
        doc_list = await send_or_to_cv(dictionary)

        print(f"end receiving OR, sended {doc_list}")
    else:
        print("---------------------------------------")
        # print(docdict[0].keys())
        print("wrong data!!!")
        print(docdict)


@app.post("/v1/func/clear")
async def clear_docs(days: int):
    answer = await clear_old_docs(days)
    return answer


@app.get("/v1/get_card")
async def get_sm_card(bar: str):
    result = get_card(bar)
    # Предполагаем, что result - это список кортежей

    return JSONResponse(content=result)


@app.post("/v1/func/send_sku")
async def send_sku():
    # Отправляем задачу в очередь на выполнение через Celery, не ожидаем ее завершения
    task = start_send_articles.delay()
    # Возвращаем идентификатор задачи клиенту
    return {"task_id": task.id}


@app.post("/v1/func/clear_table_doc")
async def send_sku():
    # Отправляем задачу в очередь на выполнение через Celery, не ожидаем ее завершения
    task = task_clear_old_doc_tables.delay()
    # Возвращаем идентификатор задачи клиенту
    return {"task_id": task.id}


@app.get("/v1/func/task_status/{task_id}")
async def get_task_status(task_id: str):
    # Получаем статус задачи по ее ID
    task_result = start_send_articles.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }
