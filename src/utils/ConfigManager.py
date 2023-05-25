import os
import configparser


class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Get the absolute path to the config file
        config_path = os.path.join(script_dir, "../config.ini")

        self.config.read(config_path)

    def get_value(self, key):
        section = "DEFAULT"
        try:
            return self.config[section][key]
        except KeyError:
            print(f"No such key '{key}' in section '{section}'")
            return None
