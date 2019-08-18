import boto3
import os
import io
import json
import csv
import base64
import time
from datetime import datetime

# grab environment variables
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']

def lambda_handler(event, context):
    # TODO implement
    print('I am being triggered!')
    print(ENDPOINT_NAME)
    
    object_categories = ['orangutan1','orangutan2','orangutan3','orangutan4','orangutan5','orangutan6','orangutan7','orangutan8','orangutan9']
    
    s3 = boto3.client("s3")
    
    if event:
        print("Event: ", event)
        fileObj = event["Records"][0]
        filename = str(fileObj['s3']['object']['key'])
        print("filename: ", filename)
    
    print('start delay 15 secs')
    time.sleep(15)
    print('after delay 15 secs')
    bucket = '<replace with your bucket name>'
    filepath = '/tmp/' + filename
    s3.download_file(bucket, filename,filepath)
    print(bucket)
    print(filepath)
    with open(filepath, 'rb') as f:
        payload = f.read()
        payload = bytearray(payload)

    client = boto3.client('sagemaker-runtime')
    response = client.invoke_endpoint(EndpointName=ENDPOINT_NAME, 
                                   ContentType='application/x-image', 
                                   Body=payload)

    result = response['Body'].read()
    result = json.loads(result)
    print(result)
    predictions = [prediction for prediction in result['prediction'] if prediction[1] > .1]
    print("predictions are: " + str(predictions))
   
    orangutan_id=str(predictions[0][0])
    confidence = str(predictions[0][1])
    print("orangutan ID is " + orangutan_id + " and prediction is " + confidence)
    orangutan_name = object_categories[int(float(orangutan_id))]
    print("orangutan name is " + str(orangutan_name))
    
    
    #get current date and time (added by Aris, 17 Aug 2019)
    timestamp = time.time()
    dt_object = datetime.fromtimestamp(timestamp)
    
    #create JSON object
    data = {}
    data["Timestamp"] = str(dt_object)
    data["OrangutanID"] = str(int(float(orangutan_id)))
    data["OrangutanName"] = str(orangutan_name)
    data["Confidence"] = str(confidence)
    data["Bucket"] = bucket
    data["Filename"] = filename
    
    #add additional column for bounding box (added by Ivan 15-AUG-2019)
    data["XMin"] = str(predictions[0][2])
    data["YMin"] = str(predictions[0][3])
    data["XMax"] = str(predictions[0][4])
    data["YMax"] = str(predictions[0][5])
    
    #invoke another lambda that is located in ap-northeast-1
    invokeLam = boto3.client("lambda",region_name="<replace with your AWS Region>")
    
    #invoke lambda for mysql saving
    resp=invokeLam.invoke(FunctionName="<replace with your function>", InvocationType="Event", Payload=json.dumps(data))
    
    #invoke image bounding box lambda (added by Ivan 15-AUG-2019)
    resp2=invokeLam.invoke(FunctionName="<replace with your function>", InvocationType="Event", Payload=json.dumps(data))
    
    #invoke create thumbnail function (added by Aris 17-AUG-2019)
    resp3=invokeLam.invoke(FunctionName="<replace with your function>", InvocationType="Event", Payload=json.dumps(data))
    
    
    print(json.dumps(data))
    print(resp)
    print(resp2)
    print(resp3)
    print("Calling successful")
    
    return 'Thanks!'
