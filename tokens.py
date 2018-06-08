from peewee import *
db = SqliteDatabase('tokens.db')
"""Elementos del modelo para la creación de la base de datos Tokens.db"""
class Token(Model):
    service = CharField(max_length=250,unique=True)
    token = CharField(max_length=700,unique=True)

    class Meta:
        database = db
#arreglo para ingreso de datos
tokens = [
    {'service' : 'facebook', 'token' : 'EAAe5tlgObXIBAPFvxAt3jZAx0aUxPqwL1RAC7VQ8dtA8qlHZAI2tnukHeh3k5CLLcYIKvghgTzPt7wgZAJ4aTEz3LNHR6cptCiYQQVGcabP9XTbOmR0KdpUt4vZCK7klUSTDAdecaNuBe3nHWIidtA2NC6FLU2ZCUEn0tVcBHk6NgJ9nWd9xY'},
    {'service' : 'my_server', 'token' : 'APP_VERIFY_TOKEN'},
]
#funcion para agregar registros
def add_tokens():
    for token in tokens:
        try:
            Token.create(service = token['service'], token = token['token'])
        """Proceso de exception para actualizar los Tokens sin que marque error"""
        except IntegrityError:
            token_record = Token.get(service = token['service'])
            token_record.token = token['token']
            token_record.save()

if __name__ == '__main__':
    db.connect()#llamado a la conexion a la base de datos
    db.create_tables([Token],safe = True) # llamado a lafuncion para crear las tablas
    add_tokens()#llamado a la funcion para agregar los registros
