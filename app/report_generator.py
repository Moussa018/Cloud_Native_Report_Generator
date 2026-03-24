import boto3
import csv 
import json 
import os 
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import io

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    ses = boto3.client('ses')
    data_bucket = os.environ['DATA_BUCKET']
    report_bucket = os.environ['REPORTS_BUCKET']
    email_adress = os.environ['EMAIL_ADDRESS']

    try:

        reponse = s3.get_object(Bucket = data_bucket, Key = 'sales/samples_sales.csv')
        sales_data = reponse['Body'].read().decode('utf-8')

        reponse = s3.get_object(Bucket = data_bucket, Key = 'inventory/samples_data.csv')
        inventory_data = reponse['Body'].read().decode('utf-8')

        report_content = generate_report(sales_data, inventory_data)

        report_key = f"report/daily_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        s3.put_object(
            Bucket = report_bucket,
            Key = report_key,
            Body = report_content,
            ContentType = 'text/csv'
        )

        send_email_report(
            ses,email_adress,report_content,report_key
        )   

        return json.dumps(
            {
            'statusCode': 200,
            'body': f"Report generated successfully: {report_key}"
        }
        )

    except Exception as e :
        print(f'Error generated: {str(e)}')
        return json.dumps({
            'statusCode': 500,
            'body': f"Error generating report: {str(e)}"
        })

def generate_report(sales_data, inventory_data):
    sales_reader = csv.DictReader(io.StringIO(sales_data))
    sales_summary = {}

    for row in sales_reader : 
        product = row['Product']
        sales = int(row['Sales'])
        if product not in sales_summary : 
            sales_summary[product] = 0
        sales_summary[product]+=sales
    inventory_reader  = csv.DictReader(io.StringIO(inventory_data))
    inventory_summary = {}

    for row in inventory_reader :
        product = row['Product']
        stock = int(row['Stock'])
        if product not in inventory_summary:
            inventory_summary[product]=0
        inventory_summary[product]+=stock
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        ['Product','Total Sales','Total Inventory', 'Sales Ratio']
    )

    for product in sales_summary:
        total_sales = sales_summary[product]
        total_inventory = inventory_summary.get(product,0)
        sales_ratio = total_sales/total_inventory if total_inventory > 0 else 0
        writer.writerow(
            [product, total_sales, total_inventory, sales_ratio]
        )
    
    return output.getvalue()

def send_email_report(ses, email_adress, report_content, report_key):
    subject  = f"Daily Business Report - {datetime.now().strftime('%Y-%m-%d')}"
    msg = MIMEMultipart()
    msg['From'] = email_adress
    msg['To'] = email_adress
    msg['Subject'] = subject

    body = f"""
    Dear Team,
    
    Please find attached the daily business report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.
    
    Bonjour
    
    Le rapport a été généré et stocké dans S3 : {report_key}
    """
    msg.attach(MIMEText(body, 'plain'))

    ses.send_raw_email(
        Source = email_adress,
        Destinations= [email_adress],
        RawMessage = {'Data': msg.as_string()}
    )
