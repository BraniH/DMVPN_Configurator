from Filter_strings import FilterStrings


def get_txt_content(path, encoding='utf-8'):

    with open(path, 'r', encoding=encoding) as file:
        content = file.readlines()
        
    return content


class CleanConfig:
    
    def __init__(self, path_to_config, setupconfig):
        self.path_to_config = path_to_config
        self.setupconfig = setupconfig
        self.file_begining_cleanup()
        
        if setup_config["Main Link"][5]["4G+Cellular"] == False:
            self.file_ending_cleanup(path_to_config, target_string=None)
        else:
            self.file_mid_content_cleanup(path_to_config, start_string=None, end_string=None)
        

    '''The beginning of the file will be cleaned up from unnecessary content'''
    
    def file_begining_cleanup(self, encoding='utf-8'):
        
        region = FilterStrings("Region").filter_string
        flag = region.replace("<Region>", self.setupconfig["Location info"][0]["Region"])
        flag_lines = flag.strip().split('\n')
        content = get_txt_content(self.path_to_config)
        

        with open(self.path_to_config, 'w', encoding=encoding) as file:
            found = False
            for line in content:
                if line.strip() == flag_lines[0]:
                    found = True
                if found:
                    file.write(line)
                    
    
    def file_ending_cleanup(input_file, target_string):
        content = get_txt_content(input_file)
        index = -1

        for i, line in enumerate(content):
            if line.strip() == target_string.strip():
                index = i
                break

        if index != -1:
            content = content[:index+1]

            with open(input_file, 'w', encoding='utf-8') as file:
                file.writelines(content)
        else:
            print("Target string not found in the file.")
            
    
    def file_mid_content_cleanup(input_file, start_string, end_string):
        pass
    

        
    
if __name__ == "__main__":
    path = r"C:\Users\brani\OneDrive\Počítač\DMVPN config\DMVPN_Configurator\Config\DMVPN - Copy.txt"


    setup_config = {'Location info': [{'Region': 'APAC'}, 
                                      {'City': 'Washington'}], 'WAN info': [{'Hostname': 'USAnr4003ALEX101'}, 
                                      {'Loopback': '10.173.130.16'}, {'Design': 'BASE'}, {'Migration from MPLS': 'True - Production router'}, 
                                      {'ZBFW': False}], 
                                      'Main Link': [{'Main_IP+mask': '192.1.1.2/24'}, {'GW': '192.1.1.1'}, {'Main_port_speed': 100}, 
                                     {'Tunnel_25/27_IP': '172.25.1.1'}, {'Main_DC_Tunnel_Speed': 20}, {'4G+Cellular': False}, {'APN': "apn.josko.sk"}], 
                                      'Backup Link': [{'Main_IP+mask': 'DHCP'}, {'Main_port_speed': 40}, {'Tunnel_26/28_IP': '172.26.1.1'}, {'Main_DC_Tunnel_Speed': 20}, 
                                                      {'4G+Cellular': False}], 'Zscaler': [{'Tunnel_type': 'IPsec'}, {'Main_Zscaler_limitation': 50}, {'Backup_Zscaler_limitation': 40}], 
                                      'LAN info': [{'LAN_interface': 'Vlan1'}, {'LAN_IP+mask': '10.2.2.1/25'}]}

    
    
    # print(setup_config["Location info"][0]["Region"])
    # CleanConfig(path, setup_config)
