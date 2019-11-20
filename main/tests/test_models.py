from decimal import Decimal
from django.test import TestCase
from main import models

class TestModel(TestCase):
    def test_active_manager_work(self):
        models.Product.objects.create(
            name="The cathedral with the baazar",
            price=Decimal("10.00")
        )
        models.Product.objects.create(
            name="Pride and prejudice",
            price=Decimal("2.00")
        )
        models.Product.objects.create(
            name="A tale of two city",
            price=Decimal("2.00"),
            active=False
        )
        
        self.assertEquals(2,len(models.Product.objects.active()))

    def test_create_order_works(self):
        p1 = models.Product.objects.create(
            name="The cathedral with the baazar",
            price=Decimal("10.00")
        )
        p2 = models.Product.objects.create(
            name="Pride and prejudice",
            price=Decimal("2.00")
        )
        user1 = models.User.objects.create_user(
            "user1",
            "pw432joij"
        )
        billing = models.Address.objects.create(
            user=user1,
            name="john kimball",
            address1="flat 2",
            address2="12 Stralz avenue",
            city="London",
            country="uk"
        )
        shipping = models.Address.objects.create(
            user=user1,
            name="marc kimball",
            address1="123 Deacon road",
            city="London",
            country="uk"
        )

        basket = models.Basket.objects.create(user=user1)
        models.BasketLine.objects.create(
            basket=basket, product=p1
        )
        models.BasketLine.objects.create(
            basket=basket, product=p2
        )

        with self.assertLogs("main.models", level="INFO") as cm:
            order = basket.create_order(billing, shipping)

        self.assertGreaterEqual(len(cm.output), 1)

        order.refresh_from_db()

        self.assertEquals(order.user, user1)
        self.assertEquals(
            order.billing_address1, billing.address1
        )
        self.assertEquals(
            order.shipping_address1, shipping.address1
        )

        self.assertEquals(order.lines.all().count(), 2)
        lines = order.lines.all()
        self.assertEquals(lines[0].product, p1)
        self.assertEquals(lines[1].product, p2)