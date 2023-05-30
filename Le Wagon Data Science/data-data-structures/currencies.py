# pylint: disable=missing-docstring

# TODO: add some currency rates
RATES = {
    "USDEUR": 0.85,
    "GBPEUR": 1.13,
    "CHFEUR": 0.86,
    "EURGBP": 0.885
    # Add more rates as necessary
}

def convert(amount, currency):
    """returns the converted amount in the given currency
    amount is a tuple like (100, "EUR")
    currency is a string
    """
    a = amount[1] + currency
    print(a)
    if a not in RATES.keys():
        return None

    rate = RATES[a]
    converted_amount = amount[0] * rate
    rounded_amount = round(converted_amount, 1)
    return rounded_amount
