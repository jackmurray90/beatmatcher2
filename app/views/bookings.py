from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse
from app.models import Booking, DJ
from app.util import random_128_bit_string
from app import forms
from datetime import datetime


class NewBookingForm(forms.Form):
    __title__ = "New booking"
    # Contact details
    contact_name = forms.CharField("Contact full name", Booking.contact_name)
    phone_number = forms.CharField("Phone number", Booking.phone_number)
    email = forms.CharField("Email address", Booking.email)
    # Address
    address_line_1 = forms.CharField("Venue address line 1", Booking.address_line_1)
    address_line_2 = forms.CharField("Venue address line 2", Booking.address_line_2, required=False)
    city = forms.CharField("Venue city", Booking.city)
    state = forms.CharField("Venue state/province/region", Booking.state)
    post_code = forms.CharField("Venue ZIP/postal code", Booking.post_code)
    country = forms.CharField("Venue country", Booking.country)
    # Booking
    set_time = forms.DateTimeField("Set time")
    hours = forms.IntegerField("Set hours", positive=True)
    equipment_information = forms.TextField("Equipment information", placeholder="What equipment will be available at the venue? What is required for the DJ to bring?")
    other_information = forms.TextField("Any other information", required=False)
    extra_budget = forms.IntegerField("Extra budget (for flights, equipment, etc)", positive=True, required=False)
    submit = forms.SubmitButton("Make booking request")


class NewBookingView(View):
    def get(self, request, dj_id, tr):
        # Ensure DJ profile exists
        dj = DJ.objects.filter(id=dj_id).first()
        if not dj:
            raise Http404

        form = NewBookingForm(request)

        # Render the form
        return render(request, f"new-booking.html", {f"form": form, f"dj": dj})

    def post(self, request, dj_id, tr):
        # Ensure DJ profile exists
        dj = DJ.objects.filter(id=dj_id).first()
        if not dj:
            raise Http404

        form = NewBookingForm(request)

        if not form.is_valid:
            return render(request, f"new-booking.html", {f"form": form, f"dj": dj})

        # Set the fields from the request
        booking = Booking()
        booking.stage = Booking.REQUESTED
        booking.dj = dj
        booking.code = random_128_bit_string()
        # Contact details
        booking.contact_name = form.contact_name
        booking.phone_number = form.phone_number
        booking.email = form.email
        # Venue Address
        booking.address_line_1 = form.address_line_1
        booking.address_line_2 = form.address_line_2
        booking.city = form.city
        booking.state = form.state
        booking.post_code = form.post_code
        booking.country = form.country
        # Booking
        booking.set_time = datetime.strptime(form.set_time, f"%Y-%m-%d %H:%M")
        booking.hours = int(form.hours)
        booking.equipment_information = form.equipment_information
        booking.other_information = form.other_information
        booking.extra_budget = int(form.extra_budget) if form.extra_budget else None
        booking.rate = dj.rate

        # Save the booking request
        booking.save()

        # Generate the email to the DJ
        # lang = dj.user.settings.language.code
        # plaintext = get_template(f"new-booking-email-{lang}.txt")
        # html = get_template(f"new-booking-email-{lang}.html")
        # subject = tr("New booking on Beatmatcher")
        # from_email = f"no-reply@beatmatcher.org"
        # to = dj.user.email
        # text_content = plaintext.render({f"url": request.build_absolute_uri(reverse(f"booking", kwargs={f"booking_id": booking.id}))})
        # html_content = html.render({f"url": request.build_absolute_uri(reverse(f"booking", kwargs={f"booking_id": booking.id}))})

        # Create the email message with the content and send it
        # message = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # message.attach_alternative(html_content, f"text/html")
        # message.send()

        return redirect(f"venue-booking", code=booking.code)


class VenueBookingView(View):
    def get(self, request, code, tr):
        # Ensure Booking exists
        booking = Booking.objects.filter(code=code).first()
        if not booking:
            raise Http404
        return render(request, f"venue-booking.html", {f"booking": booking})
