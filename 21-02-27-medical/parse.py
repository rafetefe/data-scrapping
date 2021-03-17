#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 00:09:51 2021

@author: op
"""

import pandas
from usaddress import parse, tag
#Load

data = pandas.read_csv("adresses.csv")
ctr = pandas.read_csv("country.csv")
abbr = pandas.read_csv("abbr-name.csv")
zips = pandas.read_csv("uszips.csv")

def abi(str):
    return tag(str, tag_mapping={
       'Recipient': 'recipient',
       'AddressNumber': 'address1',
       'AddressNumberPrefix': 'address1',
       'AddressNumberSuffix': 'address1',
       'StreetName': 'address1',
       'StreetNamePreDirectional': 'address1',
       'StreetNamePreModifier': 'address1',
       'StreetNamePreType': 'address1',
       'StreetNamePostDirectional': 'address1',
       'StreetNamePostModifier': 'address1',
       'StreetNamePostType': 'address1',
       'CornerOf': 'address1',
       'IntersectionSeparator': 'address1',
       'LandmarkName': 'address1',
       'USPSBoxGroupID': 'address1',
       'USPSBoxGroupType': 'address1',
       'USPSBoxID': 'address1',
       'USPSBoxType': 'address1',
       'BuildingName': 'address2',
       'OccupancyType': 'address2',
       'OccupancyIdentifier': 'address2',
       'SubaddressIdentifier': 'address2',
       'SubaddressType': 'address2',
       'PlaceName': 'city',
       'StateName': 'state',
       'ZipCode': 'zip_code',
    })
    
