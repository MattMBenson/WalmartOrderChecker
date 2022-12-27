import requests

def importData():
    with open('OrderNumbers.txt') as f:
        numbers = [line.rstrip() for line in f]
    return numbers

def checkOrderNumber(number):
    processing = "Items processing"
    can = "Cancelled"
    one_dot = "Placed"

    lookup_url = f"https://www.walmart.ca/api/order-tracking-page/flatorders?orderNo={number}&tz=-300"

    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'wm_qos.correlation_id': '16b8d6a5-02b-18540576c76a5e,16b8d6a5-02b-18540576c76e5a,16b8d6a5-02b-18540576c76e5a',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6,2 Mobile/15E148 Safari/604.1',
        'referer': f'https://www.walmart.ca/track-order-mobile-app?sellerName=Walmart&orderNo={number}',
        'accept-language': 'en-CA,en-US;q=0.9,en;q=0.8'
    }
    try:
        r = requests.get(lookup_url, timeout=5, headers=headers)
    except requests.exceptions.Timeout:
        print("Attempting to retry url..")
        r = requests.get(lookup_url, timeout=5, headers=headers)
    except requests.exceptions.TooManyRedirects:
        print(f"Bad URL/Order Number - Review: {number}")
    except requests.exceptions.RequestException as e:
        print("Unforseen error, bail and retry later.")
        raise SystemExit(e)

    try:
        decoded_data = r.text.encode().decode('utf-8-sig')
    except Exception as e:
        print(e, "Unable to decode")

    # search for 3 dot
    if processing in decoded_data:
        print(f"Order Number: {number} | Item Processing. (3 dot)")
    elif can in decoded_data:
        print(f"Order Number: {number} | Cancelled. ")
    elif one_dot in decoded_data and can not in decoded_data:
        print(f"Order Number: {number} | Order Placed (1 Dot)")
    else:
        print(f"Order Number: {number} | Unable to find ... check order number")

orderNumbers = importData()

#for ordernum in orderNumbers:
#    checkOrderNumber(ordernum)
