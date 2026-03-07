from django.db import models
from django.contrib.auth.models import User

class ProductionLine(models.Model):
    """Represents a production line or machine."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Production Line'
        verbose_name_plural = 'Production Lines'

    def __str__(self):
        return self.name

class WorkOrder(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('released', 'Released'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    )

    work_order_number = models.CharField(max_length=50, unique=True, help_text="Unique work order identifier")
    # Reference to product (will be defined in warehouse app)
    product_code = models.CharField(max_length=50, help_text="Product code from warehouse")
    product_name = models.CharField(max_length=200, blank=True, help_text="Denormalized product name for performance")
    quantity_ordered = models.DecimalField(max_digits=12, decimal_places=2)
    quantity_produced = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Dates
    planned_start_date = models.DateField(null=True, blank=True)
    planned_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    
    # Relationships
    production_line = models.ForeignKey(ProductionLine, on_delete=models.PROTECT, related_name='work_orders', null=True, blank=True)
    assigned_employees = models.ManyToManyField('hr.Employee', through='WorkOrderAssignment', blank=True, related_name='work_orders')
    
    # Metadata
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_work_orders')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'

    def __str__(self):
        return f"{self.work_order_number} - {self.product_name or self.product_code}"

class WorkOrderAssignment(models.Model):
    """Through model for assigning employees to work orders with roles and time."""
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    employee = models.ForeignKey('hr.Employee', on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True, help_text="e.g., Operator, Supervisor")
    hours_worked = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    date_assigned = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['work_order', 'employee']

    def __str__(self):
        return f"{self.work_order} - {self.employee}"

class ProductionLog(models.Model):
    """Records production output and events during a work order."""
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey('hr.Employee', on_delete=models.SET_NULL, null=True, related_name='production_logs')
    output_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    scrap_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    downtime_minutes = models.PositiveIntegerField(default=0, help_text="Downtime in minutes")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Production Log'
        verbose_name_plural = 'Production Logs'

    def __str__(self):
        return f"Log for {self.work_order} at {self.timestamp}"
