def read_config(config_file):
    config = {}
    with open(config_file, "r") as file:
        for line in file:
            key, value = line.strip().split('=',1)
            if key in config.keys():
                config[key].append(value)
            else :
                config[key] = [value]
    return config