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
    EditBankDetailsView,
    EditBankDetailsSuccessView,
)

urlpatterns = [
    # Landing page
    path("", DJsView.as_view(), name="index"),
    # Sign up, log in, reset password
    path("log-in", LogInView.as_view(), name="log-in"),
    path("log-out", LogOutView.as_view(), name="log-out"),
    path("sign-up", SignUpView.as_view(), name="sign-up"),
    path("sign-up/success", SignUpSuccessView.as_view(), name="sign-up-success"),
    path("sign-up/verify/<code>", SignUpVerifyView.as_view(), name="sign-up-verify"),
    # Change language
    path("change-language", ChangeLanguageView.as_view(), name="change-language"),
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
    # Bank details
    path("edit-bank-details", EditBankDetailsView.as_view(), name="edit-bank-details"),
    path("edit-bank-details/success", EditBankDetailsSuccessView.as_view(), name="edit-bank-details-success"),

]
