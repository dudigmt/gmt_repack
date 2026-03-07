from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def dashboard_callback(request, context):
    return context

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')