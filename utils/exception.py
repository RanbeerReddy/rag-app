import sys

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details=None):
        super().__init__(str(error_message))
        
        self.error_message = error_message
        
        if error_details:
            _, _, exc_tb = error_details.exc_info()
            
            if exc_tb:
                self.lineno = exc_tb.tb_lineno
                self.file_name = exc_tb.tb_frame.f_code.co_filename
            else:
                self.lineno = None
                self.file_name = None
        else:
            self.lineno = None
            self.file_name = None

    def __str__(self):
        return (
            f"Error in [{self.file_name}] at line [{self.lineno}]: {self.error_message}"
        )