from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from main import forms, models

class ContactUsView(FormView):
    template_name = "contact_form.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form) :
        form.send_mail()
        return super().form_valid(form)


class ProductListView( ListView ):
    template_name = 'main/product_list.html'
    paginate_by = 4

    def get_queryset(self):
        tags = self.kwargs['tag']
        self.tags = None

        if tags != "all":
            self.tags = get_object_or_404(
                models.ProductTag, slug=tags
            )
        if self.tags :
            products = models.Product.objects.active().filter(
                                    tags=self.tags
                                )
        else :
            products = models.Product.objects.active()

        return products.order_by("name")

        
    
