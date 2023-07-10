'''
The class made as storage for string filtering.
'''

class FilterStrings:
    def __init__(self, filter_string):
        
        ''' decides which string will be returned'''
        if filter_string == "Region":
            self.filter_string = self.get_region_string()
    
    
    @staticmethod
    def get_region_string():
        flag = '''Branch <Region>

                    Staging Process

                    Preparation'''

        return flag
    
    
    
if __name__ == "__main__":
    region = FilterStrings("Region")
    print(region.filter_string)