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