class DHLResponse:
    def __init__(self, success, error_title=None, error_detail=None, additional_error_details=None):
        self.success = success
        self.error_title = error_title
        self.error_detail = error_detail
        self.additional_error_details = additional_error_details

    def __str__(self):
        return '%s' % ('Success' if self.success else 'Fail: '+str(self.error_title))


class DHLShipmentResponse(DHLResponse):
    def __init__(self, success, tracking_numbers=None, identification_number=None, dispatch_number=None,
                 documents_bytes=None, error_title=None, error_detail=None, additional_error_details=None):
        DHLResponse.__init__(self, success, error_title, error_detail, additional_error_details)

        self.tracking_numbers = tracking_numbers
        self.identification_number = identification_number
        self.dispatch_number = dispatch_number
        self.documents_bytes = documents_bytes