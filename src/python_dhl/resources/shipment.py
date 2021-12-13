from datetime import datetime
from zoneinfo import ZoneInfo


class DHLProduct:
    def __init__(self, weight, length, width, height):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

    def to_dict(self):
        return {
            "weight": self.weight,
            "dimensions": {
                "length": self.length,
                "width": self.width,
                "height": self.height
            },
        }


class DHLDangerousGood:
    def __init__(self, content_id, dry_ice_total_net_weight, un_code):
        self.content_id = content_id
        self.dry_ice_total_net_weight = dry_ice_total_net_weight
        self.un_code = un_code


class DHLAddedService:
    def __init__(self, service_code, value=None, currency=None, method=None, dangerous_goods=None):
        self.service_code = service_code
        self.value = value
        self.currency = currency
        self.method = method
        self.dangerous_goods = dangerous_goods

    def to_dict(self):
        dict = {
            'serviceCode': self.service_code,
        }
        if self.value:
            dict['value'] = self.value
        if self.currency:
            dict['currency'] = self.currency
        if self.currency:
            dict['method'] = self.method
        if self.currency:
            dict['dangerousGoods'] = self.dangerous_goods
        return dict


class DHLShipmentContent:
    def __init__(self, packages, is_custom_declarable, description, incoterm_code, unit_of_measurement,
                 declared_value=None, declared_value_currency=None, product_code=None):
        self.packages = packages
        self.is_custom_declarable = is_custom_declarable
        self.description = description
        self.incoterm_code = incoterm_code
        self.unit_of_measurement = unit_of_measurement
        self.declared_value = declared_value
        self.declared_value_currency = declared_value_currency
        self.product_code = product_code

    def to_dict(self):
        dict = {
            'packages': self.packages,
            'isCustomsDeclarable': self.is_custom_declarable,
            'description': self.description,
            'incoterm': self.incoterm_code,
            'unitOfMeasurement': self.unit_of_measurement,
        }
        if self.declared_value:
            dict['declaredValue'] = self.declared_value
        if self.declared_value_currency:
            dict['declaredValueCurrency'] = self.declared_value_currency
        return dict

    def to_dict_pickup(self):
        dict = {
            'productCode': self.product_code,
            'packages': self.packages,
            'isCustomsDeclarable': self.is_custom_declarable,
            'unitOfMeasurement': self.unit_of_measurement,
        }
        if self.declared_value:
            dict['declaredValue'] = self.declared_value
        if self.declared_value_currency:
            dict['declaredValueCurrency'] = self.declared_value_currency
        return dict


class DHLShipmentOutput:
    def __init__(self, dpi, logo_file_format, logo_file_base64, encoding_format='pdf',
                 split_transport_and_waybill_doc_labels=True,
                 all_documents_in_one_image=True, split_documents_by_pages=True, split_invoice_and_receipt=True):
        self.dpi = dpi
        self.logo_file_format = logo_file_format
        self.logo_file_base64 = logo_file_base64
        self.encoding_format = encoding_format
        self.split_transport_and_waybill_doc_labels = split_transport_and_waybill_doc_labels
        self.all_documents_in_one_image = all_documents_in_one_image
        self.split_documents_by_pages = split_documents_by_pages
        self.split_invoice_and_receipt = split_invoice_and_receipt

    def to_dict(self):
        return {
            'printerDPI': self.dpi,
            'customerLogos': [{
                'fileFormat': self.logo_file_format.upper(),
                'content': self.logo_file_base64
            }],
            'encodingFormat': self.encoding_format.lower(),
            'splitTransportAndWaybillDocLabels': self.split_transport_and_waybill_doc_labels,
            'allDocumentsInOneImage': self.all_documents_in_one_image,
            'splitDocumentsByPages': self.split_documents_by_pages,
            'splitInvoiceAndReceipt': self.split_invoice_and_receipt,
        }


class DHLShipment:
    def __init__(self, sender_contact, sender_address, receiver_contact, receiver_address, ship_datetime,
                 product_code, added_services, content, output_format, account_type='shipper',
                 customer_references=None, sender_registration_numbers=None,
                 request_pickup=False, pickup_close_time=None, pickup_location=None):
        self.sender_contact = sender_contact
        self.sender_address = sender_address
        self.sender_registration_numbers = sender_registration_numbers
        self.receiver_contact = receiver_contact
        self.receiver_address = receiver_address
        self.ship_datetime = ship_datetime
        self.product_code = product_code
        self.added_services = added_services
        self.content = content
        self.request_pickup = request_pickup
        self.pickup_close_time = pickup_close_time
        self.pickup_location = pickup_location
        self.account_type = account_type
        self.output_format = output_format
        self.customer_references = customer_references


class DHLPickup:
    def __init__(self, sender_contact, sender_address, receiver_contact, receiver_address, pickup_datetime,
                 content, account_type='shipper', sender_registration_numbers=None):
        self.sender_contact = sender_contact
        self.sender_address = sender_address
        self.sender_registration_numbers = sender_registration_numbers
        self.receiver_contact = receiver_contact
        self.receiver_address = receiver_address
        self.pickup_datetime = pickup_datetime
        self.content = content
        self.account_type = account_type
