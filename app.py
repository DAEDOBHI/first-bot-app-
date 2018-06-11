"""Librerías """
#referencia de la estructura de Messenger en facebook
#https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messages

import random #libreria para selecion random
from flask import Flask, request #libreria para el levantamiento del sitio en nuestro localhost
from pymessenger.bot import Bot #libreria para el bot

app = Flask(__name__)
"""Vartibles de los token de acceso"""
ACCESS_TOKEN= 'EAAe5tlgObXIBAPFvxAt3jZAx0aUxPqwL1RAC7VQ8dtA8qlHZAI2tnukHeh3k5CLLcYIKvghgTzPt7wgZAJ4aTEz3LNHR6cptCiYQQVGcabP9XTbOmR0KdpUt4vZCK7klUSTDAdecaNuBe3nHWIidtA2NC6FLU2ZCUEn0tVcBHk6NgJ9nWd9xY'

VERIFY_TOKEN = 'APP_VERIFY_TOKEN'


bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
#método en el que se recibiran los mensajos enviados desde facebook
def receive_message():
    if request.method == 'GET':
        """proceso de verificación del token proporcionado a Facebook"""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #Si la respuesat no es GET y en su lugar es POST seguimos con el proceso del retorno de nuestro mensaje
    else:
        # obtenemos el mensaje que el usuario mando al Bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                # obtenemos el ID de Facebook Messenger para poder retornar nuestra respuesta a ese mismo usuario
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    """Auto respuesta, el bot responderá lo mismo que escribio el usuario"""
                    self_response = message['message']['text'];#obtenemos el valor del arreglo y lo colocamos en una variable.
                    send_message(recipient_id, self_response)
                    """Respuesta programada, el bot respondera en forma random conforme al arreglo definido"""
                    #response_sent_text = get_message()
                    #send_message(recipient_id, response_sent_text)

                # En dado caso de que el suario envie alguna foto, video o GIF podremos tambien retornar nuestra respuesta
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #Tomamos el token enviado por Facebook y verificamos que coincida con el token de verificación que enviamos
    #si coinciden, se permite la solicitud,si no devuelvemos un error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#Esta función seleciona un mensaje aleatorio para enviar al usuario
def get_message():
    sample_responses = ['Hola, Como estás , Mi nombre es Daniel, mucho gusto !! ;) , Este es un bot con fines académicos Gracias por tu atención','Hola, Como estás , Mi nombre es Daniel, mucho gusto !! ;) , Este es un bot con fines académicos Gracias por tu atención','Hola, Como estás , Mi nombre es Daniel, mucho gusto !! ;) , Este es un bot con fines académicos Gracias por tu atención']
    # Devolvemos el elemento seleccionado al usuario
    return random.choice(sample_responses)

#Usamos PyMessenger para enviar una respuesta al usuario
def send_message(recipient_id, response):
    #Enviamos  al usuario el mensaje de texto proporcionado a través del parámetro de respuesta de entrada
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == '__main__':
    app.run(debug = True, port = 8000, host= '0.0.0.0')
