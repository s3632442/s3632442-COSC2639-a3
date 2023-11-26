import boto3
from datetime import datetime
import uuid
from DBops import *

# Assuming you have these variables defined
bucket_name = "retroideal-member-vehicle-images"
pending_images_folder = "pending-vehicle-images"
vehicle_image_table = "retroideal-vehicle-image-table"

def upload_image_to_s3(file, user_id, vehicle_id):
    s3 = boto3.client('s3')
    try:
        unique_filename = str(uuid.uuid4())
        filename = f"{unique_filename}.jpg"

        s3.upload_fileobj(file, bucket_name, f"{pending_images_folder}/{filename}")

        image_url = f"https://{bucket_name}.s3.amazonaws.com/{pending_images_folder}/{filename}"
        status = "pending"
        purpose = str(datetime.now())
        image_id = str(uuid.uuid4())
        
        add_entry_to_vehicle_image_table(image_id, user_id, vehicle_id, image_url, status, purpose, filename)
        
        return "Upload successful"
    except Exception as e:
        return str(e)
    
def delete_image_using_image_id(image_id):
    dynamodb = boto3.client('dynamodb')
    s3 = boto3.client('s3')
    vehicle_image_table = 'retroideal-vehicle-image-table'  # Replace with your table name
    bucket_name = 'your_bucket_name'  # Replace with your S3 bucket name

    try:
        # Retrieve the filename from the DynamoDB table using image-id
        response = dynamodb.get_item(
            TableName=vehicle_image_table,
            Key={'image-id': {'S': image_id}}
        )

        # Check if the item exists and extract the filename
        if 'Item' in response:
            filename = response['Item']['filename']['S']

            # Delete the image from the S3 bucket using the filename
            s3.delete_object(Bucket=bucket_name, Key=filename)

            # Delete the entry from the DynamoDB table using image-id
            dynamodb.delete_item(
                TableName=vehicle_image_table,
                Key={'image-id': {'S': image_id}}
            )

            print(f"Image with image-id '{image_id}' deleted from S3 and DynamoDB.")
        else:
            print(f"No entry found for image-id '{image_id}'.")

    except Exception as e:
        print(f"An error occurred: {e}")