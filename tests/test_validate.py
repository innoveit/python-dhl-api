# to run tests: python -m unittest discover -s tests

import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from config import Setting
from src.python_dhl import dhl
from src.python_dhl.resources import address, shipment
from src.python_dhl.resources.helper import ProductCode, ShipmentType, TypeCode, next_business_day, IncotermCode, \
    MeasurementUnit, ShipperType


class TestDhl(unittest.TestCase):
    def test_validate(self):
        service = dhl.DHLService(api_key=Setting.DHL_API_KEY, api_secret=Setting.DHL_API_SECRET,
                                 account_number=Setting.DHL_ACCOUNT_EXPORT,
                                 import_account_number=Setting.DHL_ACCOUNT_IMPORT,
                                 test_mode=True)

        addr = address.DHLAddress(
            street_line1='Via Maestro Zampieri, 14',
            postal_code=36016,
            province_code='VI',
            country_code='IT',
            city='Thiene',
        )

        validate = service.validate_address(addr, ShipmentType.DELIVERY.value)
        print('+++++++++++++++++++++++')
        print('Validate success: ', validate.success)
        if validate.error_title:
            print('Error title: ', validate.error_title)
        self.assertTrue(validate.success)

    def test_shipment(self):
        service = dhl.DHLService(api_key=Setting.DHL_API_KEY, api_secret=Setting.DHL_API_SECRET,
                                 account_number=Setting.DHL_ACCOUNT_EXPORT,
                                 import_account_number=Setting.DHL_ACCOUNT_IMPORT,
                                 test_mode=True)

        sender_contact = address.DHLContactInformation(
            company_name='Test Co.',
            full_name='Name and surname',
            phone='+39000000000',
            email='matteo.munaretto@innove.it',
        )
        sender_address = address.DHLPostalAddress(
            street_line1='Via Maestro Zampieri, 14',
            postal_code='36016',
            province_code='VI',
            country_code='IT',
            city_name='Thiene',
        )
        registration_numbers = [address.DHLRegistrationNumber(
            type_code=TypeCode.VAT.name,
            number='42342423423',
            issuer_country_code='IT'
        )]

        receiver_contact = address.DHLContactInformation(
            full_name='Customer',
            phone='+39000000000',
            email='matteo.munaretto@innove.it',
        )
        receiver_address = address.DHLPostalAddress(
            street_line1='Rue Poncelet, 17',
            postal_code='75017',
            country_code='FR',
            city_name='Paris',
        )

        product = shipment.DHLProduct(
            weight=1,
            length=35,
            width=28,
            height=8
        )

        shipment_date = next_business_day()
        shipment_date = shipment_date.replace(hour=14, minute=0, second=0, microsecond=0)
        shipment_date = shipment_date.replace(tzinfo=ZoneInfo('Europe/Rome'))

        rates = service.get_rates(sender_address, receiver_address, product, shipment_date)
        print('+++++++++++++++++++++++')
        print('Rates success: ', rates.success)
        if rates.error_title:
            print('Error title: ', rates.error_title)
        self.assertTrue(rates.success)

        added_service = [shipment.DHLAddedService(
            service_code='W'
        )]

        content = shipment.DHLShipmentContent(
            packages=[product.to_dict()],
            is_custom_declarable=False,
            description='Shipment test',
            incoterm_code=IncotermCode.DAP.name,
            unit_of_measurement=MeasurementUnit.METRIC.value,
            product_code=ProductCode.EUROPE.value
        )

        output = shipment.DHLShipmentOutput(
            dpi=300,
            encoding_format='pdf',
            logo_file_format='png',
            logo_file_base64='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'
        )

        customer_references = ['id1', 'id2']

        """ 
        Shipment 
        """
        s = shipment.DHLShipment(
            sender_contact=sender_contact,
            sender_address=sender_address,
            sender_registration_numbers=registration_numbers,
            receiver_contact=receiver_contact,
            receiver_address=receiver_address,
            ship_datetime=shipment_date,
            added_services=added_service,
            product_code=ProductCode.EUROPE.value,
            content=content,
            output_format=output,
            customer_references=customer_references,
            shipper_type=ShipperType.BUSINESS.value,
        )

        ship = service.ship(dhl_shipment=s)
        print('+++++++++++++++++++++++')
        print('Ship success: ', ship.success)
        if ship.error_title:
            print('Error title: ', ship.error_title)
            print('Error detail: ', ship.error_detail)
            for e in ship.additional_error_details:
                print(e)
        else:
            print('Tracking numbers', ship.tracking_numbers)
            print('Labels', len(ship.documents_bytes))
        self.assertTrue(ship.success)

        """
        Pickup
        """
        p = shipment.DHLPickup(
            sender_contact=sender_contact,
            sender_address=sender_address,
            sender_registration_numbers=registration_numbers,
            receiver_contact=receiver_contact,
            receiver_address=receiver_address,
            pickup_datetime=shipment_date,
            content=content,
        )
        pickup = service.pickup(dhl_pickup=p)
        print('+++++++++++++++++++++++')
        print('Pickup success: ', pickup.success)
        if pickup.error_title:
            print('Error title: ', pickup.error_title)
            print('Error detail: ', pickup.error_detail)
            for e in pickup.additional_error_details:
                print(e)
        else:
            print('Confirmation numbers: ', pickup.dispatch_confirmation_numbers)
        self.assertTrue(pickup.success)

        """
        Way back
        """
        added_service.append(shipment.DHLAddedService(
            service_code='PT'
        ))
        s = shipment.DHLShipment(
            sender_contact=receiver_contact,
            sender_address=receiver_address,
            receiver_contact=sender_contact,
            receiver_address=sender_address,
            ship_datetime=shipment_date,
            added_services=added_service,
            product_code=ProductCode.EUROPE.value,
            content=content,
            output_format=output,
            customer_references=customer_references,
            shipper_type=ShipperType.PRIVATE.value,
        )

        ship = service.ship(dhl_shipment=s)
        print('+++++++++++++++++++++++')
        print('Way back success: ', ship.success)
        if ship.error_title:
            print('Error title: ', ship.error_title)
            print('Error detail: ', ship.error_detail)
            for e in ship.additional_error_details:
                print(e)
        else:
            print('Tracking numbers', ship.tracking_numbers)
            print('Labels', len(ship.documents_bytes))
        self.assertTrue(ship.success)

    def test_upload_document(self):
        service = dhl.DHLService(api_key=Setting.DHL_API_KEY, api_secret=Setting.DHL_API_SECRET,
                                 account_number=Setting.DHL_ACCOUNT_EXPORT,
                                 import_account_number=Setting.DHL_ACCOUNT_IMPORT,
                                 test_mode=True)

        shipment_date = next_business_day()
        shipment_date = shipment_date.replace(hour=14, minute=0, second=0, microsecond=0)
        shipment_date = shipment_date.replace(tzinfo=ZoneInfo('Europe/Rome'))

        document_image = [shipment.DHLDocumentImage(
            type_code=TypeCode.GST.value,
            image_format='pdf',
            content=''
        )]

        document = shipment.DHLDocument(
            tracking_number='1256929634',
            original_planned_shipping_date=shipment_date,
            product_code=ProductCode.EUROPE.value,
            document_images=document_image
        )

        upload = service.upload_customs_document(document)
        print('+++++++++++++++++++++++')
        print('Upload success: ', upload.success)
        self.assertTrue(upload.success)

        check = service.check_shipment('1256929634')
        print('+++++++++++++++++++++++')
        print('Check success: ', check.success)
        if check.error_title:
            print('Error title: ', check.error_title)
        self.assertTrue(check.success)


if __name__ == '__main__':
    unittest.main()
