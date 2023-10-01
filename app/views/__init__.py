from django.shortcuts import render, redirect
from django.views import View
from app.translation import translations
from app.views.sign_up import (
    SignUpView,
    SignUpSuccessView,
    SignUpVerifyView,
)
from app.views.log_in import (
    LogInView,
    LogOutView,
)
from app.views.admin import AdminLanguageView
from app.views.djs import DJsView


class RedirectToLanguageView(View):
    def get(self, request):
        for lang in translations:
            if lang in request.LANGUAGE_CODE:
                break
        else:
            lang = f"en"
        return redirect(f"index", lang=lang)


class ConceptView(View):
    def get(self, request, lang):
        return render(request, f"concept.html")


class AccountView(View):
    def get(self, request, lang):
        if not request.user.is_authenticated:
            return redirect(f"log-in", lang=lang)
        return render(request, f"account.html")
