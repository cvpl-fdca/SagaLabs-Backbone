from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from utils.ConfigManager import ConfigManager


class AzKeyVault:
    @staticmethod
    def get_secret(secret_name):
        config_manager = ConfigManager()
        vault_url = config_manager.get_value('AzureVaultURL')  # get the vault_url from the config
        if not vault_url:
            raise ValueError("Vault URL could not be retrieved from config")
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)

        try:
            return client.get_secret(secret_name).value
        except Exception as e:
            print(f"An error occurred while fetching secret: {e}")
            return None
