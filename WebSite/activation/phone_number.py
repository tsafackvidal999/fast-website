
class PhoneNumber():
    def __init__(self,brute_phone_number):
        self.phone_number = brute_phone_number
        pass
    def is_valid_phone_number(self):
        new_phone_number=self.clean_a_number(self.phone_number)
        is_correct= self.is_it_correct_number(new_phone_number)
        print(new_phone_number, is_correct)
        return new_phone_number,is_correct



    def clean_a_number(self, dirty_number):
        print("cleaning of the number")  
        dirty_number=str(dirty_number) 
        dirty_number = dirty_number.strip()
        dirty_number=dirty_number.removeprefix('+') # reitre s'il existe
        dirty_number=dirty_number.removeprefix('00') # reitre s'il existe
        dirty_number=dirty_number.removeprefix('+') # necessaire
        dirty_number=dirty_number.removeprefix('237') # reitre s'il existe
        if not dirty_number.startswith('6'):
            dirty_number="6" + dirty_number


        return str(dirty_number)


    def is_it_mnt_number(self, phone_number):
        if(("670000000"<= phone_number <="679999999") or ("650000000"<= phone_number <="654999999") or ("680000000"<= phone_number <="684999999")):
            return True
        return False



    def is_it_orange_number(self, phone_number):
        if( ("655000000"<= phone_number <="659999999") or ("685000000"<= phone_number <="689999999") or ("690000000"<= phone_number <="699999999")):
            return True
        return False



    def is_it_correct_number(self, phone_number):

        
        try:
            temp_phone_number=int(phone_number)
            temp_phone_number+=1
            

        except:
            print("numero invalide")
            return False
        if(len(str(phone_number))!=9):
            return False
        elif(self.is_it_mnt_number(phone_number) or self.is_it_orange_number(phone_number)):
            return True
        return False
