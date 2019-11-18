from django.test import TestCase
from django.urls import reverse
from main import forms,models
from decimal import Decimal


# Create your tests here.

class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"home.html")
        self.assertContains(response, "BookTime")

    def test_about_us_page_works(self):
        response = self.client.get(reverse("about_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"about_us.html")
        self.assertContains(response, "BookTime")

    def test_contact_form_page_works(self):
        response = self.client.get(reverse("contact_us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"contact_form.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(response.context['form'],forms.ContactForm)

    def test_product_page_return_active(self):
        models.Product.objects.create(
            name="cathedral and bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.0")
        )
        models.Product.objects.create(
            name="Tales of two city",
            slug="tales-city",
            price=Decimal("2.0"),
            active=False
        )
        response = self.client.get(
            reverse("products",kwargs={"tag":"all"})
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "BookTime")

        product_list = models.Product.objects.active().order_by("name")

        self.assertEquals(
            list(response.context["object_list"]),
            list(product_list),
        )


    def test_products_page_filters_by_tags_and_active( self ):
        cb = models.Product.objects.create(
            name="cathedral and bazaar",
            slug="cathedral-bazaar",
            price=Decimal("10.0")
        )
        cb.tags.create(
            name="Open source",
            slug="opensource"
        )
        models.Product.objects.create(
            name="Microsoft  windows guide",
            slug="microsoft-guide",
            price=Decimal("2.0")
        )
        response = self.client.get(
            reverse("products",kwargs={"tag":"opensource"})
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "BookTime")

        product_list = models.Product\
                                .objects\
                                .active()\
                                .filter(tags__slug="opensource")\
                                .order_by("name")
        self.assertEquals(
            list(response.context["object_list"]),
            list(product_list),
        )
    
    def test_user_signup_page_loads_correctly( self ):
        response = self.client.get( reverse("signup") )
        self.assertEqual( response.status_code, 200 )
        self.assertTemplateUsed( response, "signup.html")
        self.assertContains( response, "BookTime" )
        self.assertIsInstance(
            response.context["form"],
            forms.UserCreationForm
        )

        
