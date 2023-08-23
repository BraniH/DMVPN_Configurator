def get_txt_content(path, encoding='utf-8'):

    with open(path, 'r', encoding=encoding) as file:
        content = file.readlines()
        
    return content

class ConfigFormat:
    
    def __init__(self, path_to_config):
        self.path_to_config = path_to_config
        self.config_cleaner()


    def config_cleaner(self):
        config = get_txt_content(self.path_to_config)
        print(config)
        
    
    @staticmethod
    def basic_cleanup():
        pass
    
    
    @staticmethod
    def advanced_cleanup_rules():
        pass