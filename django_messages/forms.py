import datetime
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

from django_messages.models import Message
from django_messages.fields import CommaSeparatedUserField, CommaSeparatedUserInput

from django_messages.utils import get_user_model, get_username_field
User = get_user_model()

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=120)
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))

    
    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter

            
    def save(self, sender, parent_msg=None, extra_kwargs={}):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        for r in recipients:
            msg = Message(
                sender = sender,
                recipient = r,
                subject = subject,
                body = body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = datetime.datetime.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)
            if notification:
                if parent_msg is not None:
                    notification.send([sender], "messages_replied", {'message': msg,}, **extra_kwargs)
                    notification.send([r], "messages_reply_received", {'message': msg,}, **extra_kwargs)
                else:
                    notification.send([sender], "messages_sent", {'message': msg,}, **extra_kwargs)
                    notification.send([r], "messages_received", {'message': msg,}, **extra_kwargs)
        return message_list


import datetime
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

from django_messages.models import Message
from django_messages.fields import CommaSeparatedUserField

from django_messages.utils import get_user_model, get_username_field
User = get_user_model()

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=120)
    body = forms.CharField(label=_(u"Body"),
        widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))

    
    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter

            
    def save(self, sender, parent_msg=None, extra_kwargs={}):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []
        for r in recipients:
            msg = Message(
                sender = sender,
                recipient = r,
                subject = subject,
                body = body,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = datetime.datetime.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)
            if notification:
                if parent_msg is not None:
                    notification.send([sender], "messages_replied", {'message': msg,}, **extra_kwargs)
                    notification.send([r], "messages_reply_received", {'message': msg,}, **extra_kwargs)
                else:
                    notification.send([sender], "messages_sent", {'message': msg,}, **extra_kwargs)
                    notification.send([r], "messages_received", {'message': msg,}, **extra_kwargs)
        return message_list


class RecipientDisplayWidget(CommaSeparatedUserInput):
    input_type = 'hidden'
    is_hidden = False
    
    def __init__(self, *args, **kwargs):
        self.recipient_format = kwargs.pop("recipient_format", None)
        super(RecipientDisplayWidget, self).__init__(*args, **kwargs)
    
    def _format_display(self, display):
        if not isinstance(display, User):
            try:
                display = User.objects.get(**{'%s__iexact' % get_username_field(): display})
            except User.DoesNotExist:
                return ""
        if self.recipient_format:
            return self.recipient_format(display)
        return getattr(display, get_username_field())
    
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif isinstance(value, (list, tuple)):
            value = (', '.join([getattr(user, get_username_field()) for user in value]))
        output = super(RecipientDisplayWidget, self).render(name, value, attrs)
        display = value
        if display is None:
            display = ''
        elif isinstance(display, (list, tuple)):
            display = (', '.join([self._format_display(user) for user in display]))
        else:
            display = self._format_display(display)
        return mark_safe(u'<span>%s%s</span>' % (display, output))


class ComposeToForm(ComposeForm):
    def __init__(self, *args, **kwargs):
        recipient_format = kwargs.pop("recipient_format", None)
        self.recipients = kwargs.pop("recipients", None)
        super(ComposeToForm, self).__init__(*args, **kwargs)
        self.fields['recipient'].widget = RecipientDisplayWidget(recipient_format=recipient_format)
        self.fields['recipient'].initial = self.recipients

    def clean_recipient(self):
        data = self.cleaned_data.get('recipient')
        if not isinstance(data, (tuple, list)):
            data = [data]
        if [dd.pk for dd in data] == [rr.pk for rr in self.recipients]:
            return data
        raise forms.ValidationError("You cannot change the recipient for this message.")