import boto3
import hashlib
import json

def lambda_handler(event, context):
    # Update bucket names and paths
    approved_bucket = 'retroideal-member-vehicle-images'
    approved_prefix = 'approved-vehicle-images/'

    pending_bucket = 'retroideal-member-vehicle-images'
    pending_prefix = 'pending-vehicle-images/'

    # Update DynamoDB table name
    table_name = 'retroideal-vehicle-image-table'

    # Create S3 and DynamoDB clients
    s3 = boto3.client('s3')
    dynamodb = boto3.client('dynamodb')

    # Get the filenames from the payload
    filenames = event.get('filenames') or event.get('filename')

    if not filenames:
        return "No filenames provided"

    if isinstance(filenames, str):
        filenames = [filenames]

    results = []

    # Iterate through each filename
    for filename in filenames:
        # Get the content of the file in the 'pending' folder
        pending_key = pending_prefix + filename
        try:
            pending_object_data = s3.get_object(Bucket=pending_bucket, Key=pending_key)
            pending_content = pending_object_data['Body'].read()
        except s3.exceptions.NoSuchKey:
            results.append(f"{filename}: Pending file not found")
            continue

        # Get the list of objects in the 'approved' folder
        approved_objects = s3.list_objects_v2(Bucket=approved_bucket, Prefix=approved_prefix)['Contents']

        match_found = False

        # Iterate through approved images and compare content
        for approved_object in approved_objects:
            approved_key = approved_object['Key']

            # Skip if the object is a folder
            if approved_key.endswith('/'):
                continue

            # Retrieve the content of the approved image
            approved_object_data = s3.get_object(Bucket=approved_bucket, Key=approved_key)
            approved_content = approved_object_data['Body'].read()

            # Compare image content using hash
            if hashlib.md5(pending_content).hexdigest() == hashlib.md5(approved_content).hexdigest():
                results.append(f"{filename}: Match")
                match_found = True
                break  # If a match is found, no need to check other approved images

        if not match_found:
            try:
                response = dynamodb.scan(
                    TableName=table_name,
                    FilterExpression='filename = :filename',
                    ExpressionAttributeValues={':filename': {'S': filename}}
                )

                if response['Count'] > 0:
                    image_id = response['Items'][0]['image-id']['S']

                    # Update DynamoDB UpdateItem operation to set status to 'approved' and update URL using image-id
                    approved_image_key = f"{approved_prefix}{filename}"
                    pending_image_key = f"{pending_prefix}{filename}"

                    update_response = dynamodb.update_item(
                        TableName=table_name,
                        Key={'image-id': {'S': image_id}},
                        UpdateExpression='SET #status = :status, #image_url = :image_url',
                        ExpressionAttributeNames={'#status': 'status', '#image_url': 'image-url'},
                        ExpressionAttributeValues={
                            ':status': {'S': 'approved'},
                            ':image_url': {'S': f"https://{approved_bucket}.s3.amazonaws.com/{approved_image_key}"}
                        }
                    )
                    print(f"DynamoDB Update Response for filename {filename}: {update_response}")

                    # Move the image from pending to approved folder in S3
                    s3.copy_object(
                        Bucket=approved_bucket,
                        Key=approved_image_key,
                        CopySource={'Bucket': pending_bucket, 'Key': pending_image_key}
                    )
                    s3.delete_object(Bucket=pending_bucket, Key=pending_image_key)
                    print(f"Image moved from '{pending_image_key}' to '{approved_image_key}'")

                    results.append(f"{filename}: Status updated to 'approved'")
                else:
                    results.append(f"{filename}: No item found in DynamoDB")

            except Exception as e:
                print(f"Error processing filename {filename}: {e}")
                results.append(f"{filename}: Error processing - {e}")

    return results
