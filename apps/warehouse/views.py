from django.shortcuts import render
from .models import Product, ProductCategory, Warehouse, Stock, StockMovement
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, Value
from django.db.models.functions import Coalesce

def dashboard(request):
    total_products = Product.objects.count()
    total_categories = ProductCategory.objects.count()
    total_warehouses = Warehouse.objects.count()
    
    # Stock value dengan ExpressionWrapper
    total_stock_value = Stock.objects.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__cost_price'),
                output_field=DecimalField(max_digits=15, decimal_places=2)
            )
        )
    )['total'] or 0
    
    low_stock_products = Product.objects.filter(
        stocks__quantity__lte=F('minimum_stock')
    ).distinct().count()
    
    recent_movements = StockMovement.objects.select_related(
        'product', 'from_warehouse', 'to_warehouse', 'moved_by'
    ).order_by('-moved_at')[:5]
    
    # Stock by warehouse
    stock_by_warehouse = Warehouse.objects.annotate(
        total_items=Coalesce(
            Sum(
                ExpressionWrapper(
                    F('stocks__quantity'),
                    output_field=DecimalField(max_digits=15, decimal_places=2)
                )
            ), 
            Value(0, output_field=DecimalField(max_digits=15, decimal_places=2))
        ),
        total_products=Count('stocks')
    ).values('name', 'total_items', 'total_products')
    
    products_by_category = ProductCategory.objects.annotate(
        product_count=Count('products')
    ).values('name', 'product_count')
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_warehouses': total_warehouses,
        'total_stock_value': total_stock_value,
        'low_stock_products': low_stock_products,
        'recent_movements': recent_movements,
        'stock_by_warehouse': stock_by_warehouse,
        'products_by_category': products_by_category,
    }
    return render(request, 'warehouse/dashboard.html', context)