import os


def add_config_option_to_dict(configDict, line):
    res = line.split('=')
    if(len(res) >= 2):
        configDict[res[0]] = res[1].rstrip()


def read_config_file(file):
    if(os.path.isfile(file)):
        try:
            configDict = {}
            with open(file, 'r') as cf:
                line = cf.readline()
                if line.startswith('#') == False:
                    add_config_option_to_dict(configDict, line)

                while line:
                    line = cf.readline()
                    if line.startswith('#') == False:
                        add_config_option_to_dict(configDict, line)

            return configDict

        except Exception as e:
            print(e)
            return None
    else:
        return None


def write_config_file(file, configDict):
    with open(file, 'w') as cf:
        for key, value in configDict.items():
            cf.write(key + '=' + value + '\n')