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
    def _replacement_rules(line, setup_config, inet2_flag, backup_tunnel_flag):
        condition_line = line.lower()

        #baseline configuration handling
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
        
        #final configuration  
        elif "<country, city, sidxxxx>" in condition_line:
            line = condition_line.replace("<country", setup_config["WAN info"]["Hostname"][:3]) \
                                 .replace("city", setup_config["Location info"]["City"]) \
                                 .replace("sidxxxx>", f"SID{setup_config['WAN info']['Hostname'][5:9]}")
        
        
        #wan interface handling               
        elif "<wan interface 1>" in condition_line or "<wan interface 2>" in condition_line:
            pattern = r"<wan interface ([12])>"
            line = re.sub(pattern, lambda match: "g0/0/1" if match.group(1) == '1' else "g0/0/0", condition_line) 
             
        elif "<public ip> | dhcp" in condition_line:
            if str(setup_config["Main Link"]["Main_IP+mask"]).lower() != "dhcp":
                ip, mask = setup_config["Main Link"]["Main_IP+mask"].split("/")
                line = condition_line.replace("<public ip> | dhcp", ip + " " + cidr_to_subnet_mask(int(mask)))
            else:
                line = condition_line.replace("<public ip> | dhcp", "dhcp")
             
        elif "<wan ip>" in condition_line:
            condition_line = condition_line.replace("| dhcp", "")
            if str(setup_config["Backup Link"]["Backup_IP+mask"]).lower() != "dhcp":
                ip, mask = setup_config["Backup Link"]["Backup_IP+mask"].split("/")
                line = condition_line.replace("<wan ip>", ip + " " + cidr_to_subnet_mask(int(mask)))
            else:
                line = condition_line.replace("<wan ip>", "dhcp")
        
        #gateway handling
        elif "<gw>" in condition_line:
            if str(setup_config["Main Link"]["Main_IP+mask"]).lower() != "dhcp" and inet2_flag == False:
                line = condition_line.replace("<gw>", setup_config["Main Link"]["Main_GW"])
            elif str(setup_config["Backup Link"]["Backup_IP+mask"]).lower() != "dhcp" and inet2_flag == True:
                line = condition_line.replace("<gw>", setup_config["Backup Link"]["Backup_GW"])
            else:
                line = condition_line.replace(condition_line, "")
        
        #Tunnels handling          	        
        elif "<gre ip>" in condition_line:
            tunnel_info = setup_config["Main Link"]["Tunnel_25/27_IP"] if not backup_tunnel_flag else setup_config["Backup Link"]["Tunnel_26/28_IP"]
            line = condition_line.replace("<gre ip>", tunnel_info)
            
        elif "[ same as nhrp group, but in kbps]" in condition_line:
            tunnel_info = setup_config["Main Link"]["Main_DC_Tunnel_Speed"] if not backup_tunnel_flag else setup_config["Backup Link"]["Backup_DC_Tunnel_Speed"]
            line = condition_line.replace("[ same as nhrp group, but in kbps]", str(tunnel_info) + "000")
            
        elif "[2m-50m]" in condition_line:
            tunnel_info = setup_config["Main Link"]["Main_DC_Tunnel_Speed"] if not backup_tunnel_flag else setup_config["Backup Link"]["Backup_DC_Tunnel_Speed"]
            line = condition_line.replace("[2m-50m]", str(tunnel_info) + "M")
        
        
        return line
    
    
    @staticmethod
    def look_and_replace_strings(content, setup_config):
        final_config = []
        # for line in content:
        #     final_config.append(ParseConfig._replacement_rules(line, setup_config, 
        #                                                        inet2_flag = any("INET2" in configured_line for configured_line in final_config)))
        
        for line in content:
            final_config.append(ParseConfig._replacement_rules(line, setup_config, 
                                                               inet2_flag = any("vrf forwarding INET2" in configured_line for configured_line in final_config),
                                                               backup_tunnel_flag = any("Tunnel26" in configured_line for configured_line in final_config)))
            
        # print(final_config)
        return final_config
        #return [ParseConfig._replacement_rules(line, setup_config) for line in content]


    def __init__(self, path_to_config, setup_config):
        self.path_to_config = path_to_config
        self.setup_config = setup_config
        config = get_txt_content(self.path_to_config)
        #print(self.setup_config)
        # print(self.path_to_config)
        final_config = ParseConfig.look_and_replace_strings(config, setup_config)
        write_file(self.path_to_config, final_config)
        print("[+] file saved successfully")
        

