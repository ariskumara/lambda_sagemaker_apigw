import pymysql
import sys

#define AWS Region
AWSRegionName = '<region>'
 
# Create a connection object
dbServerName = "<db instance>"
dbUser = "<db user>"
dbPassword = "<db password>"
dbName = "<db name>"

def lambda_handler(event, context):
    # TODO implement
    rows = ""
    
    #default table and headings (Added Aris, 17 Aug 2019)
    html='<html><head><title>Ini Judul</title></head><body><h1><img src=gambar'
    html += 'Face Recognition v0.1</h1><table border=1>'
    html += '<th>Timestamp</th><th>Predicted Orangutan ID</th><th>Predicted Orangutan Name</th><th>Predicted Confidence</th><th>Bucket Name</th><th>Filename</th><th>Thumbnail Image</th>'
    
    
    try:
        print("connecting to mysql rds!")
        connectionObject = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,
        db=dbName, connect_timeout=5)
        # Create a cursor object
        cursorObject = connectionObject.cursor()
        # SQL Query to retrive the rows
        sqlQuery = "select * from table_name"
        #Fetch all the rows - for the SQL Query
        cursorObject.execute(sqlQuery)
        rows = cursorObject.fetchall()
        print("printing data from mysql rds instance!")
        #print values on rows
        for row in rows:
            html = html + '<tr><td>' + row[0] + '</td><td>' + row[1] + '</td><td>' + row[2] + '</td><td>' + row[3] + '</td><td>' + row[4] + '</td><td>' + row[5] + '</td><td>' + '<img src=https://s3-wwf-storage-gatewayresized.s3-ap-northeast-1.amazonaws.com/' + row[5] + '><br><a href=https://s3-wwf-storage-gatewayresized.s3-ap-northeast-1.amazonaws.com/preview.html?edited_' + row[5] + ' target=_blank>See Detailed Image</a></td></tr>'
    except Exception as e:
        print(str(e))
        sys.exit()
    finally:
        connectionObject.close()

    html = html + '</table><br>Technology Stack: Amazon S3, Amazon SageMaker, AWS Lambda, Amazon API Gateway'
    html += '<br><b>Copyright  2019</body></html>'
    return {
    "body": html
    }
