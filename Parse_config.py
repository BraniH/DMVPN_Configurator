import re

def get_txt_content(path, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as file:
        content = file.readlines()
    return content

def write_file(path, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
        file.writelines(content)
        
def cidr_to_subnet_mask(cidr):
    subnet_mask = [0, 0, 0, 0]
    
    # Calculate the number of bits for the network and host portions
    num_network_bits = cidr
    num_host_bits = 32 - cidr
    
    # Set the network bits to 1 in the subnet_mask
    for i in range(num_network_bits):
        subnet_mask[i // 8] |= (1 << (7 - i % 8))
    
    # Convert each octet of subnet_mask to decimal representation
    subnet_mask_decimals = ".".join(str(octet) for octet in subnet_mask)
    
    return subnet_mask_decimals


class ParseConfig:
    @staticmethod
    def _replacement_rules(line, setup_config):
        condition_line = line.lower()
        '''Tu26 issue has to be sloved in next commit'''
        tu_25_flag = False
        
        if "interface tunnel25" in condition_line:
            tu_25_flag = True
        
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
        elif "<wan interface 1>" in condition_line:
            line = condition_line.replace("<wan interface 1>", "g0/0/1")
        elif "<public ip> | dhcp" in condition_line:
            if str(setup_config["Main Link"]["Main_IP+mask"]).lower() != "dhcp":
                ip, mask = setup_config["Main Link"]["Main_IP+mask"].split("/")
                line = condition_line.replace("<public ip> | dhcp", ip + " " + cidr_to_subnet_mask(int(mask)))
            else:
                line = condition_line.replace("<public ip> | dhcp", "dhcp")
        elif "<gw>" in condition_line and setup_config["WAN info"]["Design"].upper() == "BASE":
            if str(setup_config["Main Link"]["Main_IP+mask"]).lower() != "dhcp":
                 line = condition_line.replace("<gw>", setup_config["Main Link"]["Main_GW"])
            else:
                line = condition_line.replace("ip route vrf inet 0.0.0.0 0.0.0.0 <gw>", "")
        elif "<gre ip>" in condition_line:
            line = condition_line.replace("<gre ip>", setup_config["Main Link"]["Tunnel_25/27_IP"])
        elif "[ same as nhrp group, but in kbps]" in condition_line:
            line = condition_line.replace("[ same as nhrp group, but in kbps]", str(setup_config["Main Link"]["Main_DC_Tunnel_Speed"]) + "000")
        elif "[2m-50m]" in condition_line:
            line = condition_line.replace("[2m-50m]", str(setup_config["Main Link"]["Main_DC_Tunnel_Speed"]) + "M")
        
        print(tu_25_flag)
        return line
    
    
    @staticmethod
    def look_and_replace_strings(content, setup_config):
        return [ParseConfig._replacement_rules(line, setup_config) for line in content]


    def __init__(self, path_to_config, setup_config):
        self.path_to_config = path_to_config
        self.setup_config = setup_config
        config = get_txt_content(self.path_to_config)
        print(self.setup_config)
        # print(self.path_to_config)
        final_config = ParseConfig.look_and_replace_strings(config, setup_config)
        write_file(self.path_to_config, final_config)
        print("[+] file saved successfully")
        
