import os
import twitter
import schedule
import json
import time
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

speed =float(os.environ.get("speed"))
interval = int(os.environ.get("interval"))
my_consumer_key = os.environ.get("my_consumer_key")
my_consumer_secret = os.environ.get("my_consumer_secret")
my_access_token_key = os.environ.get("my_access_token_key")
my_access_token_secret = os.environ.get("my_access_token_secret")

def job():
    print "executing .. "

    jstring = os.popen("speedtest-cli --json --server 2021").read()
    if "ERROR" not in jstring:
        try:
            api = twitter.Api(consumer_key=my_consumer_key,consumer_secret=my_consumer_secret,access_token_key=my_access_token_key,access_token_secret=my_access_token_secret)
            data = json.loads(jstring)
            upload_speed =str(data["upload"]/1000000)
            download_speed = str(data["download"]/1000000)
            latency = str(data["server"]["latency"])
        
            if data["download"]/1000000 < speed: ## tweet if speed is less than expected
                status = api.PostUpdate("my speed is sloooooow "+ download_speed[:5]  +" mbps @zuku_wecare A/c 104793 ... cc @kmarima")
            else: ## tweet if everything os ok
                status = api.PostUpdate("My speed is ok "+ download_speed[:5] + "mbps")
        except Exception as e:
            pass
        
schedule.every(interval).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)