from django.urls import path
from app.views import (
    ChangeLanguageView,
    LogInView,
    SignUpView,
    SignUpSuccessView,
    SignUpVerifyView,
    LogOutView,
    ConceptView,
    AccountView,
    AdminLanguageView,
    DJsView,
    EditDJView,
    EditDJSuccessView,
    AdminEditDJView,
    AdminEditDJSuccessView,
    EditBankDetailsView,
    EditBankDetailsSuccessView,
    BookingInvoiceView,
    BookingView,
    BookingsView,
    AcceptBookingView,
    DeclineBookingView,
    VenueDeclineBookingView,
    QuoteBookingView,
    NewBookingView,
    VenueBookingView,
)

urlpatterns = [
    # Landing page
    path("", ConceptView.as_view(), name="index"),
    # Sign up, log in, reset password
    path("log-in<path:path>", LogInView.as_view(), name="log-in"),
    path("log-out", LogOutView.as_view(), name="log-out"),
    path("sign-up", SignUpView.as_view(), name="sign-up"),
    path("sign-up/success", SignUpSuccessView.as_view(), name="sign-up-success"),
    path("sign-up/verify/<code>", SignUpVerifyView.as_view(), name="sign-up-verify"),
    # Change language
    path("change-language/<language>", ChangeLanguageView.as_view(), name="change-language"),
    # Static Pages
    path("concept", ConceptView.as_view(), name="concept"),
    # Accounts
    path("account", AccountView.as_view(), name="account"),
    # Admin
    path("admin/language", AdminLanguageView.as_view(), name="admin-language"),
    # DJs
    path("djs", DJsView.as_view(), name="djs"),
    path("edit-dj", EditDJView.as_view(), name="edit-dj"),
    path("edit-dj/success", EditDJSuccessView.as_view(), name="edit-dj-success"),
    path("admin-edit-dj/<dj_id>", AdminEditDJView.as_view(), name="admin-edit-dj"),
    path("admin-edit-dj/<dj_id>/success", AdminEditDJSuccessView.as_view(), name="admin-edit-dj-success"),
    # Bank details
    path("edit-bank-details", EditBankDetailsView.as_view(), name="edit-bank-details"),
    path("edit-bank-details/success", EditBankDetailsSuccessView.as_view(), name="edit-bank-details-success"),
    # Bookings
    path("bookings", BookingsView.as_view(), name="bookings"),
    path("booking/<booking_id>", BookingView.as_view(), name="booking"),
    path("booking/<booking_id>/accept", AcceptBookingView.as_view(), name="accept-booking"),
    path("booking/<booking_id>/decline", DeclineBookingView.as_view(), name="decline-booking"),
    path("booking/<booking_id>/quote", QuoteBookingView.as_view(), name="quote-booking"),
    path("new-booking/<dj_id>", NewBookingView.as_view(), name="new-booking"),
    path("venue-booking/<code>", VenueBookingView.as_view(), name="venue-booking"),
    path("venue-booking/<code>/decline", VenueDeclineBookingView.as_view(), name="venue-decline-booking"),
    path("venue-booking/<code>/invoice", BookingInvoiceView.as_view(), name="booking-invoice"),
]
