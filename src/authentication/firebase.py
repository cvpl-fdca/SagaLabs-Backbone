# authentication/firebase.py
import firebase_admin
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json


keyVaultUri = "https://sagalabskeyvault.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=keyVaultUri, credential=credential)

secret_name = "SagaLabs-Backbone-Firebase-privatekey-json"
retrieved_secret = client.get_secret(secret_name)

cred = json.loads(retrieved_secret.value)  # this will be your JSON content as a dict

firebase_app = firebase_admin.initialize_app(cred)
