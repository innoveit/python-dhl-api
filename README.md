# python-dhl-api
[![PyPI version](https://badge.fury.io/py/python-dhl-api.svg)](https://badge.fury.io/py/python-dhl-api)

A Django module to integrate with DHL EXPRESS API (MyDHL API).

DHL APIs documentation: https://developer.dhl.com/api-reference/dhl-express-mydhl-api#reference-docs-section/

## Requirements
Python 3.9+

## Installation
Python DHL API is available through pip. To easily install or upgrade it, do
```
pip install --upgrade python-dhl-api
```

## Usage
Set the following DHL fields in a private file.
```
DHL_API_KEY = ''
DHL_API_SECRET = ''
DHL_ACCOUNT = ''
DHL_ACCOUNT_IMPORT = '' 
DHL_ACCOUNT_EXPORT = ''
```

## Services available
Please check test_validate.py to see some practical uses.
1. Address validation
2. Get rates and services available
3. Create a shipment
4. Create a pickup
5. Upload document
6. Check shipment
7. Shipment status


## Create a shipment
```py
service = DHLService(api_key=Setting.DHL_API_KEY, api_secret=Setting.DHL_API_SECRET,
                     account_number=Setting.DHL_ACCOUNT_EXPORT,
                     test_mode=True)
```

Set one or more accounts:
```py
accounts = [
    shipment.DHLAccountType(type_code=AccountType.SHIPPER, number=Setting.DHL_ACCOUNT_EXPORT),
]
```
If you want the shipper to pay also the duties then:

```py
accounts = [
    shipment.DHLAccountType(type_code=AccountType.SHIPPER, number=Setting.DHL_ACCOUNT_EXPORT),
    shipment.DHLAccountType(type_code=AccountType.DUTIES_TAXES, number=Setting.DHL_ACCOUNT_EXPORT),
]
```

Create the sender:
```py
sender_contact = address.DHLContactInformation(
    company_name='Test Co.',
    full_name='Name and surname',
    phone='+39000000000',
    email='matteo.munaretto@innove.it',
    contact_type=ShipperType.BUSINESS.value
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
```

Create the receiver:
```py
receiver_contact = address.DHLContactInformation(
    full_name='Customer',
    phone='+39000000000',
    email='matteo.munaretto@innove.it',
    contact_type=ShipperType.PRIVATE.value
)
receiver_address = address.DHLPostalAddress(
    street_line1='Rue Poncelet, 17',
    postal_code='75017',
    country_code='FR',
    city_name='Paris',
)
```

Add the packages to ship:
```py
packages = [shipment.DHLProduct(
    weight=1,
    length=35,
    width=28,
    height=8
)]
```

Set content and label output. For a list of services you are entitled to, use service get_rates.
```py
shipment_date = next_business_day()
shipment_date = shipment_date.replace(hour=14, minute=0, second=0, microsecond=0)
shipment_date = shipment_date.replace(tzinfo=ZoneInfo('Europe/Rome'))

added_service = [shipment.DHLAddedService(
    service_code='W'
)]

content = shipment.DHLShipmentContent(
    packages=packages,
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
    logo_file_base64=LOGO_BASE64
)

customer_references = ['id1', 'id2']
```

Let's ship:
```py
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
)

ship = service.ship(dhl_shipment=s)
```
