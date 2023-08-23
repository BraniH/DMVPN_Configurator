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
        elif filter_string == "LAN_Interface":
            self.filter_string = self.lanint_string()
        elif filter_string == "UP_to_Certificate_Enrollment":
            self.filter_string = self.Cert_enroll_string()
        elif filter_string == "EIGRP_Starting":
            self.filter_string = self.EIGRP_start_string()
        elif filter_string == "MPLS_Migration":
            self.filter_string = self.Migration_MPLS_string()
        elif filter_string == "Converged_router":
            self.filter_string = self.Converged_router_string()
        elif filter_string == "In-Country_Hub":
            self.filter_string = self.In_country_Hub_string()
        elif filter_string == "BASE":
            self.filter_string = self.base_branch_string()
        elif filter_string == "SMART":
            self.filter_string = self.smart_branch_string()
        elif filter_string == "FLOW":
            self.filter_string = self.flow_branch_string()
        elif filter_string == "IN-Country-remove":
            self.filter_string = self.in_country_remove_lines()
        elif filter_string == "nhrp_nhrs_27":
            self.filter_string = self.nhrp_nhrs_27()
        elif filter_string == "nhrp_nhrs_28":
            self.filter_string = self.nhrp_nhrs_28()
        
 
    @staticmethod
    def get_region_string():
        flag = '''Branch <Region>

                    Staging Process

                    Preparation'''

        return flag
    
    @staticmethod
    def get_file_ending_cleanup_string():
        flag = "-   In case Integrated Wireless Access-point is implemented on DMVPN NG router where ZBF is configured "\
       "it is then necessary to add SVIs created for wireless networks (e.g. SVI VLAN30 used by HCAccess) into "\
       "INSIDE security zone as a member!"
        
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
    
    
    @staticmethod
    def lanint_string():
        flag = '''LAN interface configuration'''
        
        return flag
    
    
    @staticmethod
    def Cert_enroll_string():
        flag = '''Certificate Enrollment'''
        
        return flag
    
    
    @staticmethod
    def EIGRP_start_string():
        flag = '''EIGRP Summary'''
        
        return flag
    
    
    @staticmethod
    def Migration_MPLS_string():
        flag = '''Migration from MPLS'''
        
        return flag
    
    
    @staticmethod
    def Converged_router_string():
        flag = '''Converged router'''
        
        return flag
    
    
    @staticmethod
    def In_country_Hub_string():
        flag = '''In-Country Hub'''
        
        return flag
    
    
    @staticmethod
    def base_branch_string():
        flag = '''Base

                INET'''
        
        return flag
    
   
    @staticmethod
    def smart_branch_string():
        flag = '''Smart

                INET

                INET & INET2'''
        
        return flag
    
    
    @staticmethod
    def flow_branch_string():
        flag = '''Flow

                INET

                INET & INET2'''
        
        return flag
    
    
    @staticmethod
    def in_country_remove_lines():
        flag = '''ip nhrp nhs 172.25.0.1 nbma 62.134.201.17 multicast
ip nhrp nhs 172.25.0.2 nbma 62.134.201.62 multicast
ip nhrp nhs 172.25.0.3 nbma 178.237.44.105 multicast
ip nhrp nhs 172.25.0.4 nbma 178.237.44.109 multicast
ip nhrp nhs 172.26.0.1 nbma 62.134.201.18 multicast
ip nhrp nhs 172.26.0.2 nbma 62.134.201.63 multicast
ip nhrp nhs 172.26.0.3 nbma 178.237.44.106 multicast
ip nhrp nhs 172.26.0.4 nbma 178.237.44.110 multicast
ip nhrp nhs 172.26.0.1 nbma 199.87.118.204 multicast
ip nhrp nhs 172.26.0.2 nbma 199.87.118.145 multicast
ip nhrp nhs 172.26.0.3 nbma 216.200.150.37 multicast
ip nhrp nhs 172.26.0.4 nbma 216.200.150.41 multicast
ip nhrp nhs 172.26.0.1 nbma 203.117.50.69 multicast
ip nhrp nhs 172.26.0.2 nbma 203.208.237.105 multicast
ip nhrp nhs 172.26.0.3 nbma 118.67.64.5 multicast
ip nhrp nhs 172.26.0.4 nbma 118.67.64.9 multicast
ip nhrp nhs 172.25.0.1 nbma 203.117.50.68 multicast
ip nhrp nhs 172.25.0.2 nbma 203.208.237.104 multicast
ip nhrp nhs 172.25.0.3 nbma 118.67.64.4 multicast
ip nhrp nhs 172.25.0.4 nbma 118.67.64.8 multicast
ip nhrp nhs 172.25.0.1 nbma 199.87.118.201 multicast
ip nhrp nhs 172.25.0.2 nbma 199.87.118.144 multicast
ip nhrp nhs 172.25.0.3 nbma 216.200.150.36 multicast
ip nhrp nhs 172.25.0.4 nbma 216.200.150.40 multicast
nhrp map group 2M service-policy output 2M
nhrp map group 4M service-policy output 4M
nhrp map group 6M service-policy output 6M
nhrp map group 8M service-policy output 8M
nhrp map group 10M service-policy output 10M
nhrp map group 20M service-policy output 20M
nhrp map group 30M service-policy output 30M
nhrp map group 40M service-policy output 40M
nhrp map group 50M service-policy output 50M
nhrp map group 75M service-policy output 75M
nhrp map group 100M service-policy output 100M
nhrp group [2M-50M]'''
        
        return flag
    
    
    @staticmethod
    def nhrp_nhrs_27():
        flag = "ip nhrp nhs 172.27.0.xx nbma <public IP of in-country Hub> multicast"
        
        return flag
    
    @staticmethod
    def nhrp_nhrs_28():
        flag = "ip nhrp nhs 172.28.0.xx nbma <public IP of in-country Hub> multicast"
        
        return flag
    
    
    
if __name__ == "__main__":
    region = FilterStrings("Region")
    print(region.filter_string)