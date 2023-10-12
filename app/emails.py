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


def send_new_booking_email(request, booking):
    language = booking.dj.user.settings.language.code
    # Load the content
    plaintext = get_template(f"emails/new-booking-request.txt")
    html = get_template(f"emails/new-booking-request.html")
    subject = tr("%s: New booking request", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    to = booking.dj.user.email
    url = request.build_absolute_uri(reverse(f"booking", kwargs={f"booking_id": booking.id}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, f"text/html")
    message.send()


def send_quote_email(request, booking):
    language = booking.language
    # Load the content
    plaintext = get_template(f"emails/booking-quote.txt")
    html = get_template(f"emails/booking-quote.html")
    subject = tr("%s: Quote received for booking request", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    to = booking.email
    url = request.build_absolute_uri(reverse(f"venue-booking", kwargs={f"code": booking.code}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, f"text/html")
    message.send()


def send_accepted_email(request, booking):
    language = booking.language
    # Load the content
    plaintext = get_template(f"emails/booking-accepted.txt")
    html = get_template(f"emails/booking-accepted.html")
    subject = tr("%s: Booking request accepted", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    to = booking.email
    url = request.build_absolute_uri(reverse(f"venue-booking", kwargs={f"code": booking.code}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, f"text/html")
    message.send()


def send_declined_email(request, booking):
    language = booking.language
    # Load the content
    plaintext = get_template(f"emails/booking-declined.txt")
    html = get_template(f"emails/booking-declined.html")
    subject = tr("%s: Booking request declined", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    to = booking.email
    url = request.build_absolute_uri(reverse(f"venue-booking", kwargs={f"code": booking.code}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, f"text/html")
    message.send()


def send_venue_declined_email(request, booking):
    language = booking.dj.user.settings.language.code
    # Load the content
    plaintext = get_template(f"emails/booking-venue-declined.txt")
    html = get_template(f"emails/booking-venue-declined.html")
    subject = tr("%s: Quote declined", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    to = booking.dj.user.email
    url = request.build_absolute_uri(reverse(f"booking", kwargs={f"booking_id": booking.id}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, f"text/html")
    message.send()


def send_paid_email(request, booking):
    language = booking.dj.user.settings.language.code
    # Load the content
    plaintext = get_template(f"emails/booking-paid.txt")
    html = get_template(f"emails/booking-paid.html")
    subject = tr("%s: Booking confirmed", language) % settings.SITE_TITLE
    from_email = f"no-reply@{request.get_host()}"
    to = booking.dj.user.email
    url = request.build_absolute_uri(reverse(f"booking", kwargs={f"booking_id": booking.id}))
    context = {f"language": language, f"url": url}
    text_content = plaintext.render(context)
    html_content = html.render(context)

    # Create the email message with the content and send it
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, f"text/html")
    message.send()
