"""Unit tests for Supplier Service."""

import pytest
from backend.services.supplier_service import SupplierService


class TestSupplierService:
    """Test cases for SupplierService."""

    @pytest.fixture
    def service(self):
        """Create supplier service instance."""
        return SupplierService()

    @pytest.mark.asyncio
    async def test_get_supplier(self, service):
        """Test getting supplier details."""
        supplier = await service.get_supplier("SUP-001")
        
        assert supplier is not None
        assert supplier["supplier_id"] == "SUP-001"
        assert "name" in supplier
        assert "rating" in supplier
        assert "shipping_time_days" in supplier

    @pytest.mark.asyncio
    async def test_get_supplier_not_found(self, service):
        """Test getting non-existent supplier."""
        supplier = await service.get_supplier("INVALID-ID")
        assert supplier is None

    @pytest.mark.asyncio
    async def test_get_suppliers_by_category(self, service):
        """Test getting suppliers by category."""
        suppliers = await service.get_suppliers_by_category("Electronics")
        
        assert len(suppliers) > 0
        assert all(sup["supplier_id"] for s in suppliers for sup in [s])

    @pytest.mark.asyncio
    async def test_get_supplier_product(self, service):
        """Test getting supplier product."""
        product = await service.get_supplier_product("PROD-001")
        
        assert product is not None
        assert product["product_id"] == "PROD-001"
        assert "supplier_id" in product
        assert "cost_price" in product
        assert "stock_quantity" in product

    @pytest.mark.asyncio
    async def test_get_supplier_product_not_found(self, service):
        """Test getting non-existent product."""
        product = await service.get_supplier_product("INVALID-ID")
        assert product is None

    @pytest.mark.asyncio
    async def test_check_stock_available(self, service):
        """Test stock check when available."""
        result = await service.check_stock("PROD-001", quantity=10)
        
        assert result["available"] == True
        assert result["product_id"] == "PROD-001"
        assert result["requested_quantity"] == 10

    @pytest.mark.asyncio
    async def test_check_stock_unavailable(self, service):
        """Test stock check when unavailable."""
        result = await service.check_stock("PROD-001", quantity=10000)
        
        assert result["available"] == False
        assert "estimated_restock_date" in result

    @pytest.mark.asyncio
    async def test_place_order_success(self, service):
        """Test successful order placement."""
        result = await service.place_order(
            product_id="PROD-001",
            quantity=5,
            shipping_address="Test Address"
        )
        
        assert result["success"] == True
        assert "order_id" in result
        assert result["product_id"] == "PROD-001"
        assert result["quantity"] == 5
        assert "tracking_number" in result
        assert "estimated_delivery" in result

    @pytest.mark.asyncio
    async def test_place_order_insufficient_stock(self, service):
        """Test order with insufficient stock."""
        result = await service.place_order(
            product_id="PROD-001",
            quantity=10000
        )
        
        assert result["success"] == False
        assert "Insufficient stock" in result["message"]

    @pytest.mark.asyncio
    async def test_place_order_product_not_found(self, service):
        """Test order with non-existent product."""
        result = await service.place_order(
            product_id="INVALID-ID",
            quantity=5
        )
        
        assert result["success"] == False

    @pytest.mark.asyncio
    async def test_get_supplier_performance(self, service):
        """Test supplier performance metrics."""
        performance = await service.get_supplier_performance("SUP-001")
        
        assert "supplier_id" in performance
        assert "rating" in performance
        assert "on_time_delivery_rate" in performance
        assert "quality_score" in performance

    @pytest.mark.asyncio
    async def test_get_supplier_performance_not_found(self, service):
        """Test performance for non-existent supplier."""
        performance = await service.get_supplier_performance("INVALID-ID")
        assert "error" in performance

    def test_list_all_products(self, service):
        """Test listing all products."""
        products = service.list_all_products()
        
        assert len(products) > 0
        for product in products:
            assert "product_id" in product
            assert "supplier_id" in product
            assert "cost_price" in product
            assert "stock_quantity" in product

    @pytest.mark.asyncio
    async def test_supplier_data_consistency(self, service):
        """Test that supplier data is consistent."""
        supplier = await service.get_supplier("SUP-001")
        products = service.list_all_products()
        
        sup_products = [p for p in products if p["supplier_id"] == "SUP-001"]
        
        assert len(sup_products) > 0

    @pytest.mark.asyncio
    async def test_order_reduces_stock(self, service):
        """Test that placing order reduces stock."""
        product_before = await service.get_supplier_product("PROD-001")
        stock_before = product_before["stock_quantity"]
        
        await service.place_order(product_id="PROD-001", quantity=10)
        
        product_after = await service.get_supplier_product("PROD-001")
        stock_after = product_after["stock_quantity"]
        
        assert stock_after == stock_before - 10

    def test_supplier_categories(self, service):
        """Test that suppliers have categories."""
        suppliers = list(service.suppliers.values())
        
        assert all(hasattr(s, "categories") for s in suppliers)
        assert all(len(s.categories) > 0 for s in suppliers)
