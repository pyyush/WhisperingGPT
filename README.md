# WhisperingGPT
WhisperingGPT is a cutting-edge Speech Translation API that leverages the power of OpenAI's Whisper and GPT-3.5 models to provide highly accurate and fluent translations.

## Setup
1. Install the required dependencies
```sh
pip3 install -r requirements.txt
```

2. Set the OpenAI API Key as an environment variable
```sh
export OPENAI_API_KEY=<your-api-key>
```

## Usage
Start the API server using the following command:
```sh
uvicorn main:app
```
This will start the API server at <ins>http://127.0.0.1:8000</ins>


### Translate Speech
To translate an audio file, make a `POST` request to `/translate_speech` endpoint as shown below:
```sh
import requests

endpoint = "http://127.0.0.1:8000/translate_speech"
payload = {"file": open("audio.wav", "rb"), "target_language": "hindi"}
response = requests.post(endpoint, json=payload)

print(response.json())
```
This will return a JSON response containing the translated text in the target language.

### (Optional) Transcribe Audio
To transcribe an audio file, make a `POST` request to `/transcribe` endpoint as shown below:
```sh
import requests

endpoint = "http://127.0.0.1:8000/transcribe"
payload = {"file": open("audio.wav", "rb")}
response = requests.post(endpoint, json=payload)

print(response.json())
```
This will return a JSON response containing the transcription of the audio file.

### (Optional) Translate Text
To translate text, make a `POST` request to `/translate` endpoint as shown below:
```sh
import requests

endpoint = "http://127.0.0.1:8000/translate"
payload = {"text": "Hello, how are you?", "target_language": "hindi"}
response = requests.post(endpoint, json=payload)

print(response.json())
```
This will return a JSON response containing the translated text in the target language.

## (Optional) Deploying on EC2 using Docker

A [deploy.sh](deploy.sh) shell script is provided to deploy the WhisperingGPT API on EC2 inside a Docker container.

### Requirements
Before using the script, you need to have the following:

- AWS CLI installed and configured on your machine
- An EC2 key pair that you will use to connect to your instance
- The local path to your EC2 key pair
- The ID of a security group that you want to use for your instance
- Your OpenAI API Key

### Usage
1. Set the required variables
```sh
export KEY=<your-ec2-key>
export KEY_PATH=</path/to/your-ec2-key.pem>
export SECURITY_GROUP_ID=<security-group-id>
```

2. Add your OpenAI API Key by replacing `<your-openai-api-key>` with your API key and \
run the below command in your terminal from the root of this repo:
```sh
perl -i -pe 's/export OPENAI_API_KEY=/export OPENAI_API_KEY=<your-openai-api-key>/ if $.==23' install.sh
```

3. Run the script as shown below:
```sh
bash deploy.sh
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.