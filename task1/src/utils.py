def read_config(config_file):
    config = {}
    with open(config_file, "r") as file:
        for line in file:
            if ('=' not in line.strip('\n ')):
                config['STEMMER'] = [line.strip('\n ')]
            else:
                key, value = line.strip().split('=',1)
                if key in config.keys():
                    config[key].append(value)
                else :
                    config[key] = [value]
    return config

def get_stemmer(config_file):
    if config_file['STEMMER'][0] == 'STEMMER':
        return True
    return False