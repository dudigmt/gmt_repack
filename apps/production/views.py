from django.shortcuts import render
from .models import WorkOrder, ProductionLine, ProductionLog
from django.db.models import Sum, Count, Avg

def dashboard(request):
    # Dummy data / agregasi dari database
    total_work_orders = WorkOrder.objects.count()
    total_production_lines = ProductionLine.objects.count()
    total_logs = ProductionLog.objects.count()
    
    # Status work orders
    work_orders_by_status = WorkOrder.objects.values('status').annotate(count=Count('id'))
    
    # Total quantity produced vs ordered
    total_ordered = WorkOrder.objects.aggregate(total=Sum('quantity_ordered'))['total'] or 0
    total_produced = WorkOrder.objects.aggregate(total=Sum('quantity_produced'))['total'] or 0
    
    # Production per line
    production_by_line = ProductionLine.objects.annotate(
        wo_count=Count('work_orders'),
        total_produced=Sum('work_orders__quantity_produced')
    ).values('name', 'wo_count', 'total_produced')
    
    context = {
        'total_work_orders': total_work_orders,
        'total_production_lines': total_production_lines,
        'total_logs': total_logs,
        'work_orders_by_status': work_orders_by_status,
        'total_ordered': total_ordered,
        'total_produced': total_produced,
        'production_by_line': production_by_line,
    }
    return render(request, 'production/dashboard.html', context)