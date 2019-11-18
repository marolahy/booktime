
from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from main import views
from django.conf import settings
from django.conf.urls.static import static
from main import models, forms
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("products/<slug:tag>/",
        views.ProductListView.as_view(),
        name="products"
    ),
    path("product/<int:pk>/",
        DetailView.as_view(model=models.Product),
        name="product"
    ),
    path('contact-us',
        views.ContactUsView.as_view(template_name="contact_form.html"),
        name="contact_us"),
    path(
        "about-us/",
        TemplateView.as_view(template_name="about_us.html"),
        name="about_us",
    ),
    path("",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),
    path('signup/',
        views.SignupView.as_view(),
        name="signup"
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name="login.html",
            form_class=forms.AuthenticationForm,
        ),
        name="login"
    ),
] + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
