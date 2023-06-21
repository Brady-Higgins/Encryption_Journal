import random
import string
import os
from cryptography.fernet import Fernet
from datetime import datetime as d

class Login:
    def __init__(self):
        self.password_attempts =0
        self.current_directory = os.getcwd()

        self.password_directory = self.current_directory + "\Password.txt"
        self.storage_directory = self.current_directory + "\Storage.txt"
    def getPassword(self):
        password_attempt = input("Password: ")
        self.password_attempt = password_attempt
    def passwordFileCheck(self):
        file_list = os.listdir(self.current_directory)
        if "Password.txt" in file_list:
            self.password_attempt = input("Password: ")
            self.createEncryptionKey()
            self.validateIdentity()

        else:
            self.createPasswordFile()
    def createPasswordFile(self):
        #Creates the text to fill in a password document so the password can pull pieces for the encryption code

        res = "".join(random.choices(string.ascii_uppercase + string.digits, k=3000))
        final_document_list = []
        for letter in res :
            fifty_percent = random.randint(0, 1)
            if fifty_percent == 1 :
                letter = letter.lower()
            final_document_list.append(letter)
        final_document_line = "".join(final_document_list)

        #The password file creation portion that also uploads the final_document_line text
        with open(self.password_directory, 'w', encoding='utf-8') as f :
            i=0
            temp_list = []
            for letter in final_document_line:
                i+=1
                if i%50:
                    f.writelines("".join(temp_list))
                    temp_list = []
                temp_list.append(letter)
        print("Password File Created")
        self.password_attempt = input("Input your permanent password: ")
        self.createStorageFile()

    def createStorageFile(self):

        password_attempt = input("Rewrite your permanent password: ")
        if self.password_attempt == password_attempt:
            with open(self.storage_directory, 'w', encoding='utf-8') as f:
                self.createEncryptionKey()
                message = bytes("[0] V4l1dP4ssw0rd 4uth0r1zedUs4g3","utf-8")
                f.writelines(str(self.fernet_object.encrypt(message)))
            f.close()

        else:
            print("Doesn't match the previous password attempt")
            self.createStorageFile()

    def createEncryptionKey(self):
        from cryptography.fernet import Fernet

        numeric_values = [ord(char) for char in self.password_attempt]
        i =0
        while len(numeric_values) < 43:
            additional_constant = int(numeric_values[i]/2)
            i+=1
            for num in numeric_values:
                if len(numeric_values) <43:
                    numeric_values.append(num+additional_constant)
        password_list = []
        encryption_digits = []
        with open(self.password_directory, 'r', encoding='utf-8') as f :
            for line in f:
                password_line = line
            f.close()
        for char in password_line:
            password_list.append(char)
        for val in numeric_values:
            encryption_digits.append(password_list[val])
        encryption_digits.append("=")
        encryption_key = "".join(encryption_digits)
        encryption_key_bytes = bytes(encryption_key,"utf-8")
        self.encryption_key = encryption_key_bytes
        self.fernet_object = Fernet(self.encryption_key)

    def validateIdentity(self):
        with open(self.storage_directory, 'r', encoding='utf-8') as f:
            validation_line = f.readline()
            val_list = []
            for letter in validation_line:
                val_list.append(letter)
            new_val = val_list[2 :-1]
            character = "".join(new_val)
            byte_validation_line = bytes(character, 'utf-8')
            password_correct = False

            try :
                validation_line_decrypted = self.fernet_object.decrypt(byte_validation_line)
                password_correct = True
            except :
                self.password_attempts += 1
                if self.password_attempts == 3 :
                    print("Too many Incorrect Attempts")
                    exit()
                else :
                    print("Incorrect Password, Please Retry")
                    self.passwordFileCheck()

            if password_correct :
                string_validation_line_d = bytes.decode(validation_line_decrypted)
                if string_validation_line_d == "[0] V4l1dP4ssw0rd 4uth0r1zedUs4g3" :
                    self.Journal()
                else :
                    self.password_attempts += 1
                    if self.password_attempts == 3 :
                        print("Too many Incorrect Attempts")
                        exit()
                    else :
                        print("Incorrect Password, Please Retry")
                        self.passwordFileCheck()
    def Journal(self):
        dayMonthDict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"July",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        choice = input("Commands: Write, Read, Delete, Quit\n")
        document_list = []
        with open(self.storage_directory, 'r', encoding='utf-8') as f :
            for line in f :
                val_list = []
                for letter in line :
                    val_list.append(letter)
                new_val = val_list[2 :-1]
                character = "".join(new_val)
                byte_character = bytes(character, 'utf-8')
                understandable_val = self.fernet_object.decrypt(byte_character)
                document_list.append(understandable_val.decode())
        if choice.lower() == "write" :
            write_to_page = input("Add: ")
            current_time = d.now()
            month_num = int(current_time.strftime("%m"))
            month = dayMonthDict[month_num]
            day_num = str(current_time.strftime("%d"))
            time = str(current_time.strftime("%H:%M"))
            document_list.append(month + " " + day_num + " " + time + " " + write_to_page)
            i = 0
            with open(self.storage_directory, 'w', encoding='utf-8') as f :
                for val in document_list :
                    prefix_order = "[" + str(i) + "]"
                    if prefix_order in val:
                        val = bytes(val, 'utf-8')
                        f.writelines( str(self.fernet_object.encrypt(val)) + "\n")
                    else:

                        if "[" == val[0]:
                            value_list = []
                            for char in val:
                                value_list.append(char)
                            correct_list = value_list[3:]
                            val = "".join(correct_list)
                            val = bytes("[" + str((i)) + "]" + " " + val, 'utf-8')
                            f.writelines(str(self.fernet_object.encrypt(val)) + "\n")
                        else:
                            val = bytes( "[" + str((i))+ "]" + " " + val, 'utf-8')
                            f.writelines( str(self.fernet_object.encrypt(val)) + "\n")
                    i += 1

            f.close()

        if choice.lower() == "read":
            for line in document_list[1:]:
                print(line)

        if choice.lower() == "delete":
            remove_line = input("Remove Line: ")
            i = 0
            if int(remove_line) == 0 or int(remove_line) > len(document_list) :
                print("Invalid Parameters")
            with open(self.storage_directory, 'w', encoding='utf-8') as f :
                for val in document_list :
                    if int(remove_line)==0 or int(remove_line) > len(document_list):
                        pass
                    elif int(remove_line) == i:
                        pass
                    else:
                        val = bytes(val, 'utf-8')
                        f.writelines(str(i) + str(self.fernet_object.encrypt(val)) + "\n")

                    i += 1
        if choice.lower() == "quit":
            exit()
        self.Journal()
def main():
    print("Welcome to the password protected encryption journal\n"
          "If this is your first time using the system, you will have to create your password\n"
          "This will log you out of the system once succesfully created\n"
          "Please log back in after to use the journal\n")

    l = Login()
    l.passwordFileCheck()
if __name__ == "__main__":
    main()