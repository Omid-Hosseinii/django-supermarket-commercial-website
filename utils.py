from uuid import uuid4
import os
#----------------------------------------------------------------------------------------------------------

def create_random_code(count):
    import random
    count-=1
    return random.randint(10**count,10**(count+1)-1)

#----------------------------------------------------------------------------------------------------------

def send_sms(mobile_number,message):
    pass

#----------------------------------------------------------------------------------------------------------

class UploadFile:
    def __init__(self,dir,prefix):
        self.dir = dir
        self.prefix = prefix
        
    def upload_to(self,instance,filename):
        filename,ext = os.path.splitext(filename)
        return f'{self.dir}/{self.prefix}/{uuid4()}{ext}'  