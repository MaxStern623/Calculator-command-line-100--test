import json
import datetime
import logging
import os
import uuid
try:
    # prefer mongoengine when available/runtime not in test-mode
    from mongoengine import connect, Document, StringField, DateTimeField
except Exception:
    # mongoengine may be missing in some environments; we'll fallback when needed
    connect = None
import operations
from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse

from models import CalcGetRequest, CalcPostRequest, CalcResponce

# create FastAPI app
app = FastAPI()

# configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# connect to MongoDB unless tests request a mock DB
USE_MOCK = os.environ.get('USE_MOCK_DB', '')
if not USE_MOCK:
    try:
        # real mongodb credentials (tunable via env later)
        connect('mongodb_data_container', username='root',
                password='rootpassword', authentication_source='admin')
    except Exception as e:
        # if connection fails during import, continue and let runtime handlers
        # attempt to use DB on first operation (or tests can set USE_MOCK_DB)
        logger.warning('MongoDB connect failed at startup: %s', e)


# defining DB-schema: 1) math operation body, 2) math operation result, 3) date-time
if USE_MOCK:
    # simple in-memory mock used by tests to avoid external Mongo dependency
    class History:
        _store = []

        def __init__(self, operation=None, result=None, created_at=None):
            self.operation = operation
            self.result = result
            self.created_at = created_at or datetime.datetime.now()
            self.id = str(uuid.uuid4())

        def save(self):
            entry = {
                'operation': self.operation,
                'result': self.result,
                'created_at': self.created_at.isoformat(),
                '_id': self.id,
            }
            History._store.append(entry)
            class Saved:
                def __init__(self, id):
                    self.id = id

            return Saved(self.id)

        @classmethod
        def objects(cls):
            class QuerySet:
                def to_json(self):
                    return json.dumps([
                        {
                            'operation': e['operation'],
                            'result': e['result'],
                            'created_at': e['created_at'],
                            '_id': e['_id'],
                        }
                        for e in History._store
                    ])

            return QuerySet()

else:
    class History(Document):
        operation = StringField(max_length=50)
        result = StringField(max_length=50)
        # use callable default so timestamp is evaluated at save time
        created_at = DateTimeField(required=True, default=datetime.datetime.now)


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
    # evaluate expression safely
    result = operations.evaluate_expression(params['expression'])
    # normalize numeric formatting: turn 4.0 -> '4'
    def _fmt(v):
        try:
            if isinstance(v, float) and v.is_integer():
                return str(int(v))
        except Exception:
            pass
        return str(v)

    responce['result'] = _fmt(result)
    responce['operation'] = params['expression']
    saved_operation = History(operation=str(params['expression']), result=str(responce['result'])).save()
    responce['uid'] = str(saved_operation.id)
    return responce


# saving math operation to DB
@app.post('/calc', summary='Calc as post method', response_model=CalcResponce)
async def post_calc(body: CalcPostRequest):
    params = body.dict()
    responce = {'result': '', 'operation': '', 'uid': ''}
    op = params.get('operator')
    first = float(params.get('first'))
    last = float(params.get('last'))

    # perform calculation
    result = operations.calculate(first, last, op)
    # format result consistently with GET handler
    try:
        if isinstance(result, float) and result.is_integer():
            responce['result'] = str(int(result))
        else:
            responce['result'] = str(result)
    except Exception:
        responce['result'] = str(result)
    responce['operation'] = f"{params.get('first')}{op}{params.get('last')}"

    saved_operation = History(operation=str(responce['operation']), result=str(responce['result'])).save()
    responce['uid'] = str(saved_operation.id)
    return responce
