import urllib.request
import json

# name=input("Enter username: ")
name="UCSHVH_AWVUc-C8-D8mh8W6A"
key = "AIzaSyCQ2cEg3s_1ahHpikqqoPwrTRFBKQB-zFU"

data= urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id="+name+"&key="+key).read()
subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]

print(name+" has "+"{:,d}".format(int(subs))+ " subscribers")

