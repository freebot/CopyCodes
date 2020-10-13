import boto3
import csv

def lambda_handler(event, context):
    region='us-east-1'
    recList=[]
    try:            
        s3=boto3.client('s3')            
        dyndb = boto3.client('dynamodb', region_name=region)
        confile= s3.get_object(Bucket='archivoscsv', Key='codigos.csv')
        recList = confile['Body'].read().decode("utf-8").split('\n')
        print(recList)
        firstrecord=True
        csv_reader = csv.reader(recList, delimiter=',')
        for row in csv_reader:
            sku = row[0]      
            codigo = row[1]
            response = dyndb.put_item(
                TableName='CodigosCI',
                Item={
                'SKU' : {'S':sku},
                'CODIGO': {'S':codigo}
                }
            )
        print('Put succeeded:')
    except Exception as e:
        print (str(e))
