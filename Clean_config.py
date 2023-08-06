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
    

def delete_content_between_lines(file_path, start_line, end_line):
    # Ensure start_line and end_line are valid positive integers
    if not isinstance(start_line, int) or not isinstance(end_line, int) or start_line < 1 or end_line < 1:
        raise ValueError("Start and end line numbers must be positive integers.")

    # Read the content of the original file
    content = get_txt_content(file_path)

    # Calculate the indices of the lines to be deleted
    start_index = start_line - 1
    end_index = min(end_line, len(content))  # Limit the end_index to the last line

    # Delete the content between the specified lines
    del content[start_index:end_index]
    
    write_file(file_path, content)
    
    
def write_content_at_line(file_path, line_number, content_to_write):
    # Ensure line_number is a valid positive integer
    if not isinstance(line_number, int) or line_number < 1:
        raise ValueError("Line number must be a positive integer.")

    # Read the content of the original file
    content = get_txt_content(file_path)

    # Calculate the index to insert the new content
    insert_index = line_number - 1

    # Insert the new content at the specified line number
    for line in content_to_write:
        print(line)
        insert_index += 1
        content.insert(insert_index, line + f"\n")

    # Write the updated content to a new file
    write_file(file_path, content)
    

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
            
            
        if setup_config["WAN info"]["Design"].upper() == "FLOW":
            self.flow_config_cleanup()
            
        
    '''The beginning of the file will be cleaned up from unnecessary content'''
    def file_begining_cleanup(self, encoding='utf-8'):
        
        region = FilterStrings("Region").filter_string
        flag = region.replace("<Region>", self.setup_config["Location info"]["Region"])
        flag_lines = flag.strip().split('\n')
        content = get_txt_content(self.path_to_config)
 
        #kinda works - one line check - will be deleted once Im sure multiline check works as expected !!!
        # with open(self.path_to_config, 'w', encoding=encoding) as file:
        #     found = False
        #     for line in content:
        #         if line.strip() == flag_lines[0]:
        #             found = True
        #         if found:
        #             file.write(line)
        
        
        with open(self.path_to_config, 'w', encoding=encoding) as file:
            found = False
            flag_index = 0

            for line in content:
                if found:
                    file.write(line)   
                elif line.strip() == flag_lines[flag_index].strip() and found == False:
                    flag_index += 1

                    if flag_index == len(flag_lines):
                        found = True
                        for part in flag_lines:
                            file.write(part.strip() + "\n")                   
                else:
                    flag_index = 0
                    
    
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
            
    
    #sorts flow config
    #!!!! nebude ani treba path ale globalnu premennú !!!
    def flow_config_cleanup(self, encoding='utf'):
        #!!!! nebude ani treba path ale globalnu premennú !!!
        config = get_txt_content(self.path_to_config)
        clear_config = []
        start_flag = False
        line_counter = 0
        
        for line in config:
            line_counter += 1
            if "Router 101 (INET)                 | Router 102 (INET2)" in line:
                start_flag = True
                start_del_line = line_counter - 1
            elif "| spanning-tree guard loop          | spanning-tree guard loop         |" in line:
                start_flag = False
                clear_config.append(line)
                end_del_line = line_counter + 3
        
            if start_flag == True:
                clear_config.append(line)
        
        
        not_wanted = ("+-----------------------------------+----------------------------------+", 
                    "+===================================+==================================+")
        
        element_index = 0

        for line in clear_config:
            for string in not_wanted:
                if string in line:
                    clear_config.pop(element_index)

                
            element_index += 1

        router1 = []
        router2 = []

        for line in clear_config:
            last_occurrence_index = line.rfind("|")
            line = (line[:last_occurrence_index] + line[last_occurrence_index+1:]).replace(line[0], "", 1)
            element_r1, element_r2 = line.split("|")[0], line.split("|")[1]
            router1.append(element_r1)
            router2.append(element_r2)


        merged_config = router1 + router2
        #!!!! nebude ani treba path ale globalnu premennú !!!
        delete_content_between_lines(self.path_to_config, start_del_line, end_del_line)
        #!!!! nebude ani treba path ale globalnu premennú !!!
        write_content_at_line(self.path_to_config, start_del_line, merged_config)    
        
    
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
