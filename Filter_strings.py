'''
The class made as storage for string filtering.
'''

class FilterStrings:
    def __init__(self, filter_string):
        
        ''' decides which string will be returned'''
        if filter_string == "Region":
            self.filter_string = self.get_region_string()
        elif filter_string == "Ending":
            self.filter_string = self.get_file_ending_cleanup_string()
        elif filter_string == "Cellular":
            self.filter_string = self.cellular_string()
        elif filter_string == "Manual enroll":
            self.filter_string = self.manual_enroll_string()
        elif filter_string == "ZBFW":
            self.filter_string = self.ZBFW_string()
    
    
    @staticmethod
    def get_region_string():
        flag = '''Branch <Region>

                    Staging Process

                    Preparation'''

        return flag
    
    @staticmethod
    def get_file_ending_cleanup_string():
        flag = '''-   In case Integrated Wireless Access-point is implemented on DMVPN NG
    router where ZBF is configured it is then necessary to add SVIs
    created for wireless networks (e.g. SVI VLAN30 used by HCAccess)
    into INSIDE security zone as a member!'''
        
        return flag
    
    @staticmethod
    def cellular_string():
        flag = '''Appendix

                LTE Configuration

                cellular 0/1/0 lte profile create 1 APN.domain

                controller Cellular 0/1/0'''
        
        return flag
    
    @staticmethod
    def manual_enroll_string():
        flag = '''Manual Certificate Enrollment'''
        
        return flag
    
    @staticmethod
    def ZBFW_string():
        flag = '''Zone Base Firewall (ZBFW)'''
        
        return flag
    
    
if __name__ == "__main__":
    region = FilterStrings("Region")
    print(region.filter_string)