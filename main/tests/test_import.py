from io import StringIO
import tempfile
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from main import models


class TestImport(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def import_test_data(self):
        out = StringIO()
        args = [
            'main/fixtures/product-sample.csv',
            'main/fixtures/product-sampleimages/',
        ]
        call_command( 'import_data', *args, stdout=out)

        expected_out = (
            "Importing product\n"
            "Product processed=3 (created=3)\n"
            "Tags processed=6 (created=6)\n"
            "Images processed=3\n"
        )
        self.assertEquals(expected_out, out)
        self.assertEquals( models.Product.objects.count(), 3 )
        self.assertEquals( models.ProductTag.objects.count(), 6 )
        self.assertEquals( models.ProductImage.objects.count(), 3 )