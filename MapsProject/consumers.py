import logging
from channels import Group
from channels.sessions import channel_session

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    print("User connected")
    log.debug('User connected')
    Group('events').add(message.reply_channel)

@channel_session
def ws_receive(message):
    print("Message receive")
    log.debug('Message receive')
    Group('events').send({'data': 'Enviando un mensaje'})

@channel_session
def ws_disconnect(message):
    Group('events').discard(message.reply_channel)