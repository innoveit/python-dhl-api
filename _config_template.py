class Setting:
    """
    It can be that you have two different accounts for shipping and returning but it is not necessary.
    DHL_ACCOUNT_EXPORT for sending goods
    DHL_ACCOUNT_IMPORT for returning goods
    """
    DHL_API_KEY = ''
    DHL_API_SECRET = ''
    DHL_ACCOUNT = ''
    DHL_ACCOUNT_IMPORT = ''
    DHL_ACCOUNT_EXPORT = ''

    def __init__(self):
        pass
