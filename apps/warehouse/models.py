from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    UNIT_CHOICES = (
        ('pcs', 'Pieces'),
        ('kg', 'Kilograms'),
        ('m', 'Meters'),
        ('l', 'Liters'),
        ('box', 'Box'),
        ('pallet', 'Pallet'),
    )

    code = models.CharField(max_length=50, unique=True, help_text="Product SKU or unique code")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pcs')
    
    # Pricing and costing (simplified)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Inventory control
    minimum_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    reorder_point = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_purchased = models.BooleanField(default=True)
    is_manufactured = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_products')

    class Meta:
        ordering = ['code']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.code} - {self.name}"

class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'

    def __str__(self):
        return self.name

class Stock(models.Model):
    """Current stock level of a product in a warehouse."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reserved_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Quantity allocated but not yet shipped")
    last_counted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'warehouse']
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return f"{self.product.code} @ {self.warehouse.code}: {self.quantity}"

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

class StockMovement(models.Model):
    MOVEMENT_TYPES = (
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
        ('return', 'Return'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, null=True, blank=True, related_name='outgoing_movements')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, null=True, blank=True, related_name='incoming_movements')
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    reference_number = models.CharField(max_length=50, blank=True, help_text="e.g., Work Order, Purchase Order, Sales Order")
    notes = models.TextField(blank=True)
    moved_at = models.DateTimeField(auto_now_add=True)
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_movements')

    class Meta:
        ordering = ['-moved_at']
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'

    def __str__(self):
        return f"{self.movement_type} - {self.product.code} - {self.quantity}"