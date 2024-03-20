#!/usr/bin/python3
import base64       # Import base64 module for encoding
import os           # Import os module for file operations
import json         # Import json module for JSON handling
import subprocess   # Import subprocess module to run commands
import yaml         # Import yaml module for YAML handling

import argparse
script_description = '''
    This script creates a sealed secret containing environment variables,
    intended for use by Kubernetes resources. The following arguments are 
    required when running the program.
    --file-path: 
    --namespace: The Kubernetes namespace where the secret is to be deployed.
    --name: The name of the Kubernetes secret created using the encrypted environment variables.
'''
filepath_description = "The file path of the .env file containing environments to be made secret."
namespace_description = "The Kubernetes namespace where the secret is to be deployed."
name_description = "The name of the Kubernetes secret created using the encrypted environment variables."


parser = argparse.ArgumentParser(description=script_description)
parser.add_argument('--file-path', type=str, required=True, help=filepath_description)
parser.add_argument('--namespace', type=str, required=True, help=namespace_description)
parser.add_argument('--name', type=str, required=True, help=name_description)
args = parser.parse_args()

# Function to process input variable from CLI in the format Variable=Value
def processInputVariable(value):
    
    try:
        value = str(value)             # Convert input value to string
        if '=' not in value:          # Check if '=' exists in the value
            return None               # Return None if '=' is not found
        values = value.split("=")     # Split value into Variable and Value
        if len(values) != 2:          # Check if there are exactly two parts
            return None               # Return None if not exactly two parts
    except:
        print("Please input a valid string in this format: Variable=Value")
        return None
    return values   

def envFileData(file_path):
    data = {}  # Initialize an empty dictionary to store variable data
    with open(file_path, 'r') as file:
        file_content = file.read().splitlines()  # Read file content line by line
        for line in file_content:
            variableData = processInputVariable(line)
            if variableData == None:
                pass
            else:
                # Encode value to base64 and store in dictionary
                value_in_base64 = base64.b64encode(bytes(variableData[1], 'utf-8')).decode('utf-8')
                data[variableData[0]] = value_in_base64
    return data


k8s_secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {
        "name": args.name,
        "namespace": args.namespace
    },
    "data": envFileData(args.file_path)  # Add encoded data to the secret
}

# Get directory path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct absolute path for secret file
secret_file_path = os.path.join(current_dir, 'mysecret.json')

# Write Kubernetes secret to a JSON file
with open(secret_file_path, 'w') as file:
    json.dump(k8s_secret, file)  # Dump secret object to JSON file


# Function to convert sealed secret JSON to YAML format
def sealedSecretConverter(file):

    # Execute kubeseal command and capture the output
    secret = subprocess.run(['kubeseal', '-o', 'json', '-f', file], capture_output=True, text=True)
    
    # Define output file path for the YAML file
    secret_file_path = os.path.join(f'{current_dir}/templates', 'sealedsecret.yaml')
    
    # Write sealed secret JSON output to a YAML file
    with open(secret_file_path, 'w') as file:
        # Convert JSON output to Python dictionary
        secret_json_format = json.loads(secret.stdout)
        # Convert Python dictionary to YAML format
        sealed_secret_in_yaml = yaml.dump(secret_json_format)
        # Write YAML formatted sealed secret to file
        file.write(sealed_secret_in_yaml)

# Call function to convert get sealed secret.
sealedSecretConverter(secret_file_path)


