from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RSVPForm
from .models import RSVPResponse


def home(request):
    if request.method == "POST":
        form = RSVPForm(request.POST)
        selected_attendance = request.POST.get("attendance", "")
        selected_drinks = request.POST.getlist("drinks")
        full_name_value = request.POST.get("full_name", "")
        if form.is_valid():
            RSVPResponse.objects.create(
                attendance=form.cleaned_data["attendance"],
                full_name=form.cleaned_data["full_name"],
                drinks=form.cleaned_data["drinks"],
            )
            # GET after POST so refresh does not resubmit (no "Confirm Form Resubmission").
            return redirect(f"{reverse('home')}?thanks=1")

        return render(
            request,
            "core/home.html",
            {
                "rsvp_form": form,
                "rsvp_success": False,
                "selected_attendance": selected_attendance,
                "selected_drinks": selected_drinks,
                "full_name_value": full_name_value,
            },
        )

    success = request.GET.get("thanks") == "1"
    return render(
        request,
        "core/home.html",
        {
            "rsvp_form": RSVPForm(),
            "rsvp_success": success,
            "selected_attendance": "",
            "selected_drinks": [],
            "full_name_value": "",
        },
    )
