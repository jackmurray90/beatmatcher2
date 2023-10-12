from django.shortcuts import render, redirect
from django.views import View
from app.models import User, DJ
from app import forms
from PIL import Image
from io import BytesIO
from pathlib import Path


class DJsView(View):
    def get(self, request, tr):
        djs = DJ.objects.all()
        return render(request, f"djs.html", {f"djs": djs})


class EditDJForm(forms.Form):
    __title__ = "Edit DJ profile"
    name = forms.CharField("Stage name", DJ.name)
    description = forms.TextField("Description", required=False)
    picture = forms.FileField("Profile picture", "Change profile picture", "Must be square, at least 180x180 pixels, and file size must not exceed 20MB.", max_size=1024 * 1024 * 20, required=False)
    soundcloud_url = forms.CharField("SoundCloud URL", DJ.soundcloud_url, required=False)
    rate = forms.IntegerField("Rate (€ per hour)", positive=True)
    submit = forms.SubmitButton("Save")

    def validate(self, tr):
        if self.soundcloud_url and not self.soundcloud_url.startswith(f"https://soundcloud.com/"):
            self.add_error(f"soundcloud_url", tr("SoundCloud URL must start with https://soundcloud.com/"))
        if self.picture and self.picture.size < 1024 * 1024 * 20:
            image_bytes = self.picture.read()
            try:
                image = Image.open(BytesIO(image_bytes))
                width, height = image.size
                if width < 180 or height < 180:
                    self.add_error(f"picture", tr("Profile picture is not large enough. Must be at least 180x180 pixels."))
            except:
                self.add_error(f"picture", tr("Invalid picture"))


class EditDJView(View):
    def get(self, request, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        try:
            dj = request.user.dj
            form = EditDJForm(
                request,
                initial_values={
                    f"name": dj.name,
                    f"description": dj.description,
                    f"soundcloud_url": dj.soundcloud_url,
                    f"rate": dj.rate,
                },
            )
        except User.dj.RelatedObjectDoesNotExist:
            dj = DJ(user=request.user)
            form = EditDJForm(request)
        return render(request, f"edit-dj.html", {f"form": form, f"dj": dj})

    def post(self, request, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")

        try:
            dj = request.user.dj
        except User.dj.RelatedObjectDoesNotExist:
            dj = DJ(user=request.user, picture=False)

        form = EditDJForm(request)

        if not form.is_valid:
            return render(request, f"edit-dj.html", {f"form": form, f"dj": dj})

        dj.name = form.name
        dj.description = form.description
        if form.picture:
            dj.picture = True
        dj.soundcloud_url = form.soundcloud_url
        dj.rate = int(form.rate)

        # Save the DJ (error 500 if they already made one)
        dj.save()

        # Save the uploaded profile picture
        if form.picture:
            image = Image.open(form.picture)
            Path(f"static/images/djs").mkdir(parents=True, exist_ok=True)
            image.resize((180, 180)).save(f"static/images/djs/{dj.id}.png")

        return redirect(f"edit-dj-success")


class EditDJSuccessView(View):
    def get(self, request, tr):
        if not request.user.is_authenticated:
            return redirect(f"log-in")
        return render(request, f"edit-dj-success.html")


class AdminEditDJForm(forms.Form):
    __title__ = "Admin edit DJ profile"
    name = forms.CharField("Stage name", DJ.name)
    description = forms.TextField("Description", required=False)
    picture = forms.FileField("Profile picture", "Change profile picture", "Must be square, at least 180x180 pixels, and file size must not exceed 20MB.", max_size=1024 * 1024 * 20, required=False)
    soundcloud_url = forms.CharField("SoundCloud URL", DJ.soundcloud_url, required=False)
    booking_url = forms.CharField("Booking URL", DJ.booking_url, required=False)
    rate = forms.IntegerField("Rate (€ per hour)", positive=True, required=False)
    submit = forms.SubmitButton("Save")

    def validate(self, tr):
        if self.soundcloud_url and not self.soundcloud_url.startswith(f"https://soundcloud.com/"):
            self.add_error(f"soundcloud_url", tr("SoundCloud URL must start with https://soundcloud.com/"))
        if self.picture and self.picture.size < 1024 * 1024 * 20:
            image_bytes = self.picture.read()
            try:
                image = Image.open(BytesIO(image_bytes))
                width, height = image.size
                if width < 180 or height < 180:
                    self.add_error(f"picture", tr("Profile picture is not large enough. Must be at least 180x180 pixels."))
            except:
                self.add_error(f"picture", tr("Invalid picture"))


class AdminEditDJView(View):
    def get(self, request, dj_id, tr):
        if not request.user.is_staff:
            return redirect(f"log-in")
        if dj_id == f"new":
            dj = DJ()
            form = AdminEditDJForm(request)
        else:
            try:
                dj = DJ.objects.get(id=dj_id)
            except DJ.DoesNotExist:
                return Http404
            form = AdminEditDJForm(
                request,
                initial_values={
                    f"name": dj.name,
                    f"description": dj.description,
                    f"soundcloud_url": dj.soundcloud_url,
                    f"booking_url": dj.booking_url,
                    f"rate": dj.rate,
                },
            )
        return render(request, f"edit-dj.html", {f"form": form, f"dj": dj})

    def post(self, request, dj_id, tr):
        if not request.user.is_staff:
            return redirect(f"log-in")
        if dj_id == f"new":
            dj = DJ(picture=False)
        else:
            try:
                dj = DJ.objects.get(id=dj_id)
            except DJ.DoesNotExist:
                return Http404

        form = AdminEditDJForm(request)

        if not form.is_valid:
            return render(request, f"edit-dj.html", {f"form": form, f"dj": dj})

        dj.name = form.name
        dj.description = form.description
        if form.picture:
            dj.picture = True
        dj.soundcloud_url = form.soundcloud_url
        dj.booking_url = form.booking_url
        dj.rate = int(form.rate) if form.rate else None

        # Save the DJ (error 500 if they already made one)
        dj.save()

        # Save the uploaded profile picture
        if form.picture:
            image = Image.open(form.picture)
            Path(f"static/images/djs").mkdir(parents=True, exist_ok=True)
            image.resize((180, 180)).save(f"static/images/djs/{dj.id}.png")

        return redirect(f"admin-edit-dj-success", dj_id=dj.id)


class AdminEditDJSuccessView(View):
    def get(self, request, dj_id, tr):
        if not request.user.is_staff:
            return redirect(f"log-in")
        try:
            dj = DJ.objects.get(id=dj_id)
        except DJ.DoesNotExist:
            return Http404
        return render(request, f"admin-edit-dj-success.html", {f"dj": dj})
