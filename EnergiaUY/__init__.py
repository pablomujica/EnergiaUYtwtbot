import datetime
import logging
import os
from shared_code.uy import fetch_production, fetch_exchange
from shared_code.auxiliary import build_hourly_tweet
import tweepy

import azure.functions as func

auth = tweepy.OAuthHandler(os.environ["TWTApiKey"], os.environ["TWTApiKeySecret"])
auth.set_access_token(os.environ["TWTAccessToken"], os.environ["TWTAccessTokenSecret"])
api = tweepy.API(auth)

def main(mytimer: func.TimerRequest, msg: func.Out[str]) -> None:
    logging.info(mytimer)
    utc_timestamp = datetime.datetime.utcnow().replace(
                        tzinfo=datetime.timezone.utc
                    ).isoformat()
    
    try:
        logging.info("Auth OK")
        production = fetch_production()
        exchange = fetch_exchange('UY', 'BR')

        logging.info(production['production'])
        
        tweet = build_hourly_tweet(production, exchange)

        logging.info(tweet)
        if len(tweet) <= 280:
            logging.info(f'Tweet lenght: {str(len(tweet))}')
        else:
            logging.error(f'Tweet lenght: {str(len(tweet))}')

        if exchange['netFlow'] > 0:
            logging.info("Importing energy from brasil")
        else:
            logging.info("Not importing energy from brasil")
        
        api.update_status(status=tweet)
        # Write log to storage queue
        try:
            msg.set(
                (f'tweet=hourly,' +
                f'lenght={len(tweet)},' +
                f'hydro={production["production"]["hydro"]},' +
                f'wind={production["production"]["hydro"]},' +
                f'solar={production["production"]["hydro"]},' +
                f'biomass={production["production"]["hydro"]},' +
                f'oil={production["production"]["hydro"]},' +
                f'br={exchange["netFlow"]}')
            )
        except Exception as e:
            logging.error(e)
    except Exception as e:
        logging.error(e)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    return 
