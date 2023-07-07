import os

from Baseline_config import BaselineConfig

def openfile(file_name):
    file_path = os.getcwd() + file_name

    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
            print("File not found.")
    except IOError:
            print("Error while reading the file.")

def setup_parser(setup_config):
    data = {}

    lines = setup_config.strip().split('\n')

    for line in lines:
        try:
            key, value = line.split(':')
            key = key.strip()
            value = value.strip()
            data[key] = value
        except ValueError:
             pass
        
    return data

if __name__ == "__main__":

    '''base variables and paths'''
    
    setup = "\\setup.txt"
    setup_config = openfile(setup)

    Baseline = "\\Templates\\{}\\baseline.txt".format(setup_parser(setup_config)["Region"])

    '''baseline config generator'''
    baseline_config = openfile(Baseline)
    baseline_config = BaselineConfig(baseline_config, 
                   setup_parser(setup_config)["Loopback IP"],
                   setup_parser(setup_config)["Hostname"],
                   setup_parser(setup_config)["LAN"],
                   setup_parser(setup_config)["Main port speed"])
    
    print(baseline_config.config_template)