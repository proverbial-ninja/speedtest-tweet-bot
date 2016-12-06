import os
import twitter
import schedule
import json
import time

speed = 3.3 #
interval = 10 #minutes
my_consumer_key = "YOUR TWITTER CONSUMER KEY"
my_consumer_secret = "YOUR TWITTER CONSUMER SECRET"
my_access_token_key = "YOUR TWITTER ACCESS TOKEN KEY"
my_access_token_secret = "YOUR TWITTER ACCESS TOKEN SECRET"

def job():
    print "executing .. "

    jstring = os.popen("speedtest-cli --json --server 2021").read()
    if "ERROR" not in jstring:
        api = twitter.Api(consumer_key=my_consumer_key,consumer_secret=my_consumer_secret,access_token_key=my_access_token_key,access_token_secret=my_access_token_secret)
        data = json.loads(jstring)
        upload_speed =str(data["upload"]/1000000)
        download_speed = str(data["download"]/1000000)
        latency = str(data["server"]["latency"])
        
        if data["download"]/1000000 < speed: ## tweet if speed is less than expected
            status = api.PostUpdate("my speed is "+ download_speed[:3]  +"mbps  ")
        else: ## tweet if everything os ok
            status = api.PostUpdate("My speed is "+ download_speed[:3]  +"mbps  My latency is "+ latency )
schedule.every(interval).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)