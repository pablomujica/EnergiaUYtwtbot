def percentage(part: int, whole: int) -> str: 
    value = 100 * float(part)/float(whole)
    return f'{str(abs(round(value,2)))}%'

def build_hourly_tweet(apiResponse: dict, exchange: dict) -> str:
    total = 0
    for origin in apiResponse['production'].keys():
        total+= apiResponse['production'][origin]
    total+= exchange['netFlow']
    tweet = (f'En este momento, el origen de la energía utilizada en #Uruguay es:\n' +
             f'#HydroelectricEnergy 🌊: {apiResponse["production"]["hydro"]} MW {percentage(apiResponse["production"]["hydro"], total)} \n' +
             f'#WindEnergy 💨: {apiResponse["production"]["wind"]} MW {percentage(apiResponse["production"]["wind"], total)} \n' +
             f'#SolarEnergy 🌞: {apiResponse["production"]["solar"]} MW {percentage(apiResponse["production"]["solar"], total)} \n' +
             f'#Biomass 🪓: {apiResponse["production"]["biomass"]} MW {percentage(apiResponse["production"]["biomass"], total)} \n' +
             f'#Oil 🛢: {apiResponse["production"]["oil"]} MW  {percentage(apiResponse["production"]["oil"], total)} \n')
    if exchange['netFlow'] > 0.0:
        tweet+= f'#Brasil 🇧🇷 import: {str(exchange["netFlow"])} MW {percentage(exchange["netFlow"], total)} \n'
    elif exchange['netFlow'] == 0.0:
        pass
    else:
        tweet+= f'#Brasil 🇧🇷 export: {str(abs(exchange["netFlow"]))} MW {percentage(exchange["netFlow"], total)} \n'
    tweet+= f'#UTE #RenewableEnergy'
    return tweet

if __name__ == '__main__':
    from uy import fetch_production, fetch_exchange
    from pprint import pprint
    production = fetch_production()
    exchange = fetch_exchange('UY', 'BR')
    pprint('---------- Testing -0.0 netFlow ----------')
    exchange['netFlow'] = -0.0
    tweet = build_hourly_tweet(production, exchange)
    pprint(tweet)
    pprint(len(tweet))
    pprint('---------- Testing -1.0 netFlow ----------')
    exchange['netFlow'] = -1.0
    tweet = build_hourly_tweet(production, exchange)
    pprint(tweet)
    pprint(len(tweet))
    pprint('---------- Testing 2.0 netFlow ----------')
    exchange['netFlow'] = 2.0
    tweet = build_hourly_tweet(production, exchange)
    pprint(tweet)
    pprint(f'Lenght {str(len(tweet))}')