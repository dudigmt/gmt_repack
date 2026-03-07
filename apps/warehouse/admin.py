from django.contrib import admin
from .models import ProductCategory, Product, Warehouse, Stock, StockMovement

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'parent', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'unit', 'cost_price', 'selling_price', 'is_active']
    list_filter = ['category', 'unit', 'is_active', 'is_manufactured']
    search_fields = ['code', 'name']
    raw_id_fields = ['created_by']

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'location', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'reserved_quantity', 'available_quantity', 'last_counted_at']
    list_filter = ['warehouse']
    search_fields = ['product__code', 'product__name']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'from_warehouse', 'to_warehouse', 'reference_number', 'moved_at', 'moved_by']
    list_filter = ['movement_type', 'from_warehouse', 'to_warehouse', 'moved_at']
    search_fields = ['product__code', 'reference_number', 'notes']
    raw_id_fields = ['product', 'moved_by']
    date_hierarchy = 'moved_at'
