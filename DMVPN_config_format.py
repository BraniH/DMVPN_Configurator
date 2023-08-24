import os
import re


def get_txt_content(path, encoding='utf-8'):

    with open(path, 'r', encoding=encoding) as file:
        content = file.readlines()
        
    return content

def write_file(path, content, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as file:
        file.writelines(content)
        
#read file get tuple
def read_file_to_tuple(file_path):
    result = ()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove leading and trailing whitespace characters (including '\n')
            cleaned_line = line.strip()
            result += (cleaned_line,)
    
    return result
        
        

class ConfigFormat:
    
    def __init__(self, path_to_config):
        self.path_to_config = path_to_config
        self.config_cleaner()


    def config_cleaner(self):
        config = get_txt_content(self.path_to_config)
        basic_clean_config = self.basic_cleanup(config)
        advanced_clean_config = self.advanced_cleanup_rules(basic_clean_config)
        
        
        # print(advanced_clean_config)
        write_file(self.path_to_config,  advanced_clean_config)    
        
        
    def advanced_cleanup_rules(self, config):
        clean_config = []
        headers = read_file_to_tuple(os.getcwd() + "\\Config\\headers.txt")
        split_lines = read_file_to_tuple(os.getcwd() + "\\Config\\split_lines.txt")
        for line in config:
            line = self.format_config_lines(line, headers, split_lines)
            
            #at the end append only desiareble lines
            clean_config.append(line)
        

        return clean_config
    
    @staticmethod
    def basic_cleanup(config):
        clean_config = []
        undesirable_lines = ("", "\n")
        for line in config:
            line = line.lstrip()
            
            #at the end append only desiareble lines
            if line not in undesirable_lines:
                clean_config.append(line)
            
        return clean_config

    
    @staticmethod
    def format_config_lines(line, headers, split_lines):
        if line.strip() in headers:
            line = f"\n\n{line.strip()} !!!Header \n"
        elif line.strip() in split_lines:
            line = f"\n  {line.strip()}\n"
        elif re.search("^hostname [a-zA-Z]{3}nr\d{4}.*(?:101|102)$", line):
            line = f"\n  {line.strip()}\n"
        elif re.search("ip route vrf (INET|INET2) 0\.0\.0\.0 0\.0\.0\.0", line):
            line = f"\n  {line.strip()}\n"
        else:
            line = f"  {line}"

        return line


if __name__ == "__main__":
    pass