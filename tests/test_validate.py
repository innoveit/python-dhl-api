# to run tests: python -m unittest discover -s tests

import unittest
from zoneinfo import ZoneInfo

from config import Setting
from python_dhl.service import DHLService
from python_dhl.resources import address, shipment
from python_dhl.resources.helper import (
    ProductCode,
    ShipmentType,
    TypeCode,
    next_business_day,
    IncotermCode,
    MeasurementUnit,
    ShipperType,
    DocumentType,
    AccountType,
)

LOGO_BASE64 = "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"


class TestDhl(unittest.TestCase):
    def test_validate(self):
        service = DHLService(
            api_key=Setting.DHL_API_KEY,
            api_secret=Setting.DHL_API_SECRET,
            account_number=Setting.DHL_ACCOUNT_EXPORT,
            test_mode=True,
        )

        addr = address.DHLAddress(
            street_line1="Via Maestro Zampieri, 14",
            postal_code=36016,
            province_code="VI",
            country_code="IT",
            city="Thiene",
        )

        validate = service.validate_address(addr, ShipmentType.DELIVERY.value)
        print("\n+++++++++++++++++++++++")
        print("Validate success: ", validate.success)
        if validate.error_title:
            print("Error title: ", validate.error_title)
        self.assertTrue(validate.success)

    def test_shipment(self):
        service = DHLService(
            api_key=Setting.DHL_API_KEY,
            api_secret=Setting.DHL_API_SECRET,
            account_number=Setting.DHL_ACCOUNT_EXPORT,
            test_mode=True,
        )

        accounts = [
            shipment.DHLAccountType(
                type_code=AccountType.SHIPPER, number=Setting.DHL_ACCOUNT_EXPORT
            ),
        ]

        sender_contact = address.DHLContactInformation(
            company_name="Test Co.",
            full_name="Name and surname",
            phone="+39000000000",
            email="matteo.munaretto@innove.it",
            contact_type=ShipperType.BUSINESS.value,
        )
        sender_address = address.DHLPostalAddress(
            street_line1="Via Maestro Zampieri, 14",
            postal_code="36016",
            province_code="VI",
            country_code="IT",
            city_name="Thiene",
        )
        registration_numbers = [
            address.DHLRegistrationNumber(
                type_code=TypeCode.VAT.name,
                number="42342423423",
                issuer_country_code="IT",
            )
        ]

        receiver_contact = address.DHLContactInformation(
            full_name="Customer",
            phone="+39000000000",
            email="matteo.munaretto@innove.it",
            contact_type=ShipperType.PRIVATE.value,
        )
        receiver_address = address.DHLPostalAddress(
            street_line1="Rue Poncelet, 17",
            postal_code="75017",
            country_code="FR",
            city_name="Paris",
        )

        packages = [shipment.DHLProduct(weight=1, length=35, width=28, height=8)]

        shipment_date = next_business_day()
        shipment_date = shipment_date.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        shipment_date = shipment_date.replace(tzinfo=ZoneInfo("Europe/Rome"))

        rates = service.get_rates(
            sender_address, receiver_address, packages[0], shipment_date
        )
        print("\n+++++++++++++++++++++++")
        print("Rates success: ", rates.success)
        if rates.error_title:
            print("Error title: ", rates.error_title)
        self.assertTrue(rates.success)

        added_service = [shipment.DHLAddedService(service_code="PT")]

        content = shipment.DHLShipmentContent(
            packages=packages,
            is_custom_declarable=False,
            description="Shipment test",
            incoterm_code=IncotermCode.DAP.name,
            unit_of_measurement=MeasurementUnit.METRIC.value,
            product_code=ProductCode.EUROPE.value,
        )

        output = shipment.DHLShipmentOutput(
            dpi=300,
            encoding_format="pdf",
            logo_file_format="png",
            logo_file_base64=LOGO_BASE64,
        )

        customer_references = ["id1", "id2"]

        """ 
        Shipment 
        """
        s = shipment.DHLShipment(
            accounts=accounts,
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
            # request_pickup=True,
        )

        ship = service.ship(dhl_shipment=s)
        print("\n+++++++++++++++++++++++")
        print("Ship success: ", ship.success)
        if ship.error_title:
            print("Error title: ", ship.error_title)
            print("Error detail: ", ship.error_detail)
            for e in ship.additional_error_details:
                print(e)
        else:
            print("Tracking numbers", ship.tracking_number)
            print("Dispatch confirmation number", ship.dispatch_confirmation_number)
            print("Labels", len(ship.documents_bytes))
        self.assertTrue(ship.success)

        """
        Pickup if needed
        """
        p = shipment.DHLPickup(
            accounts=accounts,
            sender_contact=sender_contact,
            sender_address=sender_address,
            sender_registration_numbers=registration_numbers,
            receiver_contact=receiver_contact,
            receiver_address=receiver_address,
            pickup_datetime=shipment_date,
            content=content,
        )
        pickup = service.pickup(dhl_pickup=p)
        print("\n+++++++++++++++++++++++")
        print("Pickup success: ", pickup.success)
        if pickup.error_title:
            print("Error title: ", pickup.error_title)
            print("Error detail: ", pickup.error_detail)
            for e in pickup.additional_error_details:
                print(e)
        else:
            print("Confirmation numbers: ", pickup.dispatch_confirmation_numbers)
        self.assertTrue(pickup.success)

        """
        Way back
        """
        added_service.append(shipment.DHLAddedService(service_code="PT"))
        s = shipment.DHLShipment(
            accounts=accounts,
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
        )

        ship = service.ship(dhl_shipment=s)
        print("\n+++++++++++++++++++++++ Shipment")
        print("Way back success: ", ship.success)
        if ship.error_title:
            print("Error title: ", ship.error_title)
            print("Error detail: ", ship.error_detail)
            for e in ship.additional_error_details:
                print(e)
        else:
            print("Tracking numbers", ship.tracking_number)
            print("Labels", len(ship.documents_bytes))
        self.assertTrue(ship.success)

    def test_shipment_with_customs_payed_by_shipper(self):
        service = DHLService(
            api_key=Setting.DHL_API_KEY,
            api_secret=Setting.DHL_API_SECRET,
            account_number=Setting.DHL_ACCOUNT_EXPORT,
            test_mode=True,
        )

        accounts = [
            shipment.DHLAccountType(
                type_code=AccountType.SHIPPER, number=Setting.DHL_ACCOUNT_EXPORT
            ),
            shipment.DHLAccountType(
                type_code=AccountType.DUTIES_TAXES, number=Setting.DHL_ACCOUNT_EXPORT
            ),  # here it specifies that the shipper is also paying the duties
        ]

        sender_contact = address.DHLContactInformation(
            company_name="Test Co.",
            full_name="Name and surname",
            phone="+39000000000",
            email="matteo.munaretto@innove.it",
            contact_type=ShipperType.BUSINESS.value,
        )
        sender_address = address.DHLPostalAddress(
            street_line1="Via Maestro Zampieri, 14",
            postal_code="36016",
            province_code="VI",
            country_code="IT",
            city_name="Thiene",
        )
        registration_numbers = [
            address.DHLRegistrationNumber(
                type_code=TypeCode.VAT.name,
                number="42342423423",
                issuer_country_code="IT",
            )
        ]

        receiver_contact = address.DHLContactInformation(
            full_name="Customer",
            phone="+39000000000",
            email="matteo.munaretto@innove.it",
            contact_type=ShipperType.PRIVATE.value,
        )
        receiver_address = address.DHLPostalAddress(
            street_line1="10 Lincoln Center Plaza",
            postal_code="10023",
            country_code="US",
            city_name="New York",
        )

        packages = [shipment.DHLProduct(weight=1, length=35, width=28, height=8)]

        shipment_date = next_business_day()
        shipment_date = shipment_date.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        shipment_date = shipment_date.replace(tzinfo=ZoneInfo("Europe/Rome"))

        rates = service.get_rates(
            sender_address, receiver_address, packages[0], shipment_date
        )
        print("Rates success: ", rates.success)
        if rates.error_title:
            print("Error title: ", rates.error_title)
        self.assertTrue(rates.success)

        added_service = [
            shipment.DHLAddedService(
                service_code="PK"
            ),  # it specifies that documents are uploaded after the shipment
            shipment.DHLAddedService(
                service_code="DD"
            ),  # it specifies that duties are paid by the sender
        ]

        # Create line items
        line_items = [
            shipment.DHLLineItem(
                number=1,
                description="Line 1",
                price=5.10,
                quantity_value=1,
                quantity_unit="PCS",
                manufacturer_country="IT",
                net_weight=0.01,
                gross_weight=0.01,
                commodity_codes=[{"typeCode": "outbound", "value": 851713}],
            ),
            shipment.DHLLineItem(
                number=2,
                description="Line 2",
                price=4.90,
                quantity_value=1,
                quantity_unit="PCS",
                manufacturer_country="IT",
                net_weight=0.03,
                gross_weight=0.03,
                commodity_codes=[{"typeCode": "outbound", "value": 1234.56}],
            ),
        ]

        # Create export declaration
        export_declaration = shipment.DHLExportDeclaration(
            line_items=line_items,
            invoice_number="FAT12345678",
            invoice_date="2025-04-28",
            terms_of_payment="DAP",
            export_reason_type="permanent",
        )

        content = shipment.DHLShipmentContent(
            packages=packages,
            is_custom_declarable=True,
            declared_value=float(10),
            declared_value_currency="EUR",
            description="Shipment test with customs",
            incoterm_code=IncotermCode.DAP.name,
            unit_of_measurement=MeasurementUnit.METRIC.value,
            product_code=ProductCode.EUROPE.value,
            export_declaration=export_declaration,  # Pass the export declaration here
        )

        output = shipment.DHLShipmentOutput(
            dpi=300,
            encoding_format="pdf",
            logo_file_format="png",
            logo_file_base64=LOGO_BASE64,
        )

        customer_references = ["id1", "id2"]

        """ 
        Shipment 
        """
        s = shipment.DHLShipment(
            accounts=accounts,
            sender_contact=sender_contact,
            sender_address=sender_address,
            sender_registration_numbers=registration_numbers,
            receiver_contact=receiver_contact,
            receiver_address=receiver_address,
            ship_datetime=shipment_date,
            added_services=added_service,
            product_code=ProductCode.OTHER.value,
            content=content,
            output_format=output,
            customer_references=customer_references,
        )

        ship = service.ship(dhl_shipment=s)
        print("\n+++++++++++++++++++++++")
        print("Ship success with customs: ", ship.success)
        if ship.error_title:
            print("Error title: ", ship.error_title)
            print("Error detail: ", ship.error_detail)
            for e in ship.additional_error_details:
                print(e)
        else:
            print("Tracking numbers", ship.tracking_number)
            print("Labels", len(ship.documents_bytes))
        self.assertTrue(ship.success)

        """
        Pickup if needed
        """
        accounts = [
            shipment.DHLAccountType(
                type_code=AccountType.SHIPPER, number=Setting.DHL_ACCOUNT_EXPORT
            ),
        ]

        p = shipment.DHLPickup(
            accounts=accounts,
            sender_contact=sender_contact,
            sender_address=sender_address,
            sender_registration_numbers=registration_numbers,
            receiver_contact=receiver_contact,
            receiver_address=receiver_address,
            pickup_datetime=shipment_date,
            content=content,
        )
        pickup = service.pickup(dhl_pickup=p)
        print("\n+++++++++++++++++++++++")
        print("Pickup success: ", pickup.success)
        if pickup.error_title:
            print("Error title: ", pickup.error_title)
            print("Error detail: ", pickup.error_detail)
            for e in pickup.additional_error_details:
                print(e)
        else:
            print("Confirmation numbers: ", pickup.dispatch_confirmation_numbers)
        self.assertTrue(pickup.success)

        """
        Way back
        """
        added_service.append(shipment.DHLAddedService(service_code="PT"))
        s = shipment.DHLShipment(
            accounts=accounts,
            sender_contact=receiver_contact,
            sender_address=receiver_address,
            receiver_contact=sender_contact,
            receiver_address=sender_address,
            ship_datetime=shipment_date,
            added_services=added_service,
            product_code=ProductCode.OTHER.value,
            content=content,
            output_format=output,
            customer_references=customer_references,
        )

        ship = service.ship(dhl_shipment=s)
        print("\n+++++++++++++++++++++++")
        print("Way back success: ", ship.success)
        if ship.error_title:
            print("Error title: ", ship.error_title)
            print("Error detail: ", ship.error_detail)
            for e in ship.additional_error_details:
                print(e)
        else:
            print("Tracking numbers", ship.tracking_number)
            print("Labels", len(ship.documents_bytes))
        self.assertTrue(ship.success)

    def test_upload_document(self):
        service = DHLService(
            api_key=Setting.DHL_API_KEY,
            api_secret=Setting.DHL_API_SECRET,
            account_number=Setting.DHL_ACCOUNT_EXPORT,
            test_mode=True,
        )

        accounts = [
            shipment.DHLAccountType(
                type_code=AccountType.SHIPPER, number=Setting.DHL_ACCOUNT_EXPORT
            ),
        ]

        shipment_date = next_business_day()
        shipment_date = shipment_date.replace(
            hour=14, minute=0, second=0, microsecond=0
        )
        shipment_date = shipment_date.replace(tzinfo=ZoneInfo("Europe/Rome"))

        document_image = [
            shipment.DHLDocumentImage(
                type_code=DocumentType.INV.name, image_format="pdf", content=LOGO_BASE64
            )
        ]

        document = shipment.DHLDocument(
            accounts=accounts,
            tracking_number="1256929634",
            original_planned_shipping_date=shipment_date,
            product_code=ProductCode.EUROPE.value,
            document_images=document_image,
        )

        upload = service.upload_document(document)
        print("\n+++++++++++++++++++++++")
        print("Upload success: ", upload.success)
        if upload.error_title:
            print("Error title: ", upload.error_title)
        self.assertTrue(upload.success)

        """check = service.check_shipment('1256929634')
        print('\n+++++++++++++++++++++++')
        print('Check success: ', check.success)
        if check.error_title:
            print('Error title: ', check.error_title)
        self.assertTrue(check.success)"""


if __name__ == "__main__":
    unittest.main()
