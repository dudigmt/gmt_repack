from django.contrib import admin
from .models import ProductionLine, WorkOrder, WorkOrderAssignment, ProductionLog

@admin.register(ProductionLine)
class ProductionLineAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['work_order_number', 'product_code', 'product_name', 'quantity_ordered', 'status', 'planned_start_date', 'production_line']
    list_filter = ['status', 'production_line', 'created_at']
    search_fields = ['work_order_number', 'product_code', 'product_name']
    raw_id_fields = ['created_by']
    filter_horizontal = ['assigned_employees']
    date_hierarchy = 'planned_start_date'

@admin.register(WorkOrderAssignment)
class WorkOrderAssignmentAdmin(admin.ModelAdmin):
    list_display = ['work_order', 'employee', 'role', 'hours_worked', 'date_assigned']
    list_filter = ['date_assigned', 'role']
    search_fields = ['work_order__work_order_number', 'employee__user__username']

@admin.register(ProductionLog)
class ProductionLogAdmin(admin.ModelAdmin):
    list_display = ['work_order', 'timestamp', 'operator', 'output_quantity', 'scrap_quantity', 'downtime_minutes']
    list_filter = ['timestamp', 'operator']
    search_fields = ['work_order__work_order_number', 'notes']
    raw_id_fields = ['operator']
