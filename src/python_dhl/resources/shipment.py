from datetime import datetime
from zoneinfo import ZoneInfo


class DHLProduct:
    def __init__(self, weight, length, width, height):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height


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


class DHLShipmentContent:
    def __init__(self, products, is_custom_declarable, description, incoterm_code, unit_of_measurement,
                 declared_value=None, declared_value_currency=None):
        self.products = products
        self.is_custom_declarable = is_custom_declarable
        self.description = description
        self.incoterm_code = incoterm_code
        self.unit_of_measurement = unit_of_measurement
        self.declared_value = declared_value
        self.declared_value_currency = declared_value_currency


class DHLShipment:
    def __init__(self, sender, receiver, ship_datetime, product_code, added_services, content, request_pickup=False):
        self.sender = sender
        self.receiver = receiver
        self.ship_datetime = ship_datetime
        self.product_code = product_code
        self.added_services = added_services
        self.request_pickup = request_pickup
        self.content = content
