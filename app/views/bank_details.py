from django.shortcuts import render, redirect
from django.views import View
from app.models import User, BankDetails
from app import forms


class EditEuropeanBankDetailsForm(forms.Form):
    region = forms.HiddenField(BankDetails.region)
    account_holder = forms.CharField("Full name of the account holder", BankDetails.account_holder)
    account_number = forms.CharField("IBAN", BankDetails.account_number)
    submit = forms.SubmitButton("Save")


class EditAustralianBankDetailsForm(forms.Form):
    region = forms.HiddenField(BankDetails.region)
    account_holder = forms.CharField("Full name of the account holder", BankDetails.account_holder)
    bsb = forms.CharField("BSB", BankDetails.bsb)
    account_number = forms.CharField("Account number", BankDetails.account_number)
    submit = forms.SubmitButton("Save")


class EditUSBankDetailsForm(forms.Form):
    region = forms.HiddenField(BankDetails.region)
    account_holder = forms.CharField("Full name of the account holder", BankDetails.account_holder)
    ach = forms.CharField("ACH routing number", BankDetails.ach)
    account_number = forms.CharField("Account number", BankDetails.account_number)
    account_type = forms.SelectField("Account type", BankDetails.account_type)
    submit = forms.SubmitButton("Save")


class EditBankDetailsView(View):
    def get(self, request, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        try:
            bank_details = request.user.bankdetails
        except User.bankdetails.RelatedObjectDoesNotExist:
            bank_details = BankDetails(user=request.user)

        if bank_details.region == f"us":
            us_form = EditUSBankDetailsForm(
                request,
                initial_values={
                    f"region": f"us",
                    f"account_holder": bank_details.account_holder,
                    f"ach": bank_details.ach,
                    f"account_number": bank_details.account_number,
                    f"account_type": bank_details.account_type,
                },
            )
        else:
            us_form = EditUSBankDetailsForm(request, initial_values={f"region": f"us"})

        if bank_details.region == f"australia":
            australia_form = EditAustralianBankDetailsForm(
                request, initial_values={f"region": f"australia", f"account_holder": bank_details.account_holder, f"bsb": bank_details.bsb, f"account_number": bank_details.account_number}
            )
        else:
            australia_form = EditAustralianBankDetailsForm(request, initial_values={f"region": f"australia"})

        if bank_details.region == f"europe":
            europe_form = EditEuropeanBankDetailsForm(request, initial_values={f"region": f"europe", f"account_holder": bank_details.account_holder, f"account_number": bank_details.account_number})
        else:
            europe_form = EditEuropeanBankDetailsForm(request, initial_values={f"region": f"europe"})

        return render(request, f"edit-bank-details.html", {f"us_form": us_form, f"australia_form": australia_form, f"europe_form": europe_form, f"region": bank_details.region or f"europe"})

    def post(self, request, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")

        region = request.POST[f"region"]
        us_form = EditUSBankDetailsForm(request, initial_values={f"region": f"us"}, ignore_post=(region != f"us"))
        australia_form = EditAustralianBankDetailsForm(request, initial_values={f"region": f"australia"}, ignore_post=(region != f"australia"))
        europe_form = EditEuropeanBankDetailsForm(request, initial_values={f"region": f"europe"}, ignore_post=(region != f"europe"))
        if region == f"us":
            form = us_form
        if region == f"australia":
            form = australia_form
        if region == f"europe":
            form = europe_form

        if not form.is_valid:
            return render(request, f"edit-bank-details.html", {f"us_form": us_form, f"australia_form": australia_form, f"europe_form": europe_form, f"region": region})

        try:
            bank_details = request.user.bankdetails
        except User.bankdetails.RelatedObjectDoesNotExist:
            bank_details = BankDetails(user=request.user)

        bank_details.region = form.region
        bank_details.account_holder = form.account_holder
        bank_details.bsb = form.bsb if region == f"australia" else None
        bank_details.ach = form.ach if region == f"us" else None
        bank_details.account_type = form.account_type if region == f"us" else None
        bank_details.account_number = form.account_number

        bank_details.save()

        return redirect(f"edit-bank-details-success")


class EditBankDetailsSuccessView(View):
    def get(self, request, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        return render(request, f"edit-bank-details-success.html")
