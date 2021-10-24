from django.template.loader import render_to_string
from django.core.signing import Signer
import config.settings as conf


signer = Signer()


def send_activation_notification(user):
    if conf.DEBUG:
        host = 'http://127.0.0.1:5000'
    else:
        host = 'https://' + 'djangogrammfoxminded.herokuapp.com'
    context = {'user': user, 'host': host,
               'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)
