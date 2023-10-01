from django.shortcuts import render, redirect
from django.views import View
from app.models import DJ


class DJsView(View):
    def get(self, request, lang):
        djs = DJ.objects.all()
        return render(request, f"djs.html", {f"djs": djs})
