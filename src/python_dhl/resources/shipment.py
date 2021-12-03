from datetime import datetime
from zoneinfo import ZoneInfo


class DHLDangerousGood:
    def __init__(self, content_id, dry_ice_total_net_weight, un_cide):
        self.content_id = content_id
        self.dry_ice_total_net_weight = dry_ice_total_net_weight
        self.un_cide = un_cide


class DHLService:
    def __init__(self, service_code, value=None, currency=None, method=None, dangerous_goods=None):
        self.service_code = service_code
        self.value = value
        self.currency = currency
        self.method = method
        self.dangerous_goods = dangerous_goods


class DHLShipment:
    def __init__(self, sender, receiver, ship_datetime, product_code, added_services, request_pickup=False):
        self.sender = sender
        self.receiver = receiver
        self.ship_datetime = ship_datetime
        self.product_code = product_code
        self.added_services = added_services
        self.request_pickup = request_pickup