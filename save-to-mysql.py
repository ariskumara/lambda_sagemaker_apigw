import pymysql
import sys
 
AWSRegionName = '<replace with your region>'
 
# Create a connection object
dbServerName = "<replace with your DB Server instance name>"
dbUser = "<your DB user>"
dbPassword = "<your DB password>"
dbName = "<your DB name>"
 
def lambda_handler(event, context):
    print("save prediction to mysql function is called!")
    try:
        timestamp = str(event["Timestamp"])
        orangutanId = str(event["OrangutanID"])
        orangutanName = str(event["OrangutanName"])
        confidence = str(event["Confidence"])
        bucket = str(event["Bucket"])
        filename = str(event["Filename"])
        
        print(timestamp)
        print(orangutanId)
        print(orangutanName)
        print(confidence)
        print(bucket)
        print(filename)
        
        try:
            print("connecting to mysql rds!")
            connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,
            db=dbName, connect_timeout=5)
            # Create a cursor object
            cursorObject = connectionObject.cursor()
            # Insert rows into the MySQL Table
            print("inserting records in _orangutan table!")
            insertStatement = "INSERT INTO <table_name> (timestamp, orangutan_id, orangutan_name, confidence, bucket_name, filename) VALUES (\"" + timestamp + "\",\"" + orangutanId + "\", \"" + orangutanName + "\", \"" + confidence + "\", \"" + bucket + "\", \"" + filename + "\")"
            cursorObject.execute(insertStatement)
            connectionObject.commit()
            # SQL Query to retrive the rows
            sqlQuery = "select * from <table_name>"
            #Fetch all the rows - for the SQL Query
            cursorObject.execute(sqlQuery)
            rows = cursorObject.fetchall()
            for row in rows:
                print("printing data from mysql rds instance!")
                print(row)
        except Exception as e:
            print(str(e))
            sys.exit()
        finally:
            connectionObject.close()
    except Exception as e:
        print(str(e))
        
        # TODO implement
    #message = "Hello {} {}!".format(event["OrangutanID"], event["OrangutanName"])  
    #print(message)
    #return { 
    #    'message' : message
    #}