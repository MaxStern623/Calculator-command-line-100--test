import json
import datetime
from mongoengine import *
import mongoengine_goodjson as gj
from urllib.parse import unquote
from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from models import CalcGetRequest, CalcPostRequest, CalcResponce


# init FastAPI app
app = FastAPI()


# connecting to DB into Docker container
connect('mongodb_data_container', username='root',
        password='rootpassword', authentication_source='admin')


# defining DB-schema: 1) math operation body, 2) math operation result, 3) date-time
class History(gj.Document):
    operation = StringField(max_length=50)
    result = StringField(max_length=50)
    created_at = DateTimeField(
        required=True, default=str(datetime.datetime.now()))


# defining exceptional JSON-response for incorrect DB queries
@app.exception_handler(Exception)
async def error_handler(request, exc):
    return JSONResponse({
        'detail': f'{exc}'
    })


# showing history of math operations
@app.get('/history', summary='Get history of operations')
async def get_history():
    historyItems = History.objects()
    return {'responce': json.loads(historyItems.to_json())}


# showing math operation and a result
@app.get('/calc', summary='Calc as get method', response_model=CalcResponce)
async def get_calc(query: CalcGetRequest = Depends(CalcGetRequest)):
    params = query.dict()
    responce = {'result': '', 'operation': '', 'uid': ''}
    responce['result'] = eval(params['expression'])
    responce['operation'] = params['expression']
    saved_operation = History(operation=str(params['expression']), result=str(responce['result'])).save()
    responce['uid'] = str(saved_operation.id)
    return responce


# saving math operation to DB
@app.post('/calc', summary='Calc as post method', response_model=CalcResponce)
async def post_calc(body: CalcPostRequest):
    params = body.dict()
    responce = {'result': '', 'operation': '', 'uid': ''}

    if params['operator'] == '*':
        responce['result'] = params['first'] * params['last']
        responce['operation'] = str(
            params['first']) + '*' + str(params['last'])

    elif params['operator'] == '/':
        responce['result'] = params['first'] / params['last']
        responce['operation'] = str(
            params['first']) + '/' + str(params['last'])

    elif params['operator'] == '+':
        responce['result'] = params['first'] + params['last']
        responce['operation'] = str(
            params['first']) + '+' + str(params['last'])

    elif params['operator'] == '-':
        responce['result'] = params['first'] - params['last']
        responce['operation'] = str(
            params['first']) + '-' + str(params['last'])

    saved_operation = History(operation=str(
        responce['operation']), result=str(responce['result'])).save()
    responce['uid'] = str(saved_operation.id)

    return responce
