import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from requests.auth import HTTPBasicAuth

from src.python_dhl.resources.response import DHLShipmentResponse, DHLPickupResponse, DHLResponse, DHLUploadResponse, \
    DHLTrackingResponse, DHLRatesResponse, DHLValidateAddressResponse

logger = logging.getLogger(__name__)


class DHLService:
    """
    Main class with static data and the main shipping methods.
    """
    dhl_endpoint = ''
    dhl_endpoint_test = 'https://express.api.dhl.com/mydhlapi/test'

    def __init__(self, api_key, api_secret, account_number, import_account_number, test_mode=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.account_number = account_number
        self.import_account_number = import_account_number
        self.test_mode = test_mode
        self.endpoint_url = self.dhl_endpoint_test if test_mode else self.dhl_endpoint

    def validate_address(self, address, shipment_type):
        try:
            params = {
                'type': shipment_type,
                'strictValidation': 'true',
                "postalCode": address.postal_code,
                "cityName": address.city,
                "countryCode": address.country_code,
            }
            dhl_response = requests.get(
                self.endpoint_url + '/address-validate', params,
                auth=HTTPBasicAuth(self.api_key, self.api_secret)
            )
            response = DHLValidateAddressResponse(
                success=True,
            )
            for attribute, value in dhl_response.json().items():
                if attribute == 'address':
                    response.address = value
                if attribute == 'warnings':
                    response.warnings = value
            return response
        except Exception as err:
            return DHLValidateAddressResponse(
                success=False,
                error_title='No address found.'
            )

    def get_rates(self, sender, receiver, product, shipment_date, with_customs='false', unit_of_measurement='metric'):
        try:
            dhl_ship_date = datetime.strftime(shipment_date, '%Y-%m-%d')
            params = {
                'accountNumber': self.account_number,
                'originCountryCode': sender.country_code,
                'originCityName': sender.city,
                'destinationCountryCode': receiver.country_code,
                'destinationCityName': receiver.city,
                'weight': product.weight,
                'length': product.length,
                'width': product.width,
                'height': product.height,
                'plannedShippingDate': dhl_ship_date,
                'isCustomsDeclarable': with_customs,
                'unitOfMeasurement': unit_of_measurement
            }
            dhl_response = requests.get(
                self.endpoint_url + '/rates', params=params,
                auth=HTTPBasicAuth(self.api_key, self.api_secret)
            )
            response = DHLRatesResponse(
                success=True,
                products=dhl_response.json()['products'],
            )
            return response
        except Exception as err:
            return DHLRatesResponse(
                success=False,
                error_title='No rates found.'
            )

    def get_tracking(self, tracking_number):
        try:
            dhl_response = requests.get(
                self.endpoint_url + '/shipments' + str(tracking_number) + '/tracking',
                auth=HTTPBasicAuth(self.api_key, self.api_secret)
            )
            response = DHLTrackingResponse(
                success=True,
                shipments=dhl_response.json()['shipments'],
            )
            return response
        except Exception as err:
            return DHLTrackingResponse(
                success=False,
                error_title='No shipments found.'
            )

    def check_shipment(self, tracking_number):
        try:
            dhl_response = requests.get(
                self.endpoint_url + '/shipments' + str(tracking_number) + '/proof-of-delivery',
                auth=HTTPBasicAuth(self.api_key, self.api_secret)
            )
            response = DHLUploadResponse(
                success=True,
                documents=dhl_response.json()['documents'],
            )
            return response
        except Exception as err:
            return DHLUploadResponse(
                success=False,
                error_title='No electronic proof of delivery found.'
            )

    def ship(self, dhl_shipment):
        """
        TODO
        :param shipment: DHLShipment
        :return:
        """
        try:
            shipment = self._create_shipment(dhl_shipment)
            dhl_response = requests.post(
                self.endpoint_url + '/shipments', json=shipment,
                auth=HTTPBasicAuth(self.api_key, self.api_secret)
            )
            if 'detail' in dhl_response.json():
                error_title = None
                error_detail = None
                additional_error_details = []
                message = None
                status = None
                for attribute, value in dhl_response.json().items():
                    if attribute == 'title':
                        error_title = value
                    if attribute == 'detail':
                        error_detail = value
                    if attribute == 'additionalDetails':
                        for e in value:
                            additional_error_details.append(e)
                    if attribute == 'message':
                        message = value
                    if attribute == 'status':
                        status = value
                response = DHLShipmentResponse(
                    success=False,
                    error_title=error_title,
                    error_detail=error_detail,
                    additional_error_details=additional_error_details,
                    message = message,
                    status = status
                )
            else:
                response = DHLShipmentResponse(
                    success=True,
                    tracking_numbers=dhl_response.json()['shipmentTrackingNumber'],
                    documents_bytes=dhl_response.json()['documents'],
                )
            return response
        except Exception as err:
            return DHLShipmentResponse(
                success=False,
                error_detail=['No label.']
            )

    def _create_shipment(self, dhl_shipment):
        next_day = datetime.strftime(dhl_shipment.ship_datetime, '%d/%m/%Y %H:%M')

        ship_date = datetime.strptime(next_day, '%d/%m/%Y %H:%M')
        ship_date = ship_date.replace(tzinfo=ZoneInfo('Europe/Rome'))

        dhl_ship_date = datetime.strftime(ship_date, '%Y-%m-%dT%H:%M:%S GMT%z')
        dhl_ship_date = "{0}:{1}".format(
            dhl_ship_date[:-2],
            dhl_ship_date[-2:]
        )

        json_data = {
            "plannedShippingDateAndTime": dhl_ship_date,
            "pickup": {
                "isRequested": dhl_shipment.request_pickup,
                "pickupDetails": {
                    "postalAddress": dhl_shipment.sender_address.to_dict(),
                    "contactInformation": dhl_shipment.sender_contact.to_dict(),
                    "typeCode": dhl_shipment.shipper_type
                },
            },
            "productCode": dhl_shipment.product_code,
            "accounts": [
                {
                    "typeCode": dhl_shipment.account_type,
                    "number": self.account_number
                }
            ],
            "outputImageProperties": dhl_shipment.output_format.to_dict(),
            "customerDetails": {
                "shipperDetails": {
                    "postalAddress": dhl_shipment.sender_address.to_dict(),
                    "contactInformation": dhl_shipment.sender_contact.to_dict(),
                    "typeCode": "business"
                },
                "receiverDetails": {
                    "postalAddress": dhl_shipment.receiver_address.to_dict(),
                    "contactInformation": dhl_shipment.receiver_contact.to_dict(),
                    "typeCode": "private"
                },
            },
            "content": dhl_shipment.content.to_dict()
        }

        if dhl_shipment.pickup_close_time:
            json_data['pickup']['closeTime'] = dhl_shipment.pickup_close_time
        if dhl_shipment.pickup_location:
            json_data['pickup']['location'] = dhl_shipment.pickup_location
        if dhl_shipment.sender_registration_numbers:
            registration_numbers = []
            for r in dhl_shipment.sender_registration_numbers:
                registration_numbers.append(r.to_dict())
            json_data['pickup']['pickupDetails']['registrationNumbers'] = registration_numbers
            json_data['customerDetails']['shipperDetails']['registrationNumbers'] = registration_numbers
        if dhl_shipment.added_services:
            added_services = []
            for a in dhl_shipment.added_services:
                added_services.append(a.to_dict())
            json_data['valueAddedServices'] = added_services
        if dhl_shipment.sender_address.street_line2:
            json_data['pickup']['pickupDetails']['postalAddress']['addressLine2'] = dhl_shipment.sender.street_line2
        if dhl_shipment.sender_address.street_line3:
            json_data['pickup']['pickupDetails']['postalAddress']['addressLine3'] = dhl_shipment.sender.street_line3
        if dhl_shipment.sender_address.county_name:
            json_data['pickup']['pickupDetails']['postalAddress']['countyName'] = dhl_shipment.sender.county_name
        if dhl_shipment.customer_references:
            references = []
            for cr in dhl_shipment.customer_references:
                references.append({'value': cr})
            json_data['customerReferences'] = references

        return json_data

    def pickup(self, dhl_pickup):
        try:
            pickup = self._create_pickup(dhl_pickup)
            dhl_response = requests.post(
                self.endpoint_url + '/pickups', json=pickup,
                auth=HTTPBasicAuth(self.api_key, self.api_secret)
            )
            if 'detail' in dhl_response.json():
                error_title = None
                error_detail = None
                additional_error_details = []
                message = None
                status = None
                for attribute, value in dhl_response.json().items():
                    if attribute == 'title':
                        error_title = value
                    if attribute == 'detail':
                        error_detail = value
                    if attribute == 'additionalDetails':
                        for e in value:
                            additional_error_details.append(e)
                    if attribute == 'message':
                        message = value
                    if attribute == 'status':
                        status = value
                response = DHLShipmentResponse(
                    success=False,
                    error_title=error_title,
                    error_detail=error_detail,
                    additional_error_details=additional_error_details,
                    message=message,
                    status=status
                )
            else:
                response = DHLPickupResponse(
                    success=True,
                    dispatch_confirmation_numbers=dhl_response.json()['dispatchConfirmationNumbers'],
                )
                for attribute, value in dhl_response.json().items():
                    if attribute == 'readyByTime':
                        response.ready_by_time = value
                    if attribute == 'warnings':
                        response.warnings = value
            return response
        except Exception as err:
            return DHLPickupResponse(
                success=False
            )

    def _create_pickup(self, dhl_pickup):
        next_day = datetime.strftime(dhl_pickup.pickup_datetime, '%d/%m/%Y %H:%M')

        ship_date = datetime.strptime(next_day, '%d/%m/%Y %H:%M')
        ship_date = ship_date.replace(tzinfo=ZoneInfo('Europe/Rome'))

        dhl_pickup_date = datetime.strftime(ship_date, '%Y-%m-%dT%H:%M:%S GMT%z')
        dhl_pickup_date = "{0}:{1}".format(
            dhl_pickup_date[:-2],
            dhl_pickup_date[-2:]
        )

        json_data = {
            "plannedPickupDateAndTime": dhl_pickup_date,
            "accounts": [
                {
                    "typeCode": dhl_pickup.account_type,
                    "number": self.account_number
                }
            ],
            "customerDetails": {
                "shipperDetails": {
                    "postalAddress": dhl_pickup.sender_address.to_dict(),
                    "contactInformation": dhl_pickup.sender_contact.to_dict(),
                },
            },
            "shipmentDetails": [dhl_pickup.content.to_dict_pickup()]
        }

        return json_data

    def upload_customs_document(self, dhl_document):
        try:
            original_planned_shipping_date = datetime.strftime(dhl_document.original_planned_shipping_date, '%Y-%m-%d')
            document_data = {
                "shipmentTrackingNumber": dhl_document.tracking_number,
                "originalPlannedShippingDate": original_planned_shipping_date,
                "productCode": dhl_document.product_code,
                "accounts": [
                    {
                        "typeCode": dhl_document.account_type,
                        "number": self.account_number
                    }
                ],
            }
            if dhl_document.document_images:
                document_images = []
                for d in dhl_document.document_images:
                    document_images.append(d.to_dict())
                document_data['document_images'] = document_images
            dhl_response = requests.post(
                self.endpoint_url + '/shipments/' + dhl_document.tracking_number + '/upload-image',
                json=document_data,
                auth=HTTPBasicAuth(self.api_key, self.api_secret)
            )
            response = DHLResponse(
                success=True,
            )
            for attribute, value in dhl_response.json().items():
                if attribute == 'status':
                    response.status = value
            return response
        except Exception as err:
            return DHLResponse(
                success=False
            )