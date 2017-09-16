#!/bin/python
import config, json, strings
from flask import Flask, request
from slackclient import SlackClient
from watson_developer_cloud import VisualRecognitionV3
from Restaurants import Restaurants
import Restaurant

'''
MAIN BILBOBOT
'''

sc = SlackClient(config.slack_token)
vr = VisualRecognitionV3('2017-09-16',api_key=config.watson_api_key)
app = Flask(__name__)

### === WATSON INTEGRATION ===

@app.route('/doof', methods=['POST'])
def watsonify():
    # process image recognition
    imgurl = request.form["text"]
    res_body = vr.classify(images_url=imgurl)

    print(json.dumps(res_body,indent=2))

    # find the top 2 recognized keywords
    img_recogs = (res_body["images"][0]["classifiers"][0]["classes"])
    first = img_recogs[0]
    second = img_recogs[1]
    for img in img_recogs:
        if img["score"] > first["score"]:
            second = first
            first = img
    top_two = [first['class'],second['class']]
    
    processTopTwo(top_two)
    """
    sc.api_call(
        "chat.postMessage",
        channel="#general",
        text=(strings.watson_found).format(top_two[0],top_two[1]))
    """
    return top_two

# method to process the top 2 results
def processTopTwo(topTwo):
    # search with the keyword
    results.searchRestaurantsWith(topTwo[0])
    # check if enough results
    if (results.checkListLength() == False):
        results.searchRestaurantsWith(topTwo[1])
    # print results to the screen
    output = ""
    for restaurant in results.restaurants():
        output += restaurant.printInfo()
    # send msg to general channel
    sc.api_call("chat.postMessage",
                channel="#general",
                text=output)
     
     

### === MAIN API ENDPOINTS ===

@app.route('/')
def hi():
    return "hi! i'm bilbo"

@app.route('/test', methods=['GET'])
def test():
    sc.api_call(
        "chat.postMessage",
        channel="#random",
        text="my name jeff"
    )

    return "200 OK"

@app.route('/custom/<input>')
def custom(input):
    sc.api_call(
        "chat.postMessage",
        channel="#general",
        text=input
    )

    return "200 OK"


if __name__ == '__main__':
    results = Restaurants()    
    app.run()
    