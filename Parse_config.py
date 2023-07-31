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
        
        if "<xxxnr0000aaaa101>" in condition_line  or "<hostname>" in condition_line :
            condition_line = condition_line.replace("<xxxnr0000aaaa101>", setup_config["WAN info"]["Hostname"])
            condition_line = condition_line.replace("<hostname>", setup_config["WAN info"]["Hostname"])
            line = condition_line
        
        elif re.search(r"<loopback\d+>", condition_line) or "10.17x.x.x" in condition_line:
            condition_line = re.sub(r"<loopback\d+>", setup_config["WAN info"]["Loopback"], condition_line)
            condition_line = condition_line.replace("10.17x.x.x", setup_config["WAN info"]["Loopback"])
            line = condition_line
        
        elif "[upload bandwidth fo internet link bps]" in condition_line:
            if int(setup_config["Main Link"]["Main_port_speed"]) >= int(setup_config["Backup Link"]["Backup_port_speed"]):       
                line = condition_line.replace("[upload bandwidth fo internet link bps]", str(setup_config["Main Link"]["Main_port_speed"]))\
                    .replace("\n", "") + "000000"
            else:    
                line = condition_line.replace("[upload bandwidth fo internet link bps]", str(setup_config["Backup Link"]["Backup_port_speed"]))\
                    .replace("\n", "") + "000000"
            
        
        elif "<country, city, sidxxxx>" in condition_line :
            line = condition_line.replace("<country", setup_config["WAN info"]["Hostname"][:3])\
                       .replace("city", setup_config["Location info"]["City"])\
                       .replace("sidxxxx>", "SID" + setup_config["WAN info"]["Hostname"][5:9])


        return line   
  
    
    def __init__(self, path_to_config, setup_config):
        self.path_to_config = path_to_config
        self.setup_config = setup_config
        config = get_txt_content(self.path_to_config)
        final_config = self.look_and_replace_strings(config)
        # print(final_config)
        # print(self.path_to_config)
        write_file(self.path_to_config, final_config)
        print("[+] file saved successfully")
        
        
    def look_and_replace_strings(self, content):
        final_config = []
        for line in content:
            final_config.append(self._replacement_rules(line, self.setup_config))

        
        return final_config
            
            
                    
        
    
    
        
        
        
        