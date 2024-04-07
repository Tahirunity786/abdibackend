from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Beds
from django.db.models import Q


@login_required(login_url="/hospitrack/user/login")
def index(request):
    beds = Beds.objects.filter(Q(reservation__isnull=True) | Q(reservation__status="Decline"))
    data = {
        "beds":beds
    }
    return render(request, 'index.html', data)