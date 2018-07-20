import os
C = dict(

marioUserDict={
'Ru':
    {'code': 'r'}
     ,
'Nelg':
    {'code': 'n'}
    ,
'Tris':
    {'code': 't'}
}
)
#not openly on DB configs
X = dict(
botVersion='1.5.10',
mongoDEV=os.environ.get('BASE_MONGO_DB'),
LOG_DEBUG=True,
LOGS_TO_DB=True
)
