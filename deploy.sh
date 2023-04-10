#!/bin/bash

# Set your instance configuration
AMI_ID="ami-0c252bb9e6b71848e"
INSTANCE_TYPE="t2.micro"
VOLUME_SIZE=30

# Set the name of the instance
INSTANCE_NAME="WhisperingGPT"

# Create EC2 instance
echo "Creating EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances --user-data file://user_data.txt --image-id $AMI_ID --count 1 --instance-type $INSTANCE_TYPE --key-name $KEY --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value='"$INSTANCE_NAME"'}]' --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$VOLUME_SIZE,\"DeleteOnTermination\":true}}]" --security-group-ids $SECURITY_GROUP_ID --query 'Instances[0].InstanceId' --output text)
echo "Instance ID: $INSTANCE_ID"

# Wait for instance to be running
echo "Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get instance public IP
echo "Getting instance public IP..."
PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo "Instance public IP: $PUBLIC_IP"

# Open necessary ports in security group
echo "Opening necessary ports in security group..."
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 8000 --cidr 0.0.0.0/0

# Check API status
while true
do
    # Make HTTP request to API endpoint
    response=$(curl -s http://$PUBLIC_IP:8000)

    # Check response status code
    if [ "$(echo $response | jq -r '.status')" == "success" ]; then
        echo "WhisperingGPT API is now live at http://$PUBLIC_IP:8000"
        break  # exit the loop if API endpoint is up
    fi

    # Wait for 30 seconds before making the next request
    sleep 30
done


