import yaml

def get_required_columns(entity, config_path="column_config.yml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get(entity, [])