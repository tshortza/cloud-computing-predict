
"""
    Final AWS Lambda function skeleton. 
    
    Author: Explore Data Science Academy.
    
    Note:
    ---------------------------------------------------------------------
    The contents of this file should be added to a AWS  Lambda function 
    created as part of the EDSA Cloud-Computing Predict. 
    For further guidance around this process, see the README instruction 
    file which sits at the root of this repo.
    ---------------------------------------------------------------------

"""

# Lambda dependencies
import boto3    # Python AWS SDK
import json     # Used for handling API-based data.
import base64   # Needed to decode the incoming POST data
import numpy as np # Array manipulation
# <<< You will need to add additional libraries to complete this script >>> 

# ** Insert key phrases function **
# --- Insert your code here ---

# -----------------------------

# ** Insert sentiment extraction function **
# --- Insert your code here ---
 
# -----------------------------

# ** Insert email responses function **
# --- Insert your code here ---
 
# -----------------------------

# Lambda function orchestrating the entire predict logic
def lambda_handler(event, context):
    
    # Perform JSON data decoding 
    body_enc = event['body']
    dec_dict = json.loads(base64.b64decode(body_enc))
    

    # ** Insert code to write to dynamodb **
    # <<< Ensure that the DynamoDB write response object is saved 
    #    as the variable `db_response` >>> 
    # --- Insert your code here ---
    import random
    rid = random.randint(0,1000000000) # <--- Replace this value with your code.
    # random.shuffle(rid)
    # -----------------------------
    
    # ** Instantiate the DynamoDB service with the help of the boto3 library **
    
    # --- Insert your code here ---
    dynamodb = boto3.resource('dynamodb', endpoint_url="https://dynamodb.eu-west-1.amazonaws.com") # <--- Replace this value with your code.
    # -----------------------------
    
    # Instantiate the table. Remember pass the name of the DynamoDB table created in step 4
    table = dynamodb.Table('tshortdatatable')
    
    # ** Write the responses to the table using the put_item method. **

    # Complete the below code so that the appropriate 
    # incoming data is sent to the matching column in your DynamoDB table
    # --- Insert your code here ---
    db_response = table.put_item(Item={'ResponsesID': rid, # <--- Insert the correct variable
                        'Name': dec_dict['name'], # <--- Insert the correct variable
                        'Email': dec_dict['email'], # <--- Insert the correct variable
                        'Cell': dec_dict['phone'], # <--- Insert the correct variable
                        'Message': dec_dict['message'] # <--- Insert the correct variable
    })

    # -----------------------------
    

    # --- Amazon Comprehend ---
    comprehend = boto3.client(service_name='comprehend')
    
    # --- Insert your code here ---
    enquiry_text = None # <--- Insert code to place the website message into this variable
    # -----------------------------
    
    # --- Insert your code here ---
    sentiment = None # <---Insert code to get the sentiment with AWS comprehend
    # -----------------------------
    
    # --- Insert your code here ---
    key_phrases = None # <--- Insert code to get the key phrases with AWS comprehend
    # -----------------------------
    
    # Get list of phrases in numpy array
    phrase = []
    for i in range(0, len(key_phrases['KeyPhrases'])-1):
        phrase = np.append(phrase, key_phrases['KeyPhrases'][i]['Text'])


    # ** Use the `email_response` function to generate the text for your email response **
    # <<< Ensure that the response text is stored in the variable `email_text` >>> 
    # --- Insert your code here ---
    # Do not change the name of this variable
    email_text = 'Insert your sample email here'

    # ** SES Functionality **

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    # --- Insert your code here ---
    SENDER = 'tshort.za@gmail.com'
    # -----------------------------

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    # --- Insert your code here ---
    RECIPIENT = 'tshort.za@gmail.com' 
    # -----------------------------


    # The subject line for the email.
    # --- DO NOT MODIFY THIS CODE ---
    SUBJECT = f"Data Science Portfolio Project Website - Hello {dec_dict['name']}"
    # -------------------------------

    # The email body for recipients with non-HTML email clients
    BODY_TEXT = (email_text)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES service resource
    client = boto3.client('ses')

    # Try to send the email.
    try:
        #Provide the contents of the email.
        ses_response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                    # 'edsa.predicts@explore-ai.net', # <--- Uncomment this line once you have successfully tested your predict end-to-end
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(ses_response['MessageId'])
    # -----------------------------


    # ** Create a response object to inform the website that the 
    #    workflow executed successfully. Note that this object is 
    #    used during predict marking and should not be modified.**
    # --- DO NOT MODIFY THIS CODE ---
    lambda_response = {
        'statusCode': 200,
        'body': json.dumps({
        'Name': dec_dict['name'],
        'Email': dec_dict['email'],
        'Cell': dec_dict['phone'], 
        'Message': dec_dict['message'],
        'DB_response': db_response,
        'SES_response': ses_response,
        'Email_message': email_text
        })
    }
    # -----------------------------
    
    return lambda_response   
    




