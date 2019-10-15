class PrintUtil:
    class Colors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    
    @staticmethod
    def log_error(msg):
        print("%s[!] %s%s"%(PrintUtil.Colors.FAIL, msg, PrintUtil.Colors.ENDC))
    
    @staticmethod
    def log_warn(msg):
        print("%s[!] %s%s"%(PrintUtil.Colors.WARNING, msg, PrintUtil.Colors.ENDC))

    @staticmethod
    def log_info(msg):
        print("%s[-] %s%s"%(PrintUtil.Colors.OKBLUE, msg, PrintUtil.Colors.ENDC))

    @staticmethod
    def log_success(msg):
        print("%s[+] %s%s"%(PrintUtil.Colors.OKGREEN, msg, PrintUtil.Colors.ENDC))
