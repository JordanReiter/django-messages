
import logging
import datetime
import sys
import email
import re

from django.core.management.base import BaseCommand
from django.conf import settings
from django_messages.models import Message

try:
    from notification import models as notification
except ImportError:
    notification = None
    
SUBJECT_HEADER_ID_REGEX = getattr(settings,'MESSAGES_SUBJECT_HEADER_REGEX', r'^.+?\[([0-9a-z]+)\]\s*$')

class Command(BaseCommand):
    help = "Process an incoming message."
    
    def send_reply(self, parent_msg, body):
        message_list = []
        recipient = parent_msg.sender
        sender = parent_msg.recipient
        subject = "re: %s" % re.sub(r"^(re:\s*)+","",parent_msg.subject)
        msg = Message(
            sender = sender,
            recipient = recipient,
            subject = subject,
            body = body,
        )
        msg.parent_msg = parent_msg
        parent_msg.replied_at = datetime.datetime.now()
        parent_msg.save()
        msg.save()
        message_list.append(msg)
        if notification:
            if parent_msg is not None:
                notification.send([sender], "messages_replied", {'message': msg,})
                notification.send([recipient], "messages_reply_received", {'message': msg,}, from_address=settings.MESSAGES_HANDLER_ADDRESS)
            else:
                notification.send([sender], "messages_sent", {'message': msg,})
                notification.send([recipient], "messages_received", {'message': msg,}, from_address=settings.MESSAGES_HANDLER_ADDRESS)
        return message_list

    def get_message(self, msg):
        maintype = msg.get_content_maintype()
        if maintype == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_pay_load()
        elif maintype == 'text':
            return msg.get_payload()
    
    def handle(self, **options):
        msg = email.message_from_file(sys.stdin)
        if not len(msg.values()):
            raise ValueError("E-mail was empty.")
        content = self.get_message(msg)
        if not len(content):
            raise ValueError("Message was empty.")
        try:
            subject = re.sub(r'\s+',' ',msg['Subject'])
        except KeyError:
            raise ValueError("The email message did not have a valid header (Subject line required).")
        try:
            message_id = re.findall(SUBJECT_HEADER_ID_REGEX,subject.strip())[0]
        except IndexError:
            raise ValueError("The email message did not have a valid subject (id at the end omitted): %s." % subject)
        parent_msg = Message.objects.get_for_key(message_id)
        self.send_reply(parent_msg, content)
        
        