from django.test import TestCase

from .mpesa import normalize_phone_number, format_mpesa_amount


class MpesaHelperTests(TestCase):
    def test_normalize_phone_number_accepts_local_ke_number(self):
        self.assertEqual(normalize_phone_number("0712345678"), "254712345678")

    def test_format_mpesa_amount_rounds_to_two_decimal_places(self):
        self.assertEqual(format_mpesa_amount(1250), "1250.00")
