from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is
    used as dashboard. Here you can for example prepare data for charts.
    """
    context.update({
        "custom_variable": "Hello World",
    })
    return context