"""Unit tests for Store Service."""

import pytest
from backend.services.store_service import StoreService


class TestStoreService:
    """Test cases for StoreService."""

    @pytest.fixture
    def service(self):
        """Create store service instance."""
        return StoreService()

    @pytest.mark.asyncio
    async def test_create_product(self, service):
        """Test product creation."""
        result = await service.create_product(
            title="Test Product",
            description="Test description",
            price=29.99,
            tags=["electronics", "sale"]
        )
        
        assert result["success"] == True
        assert "store_product_id" in result
        assert result["title"] == "Test Product"
        assert result["status"] == "draft"

    @pytest.mark.asyncio
    async def test_update_product(self, service):
        """Test product update."""
        create_result = await service.create_product(
            title="Original Title",
            description="Original description",
            price=29.99
        )
        
        store_product_id = create_result["store_product_id"]
        
        update_result = await service.update_product(
            store_product_id=store_product_id,
            title="Updated Title",
            price=34.99
        )
        
        assert update_result["success"] == True
        assert update_result["updated_fields"]["title"] == "Updated Title"
        assert update_result["updated_fields"]["price"] == 34.99

    @pytest.mark.asyncio
    async def test_update_price(self, service):
        """Test price update."""
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        store_product_id = create_result["store_product_id"]
        
        update_result = await service.update_price(
            store_product_id=store_product_id,
            new_price=39.99
        )
        
        assert update_result["success"] == True
        assert update_result["old_price"] == 29.99
        assert update_result["new_price"] == 39.99
        assert "change_percent" in update_result

    @pytest.mark.asyncio
    async def test_publish_product(self, service):
        """Test product publishing."""
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        store_product_id = create_result["store_product_id"]
        
        publish_result = await service.publish_product(store_product_id)
        
        assert publish_result["success"] == True
        assert publish_result["status"] == "active"
        assert "product_url" in publish_result

    @pytest.mark.asyncio
    async def test_unpublish_product(self, service):
        """Test product unpublishing."""
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        store_product_id = create_result["store_product_id"]
        
        await service.publish_product(store_product_id)
        unpublish_result = await service.unpublish_product(store_product_id)
        
        assert unpublish_result["success"] == True
        assert unpublish_result["status"] == "draft"

    @pytest.mark.asyncio
    async def test_delete_product(self, service):
        """Test product deletion."""
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        store_product_id = create_result["store_product_id"]
        
        delete_result = await service.delete_product(store_product_id)
        
        assert delete_result["success"] == True
        
        get_result = await service.get_product(store_product_id)
        assert get_result is None

    @pytest.mark.asyncio
    async def test_get_product(self, service):
        """Test getting product details."""
        create_result = await service.create_product(
            title="Test Product",
            description="Test description",
            price=29.99
        )
        
        store_product_id = create_result["store_product_id"]
        product = await service.get_product(store_product_id)
        
        assert product is not None
        assert product["title"] == "Test Product"
        assert product["price"] == 29.99

    @pytest.mark.asyncio
    async def test_list_products(self, service):
        """Test listing products."""
        await service.create_product(title="Product 1", description="Test", price=19.99)
        await service.create_product(title="Product 2", description="Test", price=29.99)
        await service.create_product(title="Product 3", description="Test", price=39.99)
        
        products = await service.list_products()
        
        assert len(products) == 3

    @pytest.mark.asyncio
    async def test_list_products_by_status(self, service):
        """Test listing products by status."""
        result1 = await service.create_product(title="Draft Product", description="Test", price=19.99)
        result2 = await service.create_product(title="Active Product", description="Test", price=29.99)
        
        await service.publish_product(result2["store_product_id"])
        
        draft_products = await service.list_products(status="draft")
        active_products = await service.list_products(status="active")
        
        assert len(draft_products) == 1
        assert len(active_products) == 1

    @pytest.mark.asyncio
    async def test_simulate_order(self, service):
        """Test order simulation."""
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        await service.publish_product(create_result["store_product_id"])
        
        order_result = await service.simulate_order(
            store_product_id=create_result["store_product_id"],
            quantity=2
        )
        
        assert order_result["success"] == True
        assert "order_id" in order_result
        assert order_result["quantity"] == 2
        assert order_result["total_price"] == 59.98

    @pytest.mark.asyncio
    async def test_simulate_order_unpublished(self, service):
        """Test that order fails for unpublished product."""
        create_result = await service.create_product(
            title="Test Product",
            description="Test",
            price=29.99
        )
        
        order_result = await service.simulate_order(
            store_product_id=create_result["store_product_id"],
            quantity=1
        )
        
        assert order_result["success"] == False

    @pytest.mark.asyncio
    async def test_get_store_stats(self, service):
        """Test store statistics."""
        await service.create_product(title="Product 1", description="Test", price=19.99)
        await service.create_product(title="Product 2", description="Test", price=29.99)
        
        result1 = await service.create_product(title="Product 3", description="Test", price=39.99)
        await service.publish_product(result1["store_product_id"])
        
        stats = await service.get_store_stats()
        
        assert stats["total_products"] == 3
        assert stats["draft_products"] == 2
        assert stats["active_products"] == 1

    @pytest.mark.asyncio
    async def test_update_nonexistent_product(self, service):
        """Test updating non-existent product."""
        result = await service.update_product(
            store_product_id="INVALID-ID",
            title="Test"
        )
        
        assert result["success"] == False

    @pytest.mark.asyncio
    async def test_product_id_generation(self, service):
        """Test that product IDs are generated."""
        result1 = await service.create_product(title="Product 1", description="Test", price=19.99)
        result2 = await service.create_product(title="Product 2", description="Test", price=29.99)
        
        assert result1["store_product_id"] != result2["store_product_id"]
        assert result1["store_product_id"].startswith("SHOPIFY-")
