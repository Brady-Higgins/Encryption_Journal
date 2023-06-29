
import os
import random
import string
import sys
from datetime import datetime as d
from cryptography.fernet import Fernet
class Login:
    def __init__(self):
        self.password_attempts =0

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.current_directory = os.getcwd()

        self.password_directory = os.path.join(os.path.dirname(__file__), "Password.txt")
        self.storage_directory = os.path.join(os.path.dirname(__file__), "Storage.txt")
        self.sections_directory = os.path.join(os.path.dirname(__file__), "Sections.txt")
    def getPassword(self):
        password_attempt = input("Password: ")
        self.password_attempt = password_attempt
    def passwordFileCheck(self):
        self.file_list = os.listdir(self.current_directory)


        if "Password.txt" in self.file_list:
            self.password_attempt = input("Password: ")
            self.createEncryptionKey()
            self.validateIdentity()

        else:
            self.createPasswordFile()
        if "Sections.txt" in self.file_list:
            pass
        else:
            with open(self.sections_directory, 'w', encoding='utf-8') as f :
                f.writelines("")
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
                    sys.exit()
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
                        sys.exit()
                    else :
                        print("Incorrect Password, Please Retry")
                        self.passwordFileCheck()
    def Journal(self):
        dayMonthDict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"July",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
        choice = input("Commands: Write, Read, Delete, Quit\n")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        #Appends contents of encrypted text file to document_list after decrypting
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


        sections = []
        with open(self.sections_directory, 'r', encoding='utf-8') as f:
            for line in f:
                if line == "\n":
                    pass
                else:
                    word = []
                    for letter in line:
                        word.append(letter)
                    sections.append("".join(word[:-1]))




        if choice.lower() == "write" :

            #Section portion: Appends to previous sections list and writes it on sections.txt
            print("Sections: ",end="")
            for section in sections:
                print(section,end=", ")
            print("\b")
            section = input("Section: ")
            if section.isspace() or section == "":
                print("Improper Section Name")
                self.Journal()










            section_val = "{" + section + "}"
            if section_val in sections:
                pass
            else:
                sections.append(section_val)
            with open(self.sections_directory, 'w', encoding='utf-8') as f :
                for line in sections:
                    f.writelines(line + "\n")
            f.close()

            #Content added is given a date then appended to end of document_list
            write_to_page = input("Add: ")


            if section == "OldData" :
                write_to_page += " Jun"              #Adds to end of input so the function knows where to end it
                i=1
                word_list = write_to_page.split()
                sentence_list = []
                first = True

                for word in word_list:
                    if not first:
                        if word in months:

                            sentence = " ".join(sentence_list)
                            document_list.append("[" + str(i) + "]" + " " + sentence)
                            i+=1
                            sentence_list = []
                            sentence_list.append(word)
                        else:
                            sentence_list.append(word)
                    else:
                        sentence_list.append(word)
                        first = False

            else:
                current_time = d.now()
                month_num = int(current_time.strftime("%m"))
                month = dayMonthDict[month_num]
                day_num = str(current_time.strftime("%d"))
                time = str(current_time.strftime("%H:%M"))
                document_list.append(section_val +" "+ month + " " + day_num + " " + time + " " + write_to_page)
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
            print("Sections: ",end="")
            for section in sections:
                print(section,end=",")
            print("\b")
            read_choice = input("Total or Section Name: ")
            if read_choice.lower() == "total":
                for line in document_list[1:]:
                    print(line)
                    print("\n")
            if "{" + read_choice + "}" in sections:
                read_choice = "{" + read_choice + "}"
                section_to_read = []
                for line in document_list[1:]:
                    sentence = line.split()
                    section = []

                    for word in sentence:
                        if word == read_choice:
                            line_list = []
                            for word in sentence:
                                if word == read_choice:
                                    pass
                                else:
                                    line_list.append(word)
                                line_cleaned = " ".join(line_list)

                            section_to_read.append(line_cleaned)
                for line in section_to_read:
                    print(line)
                    print("\n")
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
                        val = bytes((str(val)), 'utf-8')
                        f.writelines(str(self.fernet_object.encrypt(val)) + "\n")

                    i += 1
            f.close()
        if choice.lower() == "quit":
            sys.exit()
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



#Add an append old documents feature for easy copy and paste