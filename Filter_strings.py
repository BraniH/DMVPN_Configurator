'''
The class made as storage for string filtering.
'''

class FilterStrings:
    def __init__(self, filter_string):
        self.filetr_string = filter_string
        
        if filter_string == "Region":
            self.get_initial_string(filter_string)
    
    
    def get_initial_string(self, key):
        flag = '''Branch <Country>

                    Staging Process

                    Preparation'''

        return flag