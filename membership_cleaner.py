#!/usr/local/bin/python3
# -----------------------------------------------------------------------
# Copyright (C) 2020 Academic Library Association of Ohio
# Derek C. Zoladz <derek@derekzoladz.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# -----------------------------------------------------------------------

# SET FILENAMES
input_filename = 'data/raw/ALAOdata.csv'
output_filename = 'data/processed/ALAOdata-clean.csv'

import pandas as pd
import os
import re

# FUNCTION DEFINITIONS

def grab_df():
    cd = os.getcwd()
    input_file = cd + '/' + input_filename
    df = pd.read_csv(input_file)
    return df

def write_output_file(df):
    cd = os.getcwd()
    output_file = cd + '/' + output_filename
    df.to_csv(output_file, encoding='utf-8')

def clean_city(items):
    cities = []
    for item in items:
        if type(item) is not str:
            item = ''
            cities.append(item)
        else:
            item = str(item).lower()
            item = item.title()
            cities.append(item)
    x = pd.Series(cities)
    return x

def clean_orgs(orgs):
    organizations = []
    special_org_map = {
        "Ohionet": "OhioNET",
        "Ohiolink": "OhioLINK",
        'Oclc': 'OCLC',
        'Lexisnexis': 'LexisNexis',
        'Proquest': 'ProQuest',
        'Ebsco': 'EBSCO',
        'Olssi': 'OLSSI',
        'Utc': 'UTC',
        'Osu-Newark/Cotc': 'OSU-Newark/COTC',
        'Bgsu': 'BGSU',
        'Uw-M': 'UW-M',
        'Osu Libraries': 'OSU Libraries',
        'Pbs': 'PBS',
        'Ala And Acrl': 'ALA and ACRL',
        'Infohio': 'INFOhio',
        'Cwru': 'CWRU',
        'Osu': 'OSU',
        'Mla': 'MLA',
        'Sscc': 'SSCC',
        'Onu': 'ONU',
        'Ksu Slis': 'KSU SLIS'
    }
    for org in orgs:
        if type(org) is not str:
            org = ''
        else:
            org = str(org).title()
            for key, value in special_org_map.items():
                if org == key:
                    org = value
        organizations.append(org)
    x = pd.Series(organizations)
    return x

def clean_states(states):
    clean_states = []
    for state in states:
        if type(state) is not str:
            state = ''
        else:
            state = str(state)[:2].upper()
        clean_states.append(state)
    x = pd.Series(clean_states)
    return x

def clean_zips(zips):
    zips_list = []
    for zip in zips:
        if type(zip) is not str:
            zip = ''
        elif len(str(zip).strip()) <= 4:
            zip = ''
        elif ' ' in zip:
            zip = ''
        else:
            zip = zip[:5]
        zips_list.append(zip)
    x = pd.Series(zips_list)
    return x

def clean_phone(numbers):
    clean_numbers = []
    for number in numbers:
        if type(number) is not str:
            number = ''
        else:
            number = re.sub('[^0-9]', '', number)
            # NANP rules do not permit the digits 0 and 1 as the leading digit
            if number.startswith('0') or len(number) < 7:
                number = ''
            elif number.startswith('1'):
                number = re.sub('^([1]{1})([0-9]{3})([0-9]{3})([0-9]{4})', '1-\\2-\\3-\\4', number)
            elif len(number) == 7:
                number = re.sub('^([0-9]{3})([0-9]{4})', '\\1-\\2', number)
            elif len(number) == 10:
                number = re.sub('^([0-9]{3})([0-9]{3})([0-9]{4})', '\\1-\\2-\\3', number)
            elif len(number) > 10:
                number = re.sub('^([0-9]{3})([0-9]{3})([0-9]{4})([0-9])', '\\1-\\2-\\3 x\\4', number)
            else:
                number = ''
        clean_numbers.append(number)
    x = pd.Series(clean_numbers)
    return x

def clean_countries(countries):
    clean_countries = []
    for country in countries:
        if type(country) is not str:
            country = ''
        elif re.match('[uU].*', str(country)):
            country = 'USA'
        else:
            country = str(country).upper()
        clean_countries.append(country)
    x = pd.Series(clean_countries)
    return x

def clean_address(addresses):
    clean_addr1 = []
    for address in addresses:
        if type(address) is not str:
            address = ''
        else:
            address = str(address).title()
            if ' Of ' in address:
                address = address.replace('Of', 'of')
            elif 'Ohionet' in address:
                address = address.replace('Ohionet', 'OhioNET')
        clean_addr1.append(address)
    x = pd.Series(clean_addr1)
    return x


# MAIN PROGRAM

def main():
    # get the data
    data = grab_df()

    # drop these columns
    drop_columns = [
        'Password',
        'Interest Groups',
        'ACRL Member',
        'Membership History (2010 & prior)',
        'Retired',
        'Group participation',
        'Current Leadership Positions',
        'Past Leadership Positions',
        'Current Committees',
        'Past Committees',
        'ALAO Awards',
        'Directory listing text',
        'Expected Graduation Date',
        'School Attending',
        'Archived',
        'Subscribed to emails',
        'Subscription source',
        'Opted in',
        'Event announcements',
        'Member emails and newsletters',
        'Administration access',
        'Created on',
        'Profile last updated',
        'Last login',
        'Updated by',
        'Balance',
        'Total donated',
        'Membership enabled',
        'Membership level',
        'Member since',
        'Renewal due',
        'Renewal date last changed',
        'Level last changed',
        'Access to profile by others',
        'Details to show',
        'Photo albums enabled',
        'Member bundle ID or email',
        'Member role',
        'Details to show',
        'Work Email Address',
        'Home Email Address',
        'Notes'
    ]
    data.drop(drop_columns, inplace=True, axis=1)


    # do stuff with the data
    data['First name'] = data['First name'].str.title()
    data['Last name'] = data['Last name'].str.title()
    data['Work City'] = clean_city(data['Work City'])
    data['Organization'] = clean_orgs(data['Organization'])
    data['Work Province/State'] = clean_states(data['Work Province/State'])
    data['Work Postal Code'] = clean_zips(data['Work Postal Code'])
    data['Preferred Phone'] = clean_phone(data['Preferred Phone'])
    data['Work Phone'] = clean_phone(data['Work Phone'])
    data['Work Cellular Phone'] = clean_phone(data['Work Cellular Phone'])
    data['Work Fax Number'] = clean_phone(data['Work Fax Number'])
    data['Home Phone'] = clean_phone(data['Home Phone'])
    data['Home Cellular Phone'] = clean_phone(data['Home Cellular Phone'])
    data['Home Fax Number'] = clean_phone(data['Home Fax Number'])
    data['Home City'] = clean_city(data['Home City'])
    data['Home Province/State'] = clean_states(data['Home Province/State'])
    data['Home Postal Code'] = clean_zips(data['Home Postal Code'])
    data['Work Country'] = clean_countries(data['Work Country'])
    data['Home Country'] = clean_countries(data['Home Country'])
    data['Work Address 1'] = clean_address(data['Work Address 1'])
    data['Work Address 2'] = clean_address(data['Work Address 2'])
    data['Home Address 1'] = clean_address(data['Home Address 1'])
    data['Home Address 2'] = clean_address(data['Home Address 2'])

    # write the data back to file
    write_output_file(data)

if __name__ == "__main__":
    main()
