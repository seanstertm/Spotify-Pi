import sys
import time
import requests

route = 152
stop = 12472

prevTime = ""
nowTime = ""

try:
    while True:
        try:
            response = requests.get(f"http://ctabustracker.com/bustime/api/v2/getpredictions?key=Yr9nbHrDBVbxtdC4j8BTw5R3z&rt={route}&stpid={stop}&format=json")
            bus_json = response.json()
            if "error" in bus_json['bustime-response']:
                nowTime = "No busses in the next 30 minutes"
            else: 
                nowTime = bus_json['bustime-response']['prd'][0]['prdctdn']
            if prevTime != nowTime:
                break
            prevTime = nowTime
            time.sleep(5)
        except Exception as e:
            time.sleep(1)
except KeyboardInterrupt:
    print("stopping...")
    sys.exit(0)