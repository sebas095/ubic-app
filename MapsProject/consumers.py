import logging
import json
from channels import Group
from channels.sessions import channel_session

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    log.info('websocket_connect. message = %s', message)
    Group('notifications').add(message.reply_channel)
    # Group('notifications').send({'text': 'Hola a todos'})

@channel_session
def ws_receive(message):
    log.info('send a message = %s', message.content)
    content = json.loads(message.content.get("text"))
    data = {
        'event_date': content['event_date'],
        'description': content['description'],
        'type': content['type'],
        'routes': content['routes'],
        'created_by': content['created_by'],
        'to': 'sebas.duque'
    }
    Group('notifications').send({'text': json.dumps(data)})
    message.reply_channel.send({'text': json.dumps(data)})

@channel_session
def ws_disconnect(message):
    log.info('websocket_disconnect. message = %s', message)
    Group('notifications').discard(message.reply_channel)