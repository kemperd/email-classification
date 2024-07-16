import requests
import re
import csv
import pandas as pd

# Dummy email list, replace this with reading email addresses from as CSV as follows:
#df = pd.read_csv('input.csv', sep=';')
#email_list = df['Email_address'].unique()

email_list = [ 'nonexistent@gmail.com', 'nonexistent@hotmail.com', 'nonexistent@philips.com', 'nonexistent@accenture.com',
              'nonexistent@utwente.nl', 'nonexistent@chello.nl', 'nonexistent@gmx.de', 'nonexistent@umich.edu', 'nonexistent@yahoo.com' ]

data_output = []

def process_address(address):
    response = requests.post("http://127.0.0.1:8000/predict", json={
        "input": 4.0, 
        "text":"Please assist in classifying email addresses as being from a personal email provider. You can identify personal email providers by their domain names. Please answer with YES when the email address is from a personal email provider or NO if it is another type of address like a small business or corporate address. A country-specific top level domain does not imply the address is a personal email address. If you answered YES, specify why the address is classified as being from a personal email provider. Only look at the domain names and not the usernames. If an address is from an Internet Service Provider (ISP), also classify it as YES. Now please classify the following address: {}".format(address)
    })
    # Parse the response text. There are some assumptions here with regards to the formatting
    # which are working because we are using the Mistral 7B model which does not really vary
    # the response that much. If using another model this will probably need to be updated.
    txt_search = re.search('{}(.*)'.format(address), response.text)
    if txt_search:        
        full_line = txt_search.group(1).replace(r'\n', '')

        full_line_split = full_line.split(' ', 1)
        outcome = full_line_split[0].replace('.', '')
        outcome = full_line_split[0].replace(',', '')
        if 'YES' in outcome:
            outcome = 'YES'
        elif 'NO' in outcome:
            outcome = 'NO'
        else:
            outcome = 'UNKNOWN'
        expl = full_line_split[1]

        print('{}: {} - {}'.format(address, outcome, expl))
        data_output.append([address, outcome, expl])

# Main loop
for address in email_list:
   process_address(address)

# Write collected addresses to file
df_output = pd.DataFrame(data_output, columns = ['Email', 'Outcome', 'Explanation'])
df_output.to_csv('output.csv')