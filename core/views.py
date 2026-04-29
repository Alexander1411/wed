from django.shortcuts import render

from .forms import RSVPForm
from .models import RSVPResponse

def home(request):
    success = False
    form = RSVPForm()
    selected_attendance = ""
    selected_drinks = []
    full_name_value = ""

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
            form = RSVPForm()
            success = True
            selected_attendance = ""
            selected_drinks = []
            full_name_value = ""

    return render(
        request,
        "core/home.html",
        {
            "rsvp_form": form,
            "rsvp_success": success,
            "selected_attendance": selected_attendance,
            "selected_drinks": selected_drinks,
            "full_name_value": full_name_value,
        },
    )
