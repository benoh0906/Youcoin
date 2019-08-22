import models
import urllib.request
import json

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

api=Blueprint('api','api',url_prefix="/api/v1")

#list youcoins
@api.route('/', methods=["GET"])
def get_all_youcoins():
    payload = request.get_json() #on postman, i used {"user":1}, which is the user primary id
    print(type(payload),"<-type of payload")

    key = "AIzaSyCQ2cEg3s_1ahHpikqqoPwrTRFBKQB-zFU"
    
    try:
        youcoins=[model_to_dict(youcoin) for youcoin in models.Youcoin.select().where(models.Youcoin.user == int(payload["user"]))]
        for data in youcoins:
            dataId=data['id']
            dataSN=data['startingNum']
            name=data["channelId"]
            data= urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id="+name+"&key="+key).read()
            subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
            
            query = models.Youcoin.update(currentNum=int(subs), profit=(int(subs)-dataSN)).where((models.Youcoin.user == int(payload["user"])) & (models.Youcoin.id==dataId))
            query.execute()

            models.Stat.create(youcoin=dataId, currentSubs=subs)
            stat=[model_to_dict(stat) for stat in models.Stat.select()]
            print(len(stat),"<-num of stat")
        
        return jsonify(data=youcoins,status={"code":200,"message":"success"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code":401, "message":"There was an error getting the resource"})


#create youcoin
@api.route('/', methods = ["POST"])
def create_youcoins():
    payload = request.get_json()
    
    user = models.User.get(models.User.username== payload['username'])
    
    key = "AIzaSyCQ2cEg3s_1ahHpikqqoPwrTRFBKQB-zFU"
    url=payload["channelUrl"]
    
    for i in range(len(url)):
        if url[i:i+8]=="channel/":
            name=url[i+8:]

    data= urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id="+name+"&key="+key).read()
    subs = json.loads(data)["items"][0]["statistics"]["subscriberCount"]
    title = json.loads(data)["items"][0]["snippet"]["title"]
    youcoin = models.Youcoin.create(
        user=user.id, 
        channelUrl=payload['channelUrl'],
        channelTitle= title,
        channelId = name,
        startingNum = int(subs),
        currentNum = int(subs),
        profit = 0
        )


    you_dict = model_to_dict(youcoin)

    return jsonify(data = you_dict, status={"code":281,"message":"Success"})

#delete youcoin
@api.route('/<id>', methods=["DELETE"])
def delete_youcoin(id):
    

    # print(type(models.User.get(models.User.id==1)),'<-user type') #model
    coin = model_to_dict(models.Youcoin.get(models.Youcoin.id==id))
    print(coin,"<-coin")
    coinUser=coin['user']['id']
    print(coinUser,'<-coinUser')
    coinProfit=coin['profit']
    user = model_to_dict(models.User.get(models.User.id==coinUser))

    profit = user["profit"]
    
    profitUpdate = models.User.update(profit=profit+coinProfit).where((models.User.id == coinUser))
    profitUpdate.execute()

    query = models.Youcoin.delete().where(models.Youcoin.id == id)
    query.execute()

    return jsonify(data='resources successfully deleted', status={"code":200, "message":"deleted"})
