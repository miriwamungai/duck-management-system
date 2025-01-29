from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db.models import Prefetch, Subquery, OuterRef
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json

from .models import Veterinary
from django.shortcuts import render




class EntryView(View):
    """
    Renders all initial entries
    """
    def get(self, request):
        veterinary = Veterinary.objects.all()
        return render(request, 'veterinary/veterinary.html', {'veterinary': veterinary})