class DHLResponse:
    def __init__(self, success, errors=None):
        self.success = success
        self.errors = errors

    def __str__(self):
        return '%s' % ('Success' if self.success else 'Fail: '+str(self.errors))


class DHLShipmentResponse(DHLResponse):
    def __init__(self, success, tracking_numbers=None, identification_number=None, dispatch_number=None,
                 label_bytes=None, errors=None):
        DHLResponse.__init__(self, success, errors)

        self.tracking_numbers = tracking_numbers
        self.identification_number = identification_number
        self.dispatch_number = dispatch_number
        self.label_bytes = label_bytes