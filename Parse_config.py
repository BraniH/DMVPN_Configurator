import re

def get_txt_content(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as file:
        content = file.readlines()
    return content

def write_file(path, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
        file.writelines(content)

class ParseConfig:
    @staticmethod
    def _replacement_rules(line, setup_config):
        condition_line = line.lower()
        
        if "<xxxnr0000aaaa101>" in condition_line or "<hostname>" in condition_line:
            line = condition_line.replace("<xxxnr0000aaaa101>", setup_config["WAN info"]["Hostname"]) \
                                 .replace("<hostname>", setup_config["WAN info"]["Hostname"])
        elif re.search(r"<loopback\d+>|10.17x.x.x", condition_line):
            line = re.sub(r"<loopback\d+>", setup_config["WAN info"]["Loopback"], condition_line) \
                      .replace("10.17x.x.x", setup_config["WAN info"]["Loopback"])
        elif "[upload bandwidth fo internet link bps]" in condition_line:
            main_speed = setup_config["Main Link"]["Main_port_speed"]
            backup_speed = setup_config["Backup Link"]["Backup_port_speed"]
            speed = str(main_speed) if int(main_speed) >= int(backup_speed) else str(backup_speed)
            line = condition_line.replace("[upload bandwidth fo internet link bps]", speed + "000000").replace("\n", "")
        elif "<country, city, sidxxxx>" in condition_line:
            line = condition_line.replace("<country", setup_config["WAN info"]["Hostname"][:3]) \
                                 .replace("city", setup_config["Location info"]["City"]) \
                                 .replace("sidxxxx>", f"SID{setup_config['WAN info']['Hostname'][5:9]}")
        
        return line
    
    
    @staticmethod
    def look_and_replace_strings(content, setup_config):
        return [ParseConfig._replacement_rules(line, setup_config) for line in content]


    def __init__(self, path_to_config, setup_config):
        self.path_to_config = path_to_config
        self.setup_config = setup_config
        config = get_txt_content(self.path_to_config)
        # print(final_config)
        # print(self.path_to_config)
        final_config = ParseConfig.look_and_replace_strings(config, setup_config)
        write_file(self.path_to_config, final_config)
        print("[+] file saved successfully")
        
