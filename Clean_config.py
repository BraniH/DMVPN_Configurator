

def get_txt_content(path, encoding='utf-8'):

    with open(path, 'r', encoding=encoding) as file:
        content = file.readlines()
        
    return content


class CleanConfig:
    
    def __init__(self, path_to_config, setupconfig):
        self.path_to_config = path_to_config
        self.setupconfig = setupconfig
        

    def initial_cleanup(self, flag, encoding='utf-8'):

        flag_lines = flag.strip().split('\n')
        content = get_txt_content(self.path_to_config)
        

        with open(self.path_to_config, 'w', encoding=encoding) as file:
            found = False
            for line in content:
                if line.strip() == flag_lines[0]:
                    found = True
                if found:
                    file.write(line)

        
    
if __name__ == "__main__":
    path = r"C:\Users\brani\OneDrive\Počítač\DMVPN config\DMVPN_Configurator\Config\DMVPN - Copy.txt"
    flag = '''Branch APAC

Staging Process

Preparation'''

    setup_config = {'Location info': [{'Region': 'APAC'}, 
                                      {'City': 'Washington'}], 'WAN info': [{'Hostname': 'USAnr4003ALEX101'}, 
                                      {'Loopback': '10.173.130.16'}, {'Design': 'BASE'}, {'Migration from MPLS': 'True - Production router'}, 
                                      {'ZBFW': False}], 'Main Link': [{'Main_IP+mask': '192.1.1.2/24'}, {'GW': '192.1.1.1'}, {'Main_port_speed': 100}, 
                                     {'Tunnel_25/27_IP': '172.25.1.1'}, {'Main_DC_Tunnel_Speed': 20}, {'4G+Cellular': False}], 
                                      'Backup Link': [{'Main_IP+mask': 'DHCP'}, {'Main_port_speed': 40}, {'Tunnel_26/28_IP': '172.26.1.1'}, {'Main_DC_Tunnel_Speed': 20}, 
                                                      {'4G+Cellular': False}], 'Zscaler': [{'Tunnel_type': 'IPsec'}, {'Main_Zscaler_limitation': 50}, {'Backup_Zscaler_limitation': 40}], 
                                      'LAN info': [{'LAN_interface': 'Vlan1'}, {'LAN_IP+mask': '10.2.2.1/25'}]}

    
    CleanConfig(path, setup_config).initial_cleanup(flag)
    print("done")