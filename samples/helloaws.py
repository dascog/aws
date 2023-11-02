import boto3
import logging

# obtain references to AWS services
s3 = boto3.resource('s3')
sns = boto3.resource('sns')

# list s3 bucket names and collect the names and creation dates in a string

# create a string to hold the bucket names and dates
buffer = ""

# iterate through the buckets and add the bucket names and dates to the string
for bucket in s3.buckets.all():     
    # add the bucket name and creation date to the string
    buffer += bucket.name + "," + bucket.creation_date.strftime("%m/%d/%Y") + "\n"

# print the buffer to stdout
print(buffer)

myEmail = "oweryaresourcing@gmail.com"

# create a SNS topic (this is idempotent so will not recreate the topic if it exists)
topic = sns.create_topic(Name='SampleTopic')

# check if the user is subscribed to the topic
response = topic.subscriptions.all()

# Check if the user is subscribed to the topic
found = False
for subscription in response:
    if subscription.attributes['Endpoint'] == myEmail:
        found = True
        break

if not found:
    # subscribe my email address to the SNS topic
    topic.subscribe(Protocol='email', Endpoint=myEmail)

# publish the buffer to the topic (won't work the first time if not subscribed)
response = topic.publish(
        Message="My buckets: " + buffer
    )

# Read status code from the response (dict type)
print(response['ResponseMetadata']['HTTPStatusCode'])

quit()

