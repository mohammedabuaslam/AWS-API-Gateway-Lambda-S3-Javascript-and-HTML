# AWS REST API, Lambda, DynamoDB and S3 Application

This application provides a solution to process form data, store it in a DynamoDB table and an S3 bucket, and retrieve the data on request. The form data is submitted using an HTML form, processed by an AWS Lambda function (Python), and returned via a REST API endpoint in AWS API Gateway.

## Prerequisites

- An AWS account
- An S3 bucket created in AWS

## Steps

1. Create a REST API endpoint using AWS API Gateway
2. Create a Lambda function in Python
3. Create a DynamoDB table
4. Store data in DynamoDB
5. Store the image in S3
6. Return a response from Lambda
7. Retrieve data from DynamoDB and S3
8. Integrate the HTML form with the REST API endpoint using JQuery

## Notes

Refer the lambda_function.py file to get an overview of the functionality.
Refer the HTML files to store and retrieve the data
