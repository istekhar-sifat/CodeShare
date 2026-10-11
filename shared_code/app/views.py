from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import SharedCode
import re

def home_page(request):
    return render(request, 'app/home.html')


def create_text(request):
    error = None
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        pin = request.POST.get('pin', '').strip()

        if not text:
            error = "Text cannot be empty"
        elif not pin:
            error = "PIN is required"
        elif not re.match(r'^\d{4}$', pin):
            error = "PIN must be exactly 4 digits"
        else:
            existing = SharedCode.objects.filter(pin=pin).first()
            if existing:
                if existing.is_expired():
                    existing.delete()
                else:
                    error = "This PIN is already used. Please choose a different one."

            if not error:
                SharedCode.objects.create(text=text, pin=pin)
                return redirect('text_detail', pin=pin)

    return render(request, 'app/create.html', {'error': error})


def get_text(request):
    text_obj = None
    pin = request.GET.get('pin', '').strip()
    error = None

    if pin:
        if not re.match(r'^\d{4}$', pin):
            error = "PIN must be 4 digits"
        else:
            text_obj = SharedCode.objects.filter(pin=pin).first()
            if text_obj:
                if text_obj.is_expired():
                    text_obj.delete()
                    text_obj = None
                    error = "This code has expired (older than 24 hours)"
            else:
                error = "No code found with this PIN"

    return render(request, 'app/get_text.html', {
        'text_obj': text_obj,
        'pin': pin,
        'error': error
    })


def text_detail(request, pin):
    text_obj = SharedCode.objects.filter(pin=pin).first()

    if not text_obj or text_obj.is_expired():
        if text_obj:
            text_obj.delete()
        return render(request, 'app/expired.html')

    return render(request, 'app/text_detail.html', {
        'text_obj': text_obj
    })