from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from app.translation import tr


def send_sign_up_email(request, language, email, code):
    # Load the content
    plaintext = get_template(f"emails/sign-up.txt")
    html = get_template(f"emails/sign-up.html")
    subject = tr("Welcome to %s", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    url = request.build_absolute_uri(reverse(f"sign-up-verify", kwargs={f"code": code}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [email])
    message.attach_alternative(html_content, f"text/html")
    message.send()


def send_new_booking_email(request, dj, booking_id):
    language = dj.user.settings.language.code
    # Load the content
    plaintext = get_template(f"emails/new-booking-request.txt")
    html = get_template(f"emails/new-booking-request.html")
    subject = tr("%s: New booking request", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    to = dj.user.email
    url = request.build_absolute_uri(reverse(f"booking", kwargs={f"booking_id": booking_id}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, f"text/html")
    message.send()
