# Use only if everything is bad.
class CriticalError(Exception):
    message: str
    
    def __init__(self, message=None):
        self.message = message
    
    def __str__(self):
        if self.message:
            return f"Attention, CriticalError! {self.message}"
        return f"Attention, CriticalError!"

# May be useless(?)
class Warning(Exception):
    message: str
    cause: Exception
    
    def __init__(self, message=None, cause: Exception=None):
        self.cause = cause
        self.message = message
        
    def __str__(self):
        s = "Warning!"
        if self.message: s += f" Message: {self.message}"
        if self.cause: s += f", Cause: {self.cause}"
        return s
    