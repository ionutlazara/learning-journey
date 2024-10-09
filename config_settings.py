import config


def config_from_json_if_exists(json_file: str) -> config.Configuration:
    try:
        return config.config_from_json(json_file, read_from_file=True)
    except FileNotFoundError as e:
        return config.config_from_dict({})
        print(e)

settings = config.ConfigurationSet(
    config_from_json_if_exists(json_file="config_settings.json")
    )
