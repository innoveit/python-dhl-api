# to run tests: python -m unittest discover -s tests

import unittest
from zoneinfo import ZoneInfo

from config import Setting
from src.python_dhl import dhl
from src.python_dhl.resources import address, helper, shipment


class TestDhl(unittest.TestCase):
    def test_validate(self):
        service = dhl.DHLService(api_key=Setting.DHL_API_KEY, api_secret=Setting.DHL_API_SECRET,
                                 account_number=Setting.DHL_ACCOUNT_EXPORT,
                                 import_account_number=Setting.DHL_ACCOUNT_IMPORT,
                                 test_mode=True)

        addr = address.DHLAddress(
            street_line='Via Maestro Zampieri, 14',
            postal_code=36016,
            province_code='VI',
            country_code='IT',
            city='Thiene',
        )

        validate = service.validate_address(addr, helper.ShipmentType.DELIVERY.value)
        print(validate)
        self.assertIn('address', validate)

    def test_shipment(self):
        service = dhl.DHLService(api_key=Setting.DHL_API_KEY, api_secret=Setting.DHL_API_SECRET,
                                 account_number=Setting.DHL_ACCOUNT_EXPORT,
                                 import_account_number=Setting.DHL_ACCOUNT_IMPORT,
                                 test_mode=True)

        registration = address.DHLRegistrationNumber(
            type_code=helper.TypeCode.VAT.name,
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

        receiver = address.DHLPerson(
            street_line='Via Maestro Zampieri, 14',
            postal_code=36016,
            province_code='VI',
            country_code='IT',
            city='Thiene',
            email='matteo.munaretto@gmail.com',
            full_name='Sender',
            phone='000000000'
        )

        product = shipment.DHLProduct(
            weight=1,
            length=35,
            width=28,
            height=8
        )

        shipment_date = helper.next_business_day()
        shipment_date = shipment_date.replace(hour=14, minute=0, second=0, microsecond=0)
        shipment_date = shipment_date.replace(tzinfo=ZoneInfo('Europe/Rome'))

        rates = service.get_rates(sender, receiver, product, shipment_date)
        # for p in rates.get('products'):
        #     print(str(p.get('productName')) + ' - ' + str(p.get('productCode')))

        added_service = shipment.DHLAddedService(
            service_code='WY'
        )

        content = shipment.DHLShipmentContent(
            products=[product.__dict__],
            is_custom_declarable=False,
            description='Shipment test',
            incoterm_code=helper.IncotermCode.DAP.name,
            unit_of_measurement=helper.MeasurementUnit.METRIC.value
        )

        s = shipment.DHLShipment(
            sender=sender,
            receiver=receiver,
            ship_datetime=shipment_date,
            added_services=[added_service.__dict__],
            product_code=helper.ProductCode.DOMESTIC.value,
            content=content.__dict__
        )

        ship = service.ship(dhl_shipment=s)
        print('+++++++++++++++++++++++')
        print(ship.success)
        print('+++++++++++++++++++++++')
        self.assertTrue(ship.success)


if __name__ == '__main__':
    unittest.main()
