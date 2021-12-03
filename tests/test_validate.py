# to run tests: python -m unittest discover -s tests

import unittest
from config import Setting
from src.python_dhl import dhl
from src.python_dhl.resources import address, helper, shipment


class TestDhl(unittest.TestCase):
    def test_validate(self):
        service = dhl.DHLService(api_key=Config.DHL_API_KEY, api_secret=Config.DHL_API_SECRET,
                                 account_number=Config.DHL_ACCOUNT_EXPORT,
                                 import_account_number=Config.DHL_ACCOUNT_IMPORT,
                                 test_mode=True)

        addr = address.DHLAddress(
            street_line='Via Maestro Zampieri, 14',
            postal_code=36016,
            province_code='VI',
            country_code='IT',
            city='Thiene',
        )

        validate = service.validate_address(addr, helper.TypeOfShipment.DELIVERY)
        # print(validate)
        self.assertIn('address', validate)

    def test_shipment(self):
        service = dhl.DHLService(api_key=Config.DHL_API_KEY, api_secret=Config.DHL_API_SECRET,
                                 account_number=Config.DHL_ACCOUNT_EXPORT,
                                 import_account_number=Config.DHL_ACCOUNT_IMPORT,
                                 test_mode=True)

        registration = address.DHLRegistrationNumber(
            type_code=helper.TypeCode.VAT,
            number='42342423423',
            issuer_country_code='IT'
        )
        sender = address.DHLCompany(
            company_name='Test Co.',
            full_name='Name and surname',
            phone='+39000000000',
            email='matteo.munaretto@innove.it',
            street_line='Via Maestro Zampieri, 14',
            postal_code=36016,
            province_code='VI',
            country_code='IT',
            city='Thiene',
            registration_numbers=[registration.get_registration()]
        )

        receiver = address.DHLAddress(
            street_line='Via Maestro Zampieri, 14',
            postal_code=36016,
            province_code='VI',
            country_code='IT',
            city='Thiene',
        )

        shipment_date = helper.next_business_day()
        shipment_date = shipment_date.replace(hour=14, minute=0, second=0, microsecond=0)

        s = shipment.DHLShipment(
            sender=sender,
            receiver=receiver,
            ship_datetime=shipment_date,
            product_code=helper.ProductCode.DOMESTIC
        )

        validate = service.ship(dhl_shipment=s)
        # print(validate)
        self.assertIn('address', validate)

if __name__ == '__main__':
    unittest.main()