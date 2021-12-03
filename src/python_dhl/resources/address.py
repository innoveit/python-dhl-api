from enum import Enum


class DHLAddress:
    """
    Saves all the address data.
    """

    def __init__(self, street_line, city, postal_code, province_code, country_code,
                 county_name=None, street_line2=None, street_line3=None):
        self.street_line = street_line
        self.city = city
        self.postal_code = postal_code
        self.province_code = province_code
        self.country_code = country_code
        self.county_name = county_name
        self.street_line2 = street_line2
        self.street_line3 = street_line3


class DHLRegistrationNumber:
    def __init__(self, type_code, number, issuer_country_code):
        self.type_code = type_code
        self.number = number
        self.issuer_country_code = issuer_country_code

    def get_registration(self):
        return {
            "typeCode": self.type_code,
            "number": self.number,
            "issuerCountryCode": self.issuer_country_code
        }


class DHLCompany(DHLAddress):
    """
    A class for creating the shipper and the recipient in the DHLShipment.
    """

    def __init__(self, company_name, full_name, phone, registration_numbers,
                 street_line, city, postal_code, province_code, country_code,
                 county_name=None, street_line2=None, street_line3=None, email=None):
        DHLAddress.__init__(self, street_line, city, postal_code, province_code, country_code, county_name, street_line2, street_line3)

        self.company_name = company_name
        self.full_name = full_name
        self.phone = phone
        self.email = email
        self.registration_numbers = registration_numbers


class DHLPerson(DHLCompany):
    """
    A class for creating a company instead of a person for use in DHLShipment.
    # DHL requires the company name, so we use person name
    """

    def __init__(self, full_name, phone,
                 street_line, city, postal_code, province_code, country_code,
                 county_name=None, street_line2=None, street_line3=None, email=None):
        DHLAddress.__init__(self, street_line, city, postal_code, province_code, country_code, county_name, street_line2, street_line3)

        self.full_name = full_name
        self.phone = phone
        self.email = email