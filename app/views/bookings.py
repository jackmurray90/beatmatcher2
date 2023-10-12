from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from django.urls import reverse
from app.models import Booking, DJ
from app.util import random_128_bit_string
from app import forms
from app.emails import send_new_booking_email, send_quote_email, send_accepted_email, send_declined_email, send_venue_declined_email, send_paid_email
from datetime import datetime, timezone, timedelta
from time import mktime
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_API_KEY


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
        booking.language = request.session[f"language"]
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
        booking.set_time = datetime.strptime(form.set_time, f"%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        booking.hours = int(form.hours)
        booking.equipment_information = form.equipment_information
        booking.other_information = form.other_information
        booking.extra_budget = int(form.extra_budget) if form.extra_budget else None
        booking.rate = dj.rate

        # Save the booking request
        booking.save()

        # Generate the email to the DJ about the new booking request.
        send_new_booking_email(request, booking)

        return redirect(f"venue-booking", code=booking.code)


class BookingsView(View):
    def get(self, request, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        bookings = Booking.objects.filter(dj__user=request.user).order_by("set_time")
        return render(request, f"bookings.html", {f"bookings": bookings})


class QuoteForm(forms.Form):
    __title__ = "Quote"
    quote = forms.IntegerField("Quote (in €)", positive=True)
    submit = forms.SubmitButton("Give a quote")


class BookingView(View):
    def get(self, request, booking_id, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking or booking.dj.user != request.user:
            return Http404
        return render(request, f"venue-booking.html", {f"booking": booking, f"is_dj": True})


class QuoteBookingView(View):
    def get(self, request, booking_id, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking or booking.dj.user != request.user or booking.stage != Booking.REQUESTED:
            return Http404
        quote_form = QuoteForm(request)
        return render(request, f"venue-booking.html", {f"booking": booking, f"quote_form": quote_form, f"is_dj": True})

    def post(self, request, booking_id, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking or booking.dj.user != request.user or booking.stage != Booking.REQUESTED:
            return Http404
        quote_form = QuoteForm(request)
        if not quote_form.is_valid:
            return render(request, f"venue-booking.html", {f"booking": booking, f"quote_form": quote_form, f"is_dj": True})
        booking.quote = int(quote_form.quote)
        booking.stage = Booking.QUOTE
        booking.save()
        send_quote_email(request, booking)
        return redirect(f"booking", booking_id=booking.id)


class AcceptBookingView(View):
    def post(self, request, booking_id, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking or booking.dj.user != request.user or booking.stage != Booking.REQUESTED:
            return Http404
        booking.stage = Booking.ACCEPTED
        booking.save()
        send_accepted_email(request, booking)
        return redirect(f"booking", booking_id=booking.id)


class DeclineBookingView(View):
    def post(self, request, booking_id, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        booking = Booking.objects.filter(id=booking_id).first()
        if not booking or booking.dj.user != request.user or booking.stage != Booking.REQUESTED:
            return Http404
        booking.stage = Booking.DECLINED
        booking.save()
        send_declined_email(request, booking)
        return redirect(f"booking", booking_id=booking.id)


class VenueDeclineBookingView(View):
    def post(self, request, code, tr):
        booking = Booking.objects.filter(code=code).first()
        if not booking or booking.stage != Booking.QUOTE:
            return Http404
        booking.stage = Booking.DECLINED
        booking.save()
        send_venue_declined_email(request, booking)
        return redirect(f"venue-booking", code=code)


class VenueBookingView(View):
    def get(self, request, code, tr):
        # Ensure Booking exists
        booking = Booking.objects.filter(code=code).first()
        if not booking:
            raise Http404
        if booking.stage in [Booking.ACCEPTED, Booking.QUOTE] and booking.checkout_session_id:
            checkout_session = stripe.checkout.Session.retrieve(booking.checkout_session_id)
            if checkout_session.payment_status == f"paid":
                booking.stage = Booking.PAID
                booking.save()
                send_paid_email(request, booking)
        return render(request, f"venue-booking.html", {f"booking": booking})


class BookingInvoiceView(View):
    def get(self, request, code, tr):
        # Ensure Booking exists
        booking = Booking.objects.filter(code=code).first()
        if not booking or booking.stage not in [Booking.ACCEPTED, Booking.QUOTE]:
            raise Http404
        if booking.stage == Booking.QUOTE:
            total = booking.quote * 100
        else:
            total = booking.rate * booking.hours * 100
        payment_fee = int(total * 0.035) + 19
        service_fee = int(total * 0.01)
        if booking.checkout_session_id:
            checkout_session = stripe.checkout.Session.retrieve(booking.checkout_session_id)
        else:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        f"price_data": {
                            f"currency": f"EUR",
                            f"product_data": {
                                f"name": booking.dj.name,
                            },
                            f"unit_amount": total,
                        },
                        f"quantity": 1,
                    },
                    {
                        f"price_data": {
                            f"currency": f"EUR",
                            f"product_data": {
                                f"name": tr("Service fee"),
                            },
                            f"unit_amount": service_fee,
                        },
                        f"quantity": 1,
                    },
                    {
                        f"price_data": {
                            f"currency": f"EUR",
                            f"product_data": {
                                f"name": tr("Payment processing fee"),
                            },
                            f"unit_amount": payment_fee,
                        },
                        f"quantity": 1,
                    },
                ],
                mode=f"payment",
                success_url=request.build_absolute_uri(reverse(f"venue-booking", kwargs={f"code": booking.code})),
                expires_at=mktime((booking.set_time + timedelta(days=1)).timetuple()),
            )
            booking.checkout_session_id = checkout_session.id
            booking.save()
        return redirect(checkout_session.url)
