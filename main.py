import urllib.request
import json
import lob
import time

def main():
    lob.api_key = "test_5416711ed6678f2147f6a8fdd6c125a03a3"
    name = str(input("From Name: "))
    address1 = str(input("From Address Line 1: "))
    address2 = str(input("From Address Line 2: "))
    city = str(input("From City: "))
    state = str(input("From State: "))
    zipCode = str(input("From Zip Code: "))
    message = str(input("Message: "))

    # Makes sure the message is 200 words or less, as per the spec.
    while len(message.split()) > 200:
        print("Please empty a message 200 words or less.")
        message = str(input("Message: "))

    # Builds up the URL to get information from google
    civicUrl = "https://www.googleapis.com/civicinfo/v2/representatives" + "?address=" + address1.replace(" ", "+") + \
                           "&roles=legislatorUpperBody&fields=officials(address%2Cname)&key=AIzaSyB0kTM1hWRbDCyhdfKuYM9ao6nngCW00Z0"

    # Checks if the information can be obtained
    try:
        response = urllib.request.urlopen(civicUrl)
        print("Obtaining civic information.")
    except:
        print("Invalid Address. Please try again.")
        return

    # Parses the json file into a python dictionary
    data = json.loads(response.read().decode('utf-8'))
    official = data["officials"][0]
    legislator_name = official['name']
    legislator_address = official['address']
    legislator_address = legislator_address[0]
    legislator_city = legislator_address['city']
    legislator_zip = legislator_address['zip']
    legislator_state = legislator_address['state']
    legislator_line = legislator_address['line1']

    # Tries to create a letter with the Lob API
    try:
        letter = lob.Letter.create(
            description = "Legislature Challenge",
            to_address = {
                'name': legislator_name,
                'address_line1': legislator_line,
                'address_city': legislator_city,
                'address_state': legislator_state,
                'address_zip': legislator_zip,
                'address_country': 'US'
            },
            from_address= {
                'name': name,
                'address_line1': address1 + " " + address2,
                'address_city': city,
                'address_state': state,
                'address_zip': zipCode,
                'address_country': 'US'
            },
            file = """<html><head><meta charset="UTF-8"><link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css"><title>Lob Coding Challenge</title><style>*, *:before, *:after{-webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box;}body{width: 8.5in; height: 11in; margin: 0; padding: 0;}.page{page-break-after: always;}.page-content{position: relative; width: 8.125in; height: 10.625in; left: 0.1875in; top: 0.1875in;}.text{position: relative; left: 40px; top: 40px; width: 6in; font-family: sans-serif; font-size: 16px;}#return-address-window{position: absolute; left: .625in; top: .5in; width: 3.25in; height: .875in;}#return-address-text{position: absolute; left: .07in; top: .34in; width: 2.05in; height: .44in; background-color: white; font-size: .11in;}#return-logo{position: absolute; left: .07in; top: .02in; width: 2.05in; height: .3in; background-color: white;}#recipient-address-window{position: absolute; left: .625in; top: 1.75in; width: 4in; height: 1in;}#recipient-address-text{position: absolute; left: .07in; top: .05in; width: 2.92in; height: .9in; background-color: white;}</style></head><body> <div class="page"> <div class="page-content"> <div class="text" style="top: 4in">{{message}}</div></div><div id="return-address-window"> <div id="return-address-text"> </div></div><div id="recipient-address-window"> <div id="recipient-address-text"> </div></div></div></body></html>""",
            data = {
                'message': message
            },
            color = False
        )
        print("Processing with Lob.")
    except:
        print("There was an error with Lob, please try again.")
        return

    jsonLetter = json.loads(str(letter))
    # Gets the URL of the letter on Lob's servers
    lobLetterURL = jsonLetter["url"]

    # Tries to save the file locally
    try:
        # Sleeps for 2 seconds, because an instant request will almost always fail
        time.sleep(2)
        print("Saving pdf locally as Letter.pdf")
        urllib.request.urlretrieve(lobLetterURL, "Letter.pdf")
        print("Saved.")
    except:
        # Tries to save 1 more time before asking the user to retry
        try:
            print("There was an error saving, retrying.")
            print("Saving pdf locally as Letter.pdf")
            urllib.request.urlretrieve(lobLetterURL, "Letter.pdf")
            print("Saved.")
        except:
            print("There was an error when saving, please try again.")
            return

if __name__ == "__main__":
    main()