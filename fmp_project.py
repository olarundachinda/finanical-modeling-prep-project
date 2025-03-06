import datetime
import pprint
import statistics
import urllib
import requests

def getEndpoint(endpoint, parameters):
    baseUrl = f"https://financialmodelingprep.com/api"

    endpointUrl = f"{baseUrl}/{endpoint}"

    parameters['apikey'] = "api_key"
    headers = {}
    payload = {}

    print("Getting Endpoint: " + endpointUrl + "?" + urllib.parse.urlencode(parameters))
    response = requests.request("GET", endpointUrl, headers=headers, data=payload, params=parameters)
    response_data = response.json()
    return response_data

# IS 352 Exercises – Apple
# 1.	Connect to Financial Modeling Prep and download a company profile for AAPL.
print("1. Connect to Financial Modeling Prep and download a company profile for AAPL.")
# {version}/{method}/{ticker}
# Set version, method, and ticker
version = "v3"
method = "profile"
ticker = "AAPL"
endpoint = f"{version}/{method}/{ticker}"
parameters = {} # if we don't have a dictionary we can just use an empty one

# Download the data
profile_response = getEndpoint(endpoint, parameters)
profile_response = profile_response[0]
# pprint.pprint(profile_response)

# a.	Report the CEO of a description of the company.
print("\t a.	Report the CEO a description of the company.")
# Find the CEO key in the dictionary and print
profile_ceo = profile_response["ceo"]
profile_desc = profile_response["description"]
print("\t\tCEO:", profile_ceo)
print("\t\tDescription: ", profile_desc)


# b.	Market Capitalization, share price and number of outstanding shares (outstanding shares = market capitalization / share price).
print("\t b.	Market Capitalization, share price and number of outstanding shares (outstanding shares = market capitalization / share price).")
# Find market capitalization and share price
profile_marketcapitalization = profile_response["mktCap"]
profile_shareprice = profile_response["price"]
# Divide to get outstanding shares and print results
profile_outstandingshares = profile_marketcapitalization / profile_shareprice
print("\t\tMarket Capitalization:",profile_marketcapitalization)
print("\t\tShare Price:", profile_shareprice)
print("\t\tOutstanding Shares:", profile_outstandingshares)

# c.	Report the high and low of the stock price range.
print("\t c. Report the high and low of the stock price range.")
# Find the range, high and low, and change to floats
profile_range = profile_response['range']
profile_high = float(profile_range[profile_range.find("-")+1:])
profile_low = float(profile_range[:profile_range.find("-")])
# Print results
print("\t\tProfile Range:", profile_range)
print("\t\tProfile High:", profile_high)
print("\t\tProfile Low:", profile_low)
print("\t\tProfile High-Low:", profile_high-profile_low)

# d.	Report the number of full time employees.
print("\t d. Report the number of full time employees.")
# Find the number of full time employees
profile_fulltimeemployees = profile_response["fullTimeEmployees"]
# Print the results
print("\t\tNumber of Full Time Employees:", profile_fulltimeemployees)

# 2.	Connect to Financial Modeling Prep and download the most recent income statement for AAPL.
print("2.	Connect to Financial Modeling Prep and download the most recent income statement for AAPL.")
# https://financialmodelingprep.com/api/v3/income-statement/AAPL
# Set version, method, and ticker
version = "v3"
method = "income-statement"
ticker = "AAPL"
endpoint = f"{version}/{method}/{ticker}"
parameters = {}

# Download the data
incomestatement_response = getEndpoint(endpoint, parameters)
incomestatement_response = incomestatement_response[0]
# pprint.pprint(incomestatement_response)

# a.	Report the date of the most recent income statement.
print("\t a.	Report the date of the most recent income statement.")
# Find the date
date = incomestatement_response["date"]
# Print the results
print("\t\tDate:", date)

# b.	Calculate and report productivity (productivity = revenues / full time employees.
print("\t b.	Calculate and report productivity (productivity = revenues / full time employees.")
# Find revenue and full time employees
revenues = incomestatement_response["revenue"]
fulltimeemp = profile_fulltimeemployees
# Divide to get productivity
productivity = revenues/int(profile_fulltimeemployees)
# Print the results
print("\t\tProductivity:", productivity)

# c.	Calculate and report preferred dividends (preferred dividends = net income - (eps * weighted average shares outstanding).
print("\t c.	Calculate and report preferred dividends (preferred dividends = net income - (eps * weighted average shares outstanding).")
# Find the net income, earnings per share, and weighted average shares outstanding
net_income = incomestatement_response["netIncome"]
eps = incomestatement_response["eps"]
waso = incomestatement_response["weightedAverageShsOut"]
# Perform operations to fund preferred dividends
pref_div = net_income - (eps * waso)
# Print the results
print("\t\tPreferred Dividends:", pref_div)

# 3.	Download the daily stock prices for AAPL since March 1st.
print("3.	Download the daily stock prices for AAPL since March 1st.")
# https://financialmodelingprep.com/api/v3/historical-price-full/AAPL
# Set version, method, and ticker
version = "v3"
method = "historical-price-full"
ticker = "AAPL"
endpoint = f"{version}/{method}/{ticker}"
parameters = { # can be manipulated to give values that we want
    "to": "2024-04-10",
    "from": "2024-03-01"
}

# Download the data
dailystock_response = getEndpoint(endpoint, parameters)
dailystock_response = dailystock_response["historical"]
dailystock_response = dailystock_response[:15] # used to skip for a 15-day period
# pprint.pprint(dailystock_response)

# a. For each of the last 15 days report: Date, open, close, volume
# Use a for lop to run through each value in the dictionary
print("\t a. For each of the last 15 days report: Date, open, close, volume")
for day_index, day_dictionary in enumerate(dailystock_response):
    # a.    For each of the last 15 days report: Date, open, close, volume
    # Find the date, open, close, and volume and print the results
    print("\t\tDate:", day_dictionary["date"])
    print("\t\tOpen:", day_dictionary["open"])
    print("\t\tClose:", day_dictionary["close"])
    print("\t\tVolume:", day_dictionary["volume"])
    print()

# b.	Create a list of change values and report the average change
print("\t b.	Create a list of change values and report the average change")
# Create an empty list for the change values
change_values = []
# Use a for lop to run through each value in the dictionary
for day_index, day_dictionary in enumerate(dailystock_response):
    # Extract the change values and append to the empty list
    change_values.append(float(day_dictionary["change"]))
# Print the results
print("\t\tAverage Change:", statistics.mean(change_values))

# c.	Create a list of volume values and report the average volume
print("\t c.	Create a list of volume values and report the average volume")
# Create an empty list for the volume values
volume_values = []
# Use a for lop to run through each value in the dictionary
for day_index, day_dictionary in enumerate(dailystock_response):
    # Extract the volume values and append to the empty list
    volume_values.append(float(day_dictionary["volume"]))
# Print the results
print("\t\tAverage volume:", statistics.mean(volume_values))


# d.	Create a list of dates as day number (x) (Note: datetime.datetime.strptime(daily_stock_data['date'], "%Y-%m-%d").timetuple().tm_yday
print("\td.	Create a list of dates as day number (x) (Note: datetime.datetime.strptime(daily_stock_data['date'], \"%Y-%m-%d\").timetuple().tm_yday")
# Create an empty list for the x and y values
x_values = []
y_values = []
volume_values = []
# Use a for lop to run through each value in the dictionary
for day_index, day_dictionary in enumerate(dailystock_response):
    # Extract the date values and append to the empty x values list
    x_values.append(datetime.datetime.strptime(day_dictionary['date'], "%Y-%m-%d").timetuple().tm_yday)
    # Extract the open values and append to the empty y values list
    y_values.append(day_dictionary['open'])
# Print the results
print("\t\tX Values:", x_values)
print("\t\tY Values:", y_values)
print("\t\tLinear regression:", statistics.linear_regression(x_values,y_values,))


# Extra Credit
# 4.	Apple is a part of the FAANG group. Create a list of tickers representing the full group (META, AAPL, AMZN, NFLX GOOG) and report the market capitalization and # of employees for each
print()
print("Extra Credit: Apple is a part of the FAANG group. Create a list of tickers representing the full group (META, AAPL, AMZN, NFLX GOOG), and report the market capitalization and # of employees for each")
# Create a list of the tickers
companies = ["META", "AAPL", "AMZN", "MSFT", "GOOG"]

# Connect to Financial Modeling Prep and download a company profile for company in a for loop and present the results. {version}/{method}/{ticker}
# Set version, method, and ticker
for i in companies:
    version = "v3"
    method = "profile"
    ticker = i
    endpoint = f"{version}/{method}/{ticker}"
    parameters = {}

    # Download the data
    profile_response = getEndpoint(endpoint, parameters)
    profile_response = profile_response[0]
    # pprint.pprint(profile_response)

    # Report the market capitalization and numbers of employees for each
    profile_marketcapitalization = profile_response["mktCap"]
    profile_fulltimeemployees = profile_response["fullTimeEmployees"]
    # Print the results
    print("\t", i, ":")
    print("\t\tMarket Capitalization:", profile_marketcapitalization)
    print("\t\tNumber of Full Time Employees:", profile_fulltimeemployees)
    print()