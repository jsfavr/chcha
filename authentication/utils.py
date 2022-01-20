from django.core.mail import EmailMessage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string,get_template
from django.utils.html import strip_tags
from rest_framework.response import Response

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

    def email_send(data):
        try:
            to=data['to_email']
            html_content = render_to_string('email.html',{'title':data['title'],'content':data['content']})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                #subject
                data['email_subject'],
                #content
                text_content,
                data['from_email'],
                [to]
            )
            email.attach_alternative(html_content,'text/html')
            email.send()
        except:
            return  True
       
