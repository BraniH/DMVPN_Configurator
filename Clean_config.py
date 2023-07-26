from Filter_strings import FilterStrings


def get_txt_content(path, encoding='utf-8'):

    with open(path, 'r', encoding=encoding) as file:
        content = file.readlines()
        
    return content


def write_file(path, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
                file.writelines(content)
                

def delete_line(path, target_string, content, encoding='utf-8'):
    updated_content = [line for line in content if target_string not in line]
    write_file(path, updated_content, encoding=encoding)
    

class CleanConfig:
    
    def __init__(self, path_to_config, setup_config):
        self.path_to_config = path_to_config
        self.setup_config = setup_config
        
        # [+] cleans up start of the config file from unnecessary content until the specified region
        self.file_begining_cleanup()

        
        # [+] based on if the setup provided by the user choose 4G or not it will clear unnecessary content from branch 
        # to either end of the file or until 4G config section. If 4G config is selected as true it also clears unnecessary
        # config contend after 4G section
        if (setup_config["Main Link"]["4G+Cellular"] == False) and (setup_config["Backup Link"]["4G+Cellular"] == False): 
            self.file_ending_cleanup(target_string=FilterStrings("Ending").filter_string)
            
            # Remove ZBFW config if required
            if setup_config["WAN info"]["ZBFW"] == False:
                self.file_ending_cleanup(target_string=FilterStrings("ZBFW").filter_string, delete_target_string=True)
        else:
            self.file_mid_content_cleanup(start_flag=FilterStrings("Ending").filter_string, 
                                          end_flag=FilterStrings("Cellular").filter_string)
            
            self.file_ending_cleanup(target_string=FilterStrings("Manual enroll").filter_string, delete_target_string=True)
            
            # Remove ZBFW config if required
            if setup_config["WAN info"]["ZBFW"] == False:
                self.file_mid_content_cleanup(start_flag=FilterStrings("ZBFW").filter_string, 
                                            end_flag=FilterStrings("Cellular").filter_string)
                
        
        #Removes all branch configurations except one selected by the user
        if setup_config["WAN info"]["Design"].upper() == "BASE":

            if setup_config["Location info"]["Region"] == "EMEA":
                self.file_mid_content_cleanup(start_flag=FilterStrings("SMART").filter_string,
                                            end_flag=FilterStrings("LAN_Interface").filter_string)
            else:
                self.file_mid_content_cleanup(start_flag=FilterStrings("SMART").filter_string,
                                            end_flag=FilterStrings("EIGRP_Starting").filter_string)
                
            
        elif setup_config["WAN info"]["Design"].upper() == "SMART":
            
            self.file_mid_content_cleanup(start_flag=FilterStrings("BASE").filter_string,
                                            end_flag=FilterStrings("SMART").filter_string)
            
            if setup_config["Location info"]["Region"] == "EMEA":
                self.file_mid_content_cleanup(start_flag=FilterStrings("FLOW").filter_string,
                                            end_flag=FilterStrings("LAN_Interface").filter_string)
            else:
                self.file_mid_content_cleanup(start_flag=FilterStrings("FLOW").filter_string,
                                            end_flag=FilterStrings("EIGRP_Starting").filter_string)
            
        elif setup_config["WAN info"]["Design"].upper() == "FLOW":
            
            self.file_mid_content_cleanup(start_flag=FilterStrings("BASE").filter_string,
                                            end_flag=FilterStrings("FLOW").filter_string)
        else:
            print("[!] Wrong value set by the user!")
        
        
        # Handles EIGRP, coverged, incoutnry hub, Lan interface configuration, converged
        if setup_config["Location info"]["Region"] == "EMEA":
            self.file_mid_content_cleanup(start_flag=FilterStrings("LAN_Interface").filter_string,
                                        end_flag=FilterStrings("UP_to_Certificate_Enrollment").filter_string)
        
        elif setup_config["Location info"]["Region"] == "NAM":
        
            if setup_config["WAN info"]["Migration from MPLS"] != "True - Production router" and setup_config["WAN info"]["Converged router"] == False:
                self.file_mid_content_cleanup(start_flag=FilterStrings("EIGRP_Starting").filter_string,
                                        end_flag=FilterStrings("UP_to_Certificate_Enrollment").filter_string)
            
            elif setup_config["WAN info"]["Migration from MPLS"] == "True - Production router" and setup_config["WAN info"]["Converged router"] == False:
                self.file_mid_content_cleanup(start_flag=FilterStrings("EIGRP_Starting").filter_string,
                                        end_flag=FilterStrings("MPLS_Migration").filter_string)
                
            elif setup_config["WAN info"]["Migration from MPLS"] != "True - Production router" and setup_config["WAN info"]["Converged router"] == True:
                self.file_mid_content_cleanup(start_flag=FilterStrings("EIGRP_Starting").filter_string,
                                        end_flag=FilterStrings("Converged_router").filter_string)
                self.file_mid_content_cleanup(start_flag=FilterStrings("In-Country_Hub").filter_string,
                                        end_flag=FilterStrings("UP_to_Certificate_Enrollment").filter_string)
            else:
                 self.file_mid_content_cleanup(start_flag=FilterStrings("EIGRP_Starting").filter_string,
                                        end_flag=FilterStrings("Converged_router").filter_string)
                 self.file_mid_content_cleanup(start_flag=FilterStrings("In-Country_Hub").filter_string,
                                        end_flag=FilterStrings("MPLS_Migration").filter_string)
    
        else:
            self.file_mid_content_cleanup(start_flag=FilterStrings("EIGRP_Starting").filter_string,
                                        end_flag=FilterStrings("UP_to_Certificate_Enrollment").filter_string)
            
        
    '''The beginning of the file will be cleaned up from unnecessary content'''
    def file_begining_cleanup(self, encoding='utf-8'):
        
        region = FilterStrings("Region").filter_string
        flag = region.replace("<Region>", self.setup_config["Location info"]["Region"])
        flag_lines = flag.strip().split('\n')
        content = get_txt_content(self.path_to_config)
        

        with open(self.path_to_config, 'w', encoding=encoding) as file:
            found = False
            for line in content:
                if line.strip() == flag_lines[0]:
                    found = True
                if found:
                    file.write(line)
                    
    
    def file_ending_cleanup(self, target_string, delete_target_string=False):
        content = get_txt_content(self.path_to_config)
        target_lines = target_string.strip().split('\n')
        index = -1

        for i in range(len(content) - len(target_lines) + 1):
            lines_to_check = content[i:i+len(target_lines)]
            if all(line.strip() == target.strip() for line, target in zip(lines_to_check, target_lines)):
                index = i + len(target_lines)
                break

        if index != -1:
            content = content[:index]
            write_file(self.path_to_config, content)
                       
        else:
            print("[!] Filter setting stopped working in file_ending_cleanup function. The filter needs to be changed!")
            
        if delete_target_string == True:
            delete_line(self.path_to_config, target_string, content)
			 
    
    def file_mid_content_cleanup(self, start_flag, end_flag):
        content = get_txt_content(self.path_to_config)
        start_lines = start_flag.strip().split('\n')
        end_lines = end_flag.strip().split('\n')
        start_index = None
        end_index = None

        for i in range(len(content) - len(start_lines) + 1):
            found_start = True
            for j in range(len(start_lines)):
                if content[i + j].strip() != start_lines[j].strip():
                    found_start = False
                    break
            if found_start:
                start_index = i
                break

        if start_index is not None:
            for i in range(start_index + len(start_lines), len(content) - len(end_lines) + 1):
                found_end = True
                for j in range(len(end_lines)):
                    if content[i + j].strip() != end_lines[j].strip():
                        found_end = False
                        break
                if found_end:
                    end_index = i
                    break

        if start_index is not None and end_index is not None:
            content = content[:start_index] + content[end_index:]
            write_file(self.path_to_config, content)
        else:
            print("Start or end string not found in the file.")

    
        
    
if __name__ == "__main__":
    path = r"C:\Users\brani\OneDrive\Počítač\DMVPN config\DMVPN_Configurator\Config\DMVPN - Copy.txt"


    setup_config = {'Location info': {'Region': 'APAC', 'City': 'Washington'}, 
                    'WAN info': {'Hostname': 'USAnr4003ALEX101', 'Loopback': '10.173.130.16', 'Design': 'BASE', 'Migration from MPLS': 'True - Production router', 'ZBFW': False}, 
                    'Main Link': {'Main_IP+mask': '192.1.1.2/24', 'Main_GW': '192.1.1.1', 'Main_port_speed': 100, 'Tunnel_25/27_IP': '172.25.1.1', 'Main_DC_Tunnel_Speed': 20, '4G+Cellular': False, 'APN': 'internet.odjosky.com'}, 
                    'Backup Link': {'Backup_IP+mask': 'DHCP', 'Backup_port_speed': 40, 'Tunnel_26/28_IP': '172.26.1.1', 'backup_DC_Tunnel_Speed': 20, '4G+Cellular': True, 'APN': 'internet.odjosky.com'}, 
                    'Zscaler': {'Tunnel_type': 'IPsec', 'Main_Zscaler_limitation': 50, 'Backup_Zscaler_limitation': 40}, 
                    'LAN info': {'LAN_interface': 'Vlan1', 'LAN_IP+mask': '10.2.2.1/25'}}

    
    
    # print(setup_config["Location info"][0]["Region"])
    CleanConfig(path, setup_config)
