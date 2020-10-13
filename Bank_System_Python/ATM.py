import datetime
import random

class Bank:

    __Account_holders={}

    def __init__(self,name,contact):
        self.Bank_Name=name
        self.Bank_Contact=contact

    def _checkPin(self,Account_Number,Pin):
        Atm_pin=self.__Account_holders[Account_Number].Atm_pin
        if(Atm_pin==Pin):
            return True
        else:
            return False


    def RegisterNewAccount(self,Account_Data):
        New_Account = Account(Account_Data["A_No"],Account_Data["A_H_Name"],Account_Data["A_H_Mb_No"],Account_Data["A_Ini_Bal"],Account_Data["Pin"])
        self.__Account_holders[Account_Data["A_No"]]=New_Account

    def RegisterMultiAccount(self,Datum):
        for Data in Datum:
            self.RegisterNewAccount(Data)
    
    def _BankAcounts(self):
        Accounts=self.__Account_holders.keys()
        return Accounts
    
    def _AccountBalance(self,Account_Number):
        Balance=self.__Account_holders[Account_Number].TotalBalance
        return Balance

    def _WithdrawAmount(self,Account_Number,withdraw_Amount):
        Time=str(datetime.datetime.now())[:19]
        Account_Balance=self._AccountBalance(Account_Number)
        if(withdraw_Amount<Account_Balance):
            Account_Balance-=withdraw_Amount
            self.__Account_holders[Account_Number].TotalBalance=Account_Balance
            return "Your Account Number {} is debited by Rs. {} on {}.\nAvailable Balance : Rs. {}.\nInfo : {}, Contact {} for more info".format("X"*(len(str(Account_Number))-3)+str(Account_Number)[-3:],withdraw_Amount,Time,Account_Balance,self.Bank_Name,self.Bank_Contact)
        else:
            return "Your Account Number {} doesn't have sufficient balance ( {} ).\nAvailable Balance : Rs. {}.\nInfo : {}, Contact {} for more info".format("X"*(len(str(Account_Number))-3)+str(Account_Number)[-3:],Time,Account_Balance,self.Bank_Name,self.Bank_Contact)

    def _help(self):
        print("{:^100s}".format(self.Bank_Name+" Help Menu "+", Contact Number - "+str(self.Bank_Contact)))
        print("-> {:50s} {:50s}".format("Would you like to connect your account with "+self.Bank_Name,", Press 'Y' for Yes :- "),end="")
        user_input=input().upper()
        if(user_input=="Y"):
            self._OpenBankForum()
    
    def _OpenBankForum(self):
        print("\n{:^100s}\n".format(self.Bank_Name+" Registration Form "+", Contact Number - "+str(self.Bank_Contact)))
        Account_Holder=input("Enter Your Name :- ")
        if(Account_Holder==""):
            print("\nError ! Invalid Name ")
            return
        try:
            Contact_Number=int(input("\nEnter Your Contact Number :- "))
            if(len(str(Contact_Number))!=10):
                print("\n Error ! Invalid Mobile Number")
                return
        except:
            print("\n Error ! Invalid Mobile Number")
            
        try:
            Initial_Bal=int(input("\nEnter Initial Balance ( Your Initial Balance must be greater than Rs . 500.00 ) :- "))
            if(Initial_Bal<500):
                print("\n Error ! Your Initial Balance must be greater than Rs . 500.00 ")
                return
        except:
            print("\n Error ! Invalid Amount")
            return

        Account_Num=int("191520"+str(random.randint(100,999)))
        while(Account_Num in self.__Account_holders):
            Account_Num=int("191520"+str(random.randint(100,999)))
        
        print("\nCongratulations ! Your Account has successfully created .")
        print("\nAccount_holder :- {}\nAccount_Number :- {}\nContact_Number :- {}\nTotal_Balance :- Rs. {}.0".format(Account_Holder,Account_Num,Contact_Number,Initial_Bal))
        Data={"A_No":Account_Num,"A_H_Name":Account_Holder,"A_H_Mb_No":Contact_Number,"A_Ini_Bal":Initial_Bal}
        self.RegisterNewAccount(Data)
        


class ATM(Bank):

    def __init__(self,Account_Number,Bank):
        print("\n{:50s}".format(Bank.Bank_Name))
        if(Account_Number in Bank._BankAcounts()):
            print()
            print("{:^100s}".format("Welcome to "+Bank.Bank_Name))
            self.__ShowService(Bank,Account_Number)
        else:
            print("\n{:^100s}".format("Your Account doesn't exist in "+Bank.Bank_Name))
            User_Input=input("\nMay I help You ! Press 'Y' for yes :- ")
            if(User_Input.upper()=="Y"):
                Bank._help()
            else:
                print("\n{:^100s}\n".format("Thanks for using "+Bank.Bank_Name))
    
    def __ShowService(self,Bank,Account_Number):
        print("\n{:^100s}".format(Bank.Bank_Name+" Services "))
        print("-> {:50s}\n-> {:50s}".format("Press '1' for Withdrawl","Press '2' for Check Balance"))
        try:
            user_Input=int(input("-> Enter Your Input :- "))
            show=True
            if(user_Input==1):
                try:
                    withdraw_Amount=float(input("\nEnter Withdrawl Amount in INR :- "))
                    if(withdraw_Amount>0):
                        self.__Withdraw(Bank,withdraw_Amount,Account_Number)
                    else:
                        print("\n{:^20s}".format("Error ! Invalid Amount "))   
                except:
                    print("\n{:^20s}".format("Error ! Invalid Amount "))
            elif(user_Input==2):
                self.__ShowBalance(Bank,Account_Number)
        except:
            User_Input=input("\nDo you want service menu again? Press 'Y' for yes :- ")
            if(User_Input.upper()=="Y"):
                show=False
                self.__ShowService(Bank,Account_Number)
            else:
                show=True
        finally:
            if(show):
                print("\n{:^100s}".format("Thanks for using "+Bank.Bank_Name))


    def __Withdraw(self,Bank,withdraw_Amount,Account_Number):
        print("\n{:^10s}".format("Withdrawing ... \n"))
        chance=3
        is_correct=False
        while(chance>0 and not is_correct):
            try:
                Pin=int(input("\nEnter Your ATM Pin : - "))
            except:
                return
            is_correct=self._checkPin(Account_Number,Pin)
            if(is_correct==False):
                print("\nError ! Invalid Pin Number ")
            chance-=1
        if(is_correct):
            print(Bank._WithdrawAmount(Account_Number,withdraw_Amount))

    def __ShowBalance(self,Bank,Account_Number):
        print("\n{:^10s}".format("Showing Balance ... \n"))
        Time=str(datetime.datetime.now())[:19]
        print("Your Account Number {} has Available Balance : Rs. {} , Time :- {}".format("X"*(len(str(Account_Number))-3)+str(Account_Number)[-3:],Bank._AccountBalance(Account_Number),Time))
    
class Account():
    
    def __init__(self,Account_Number,Account_holder,Mobile_Number,Initial_Balance,Atm_Pin):
        self.Account_Number=Account_Number
        self.Account_holder=Account_holder
        self.Mobile_Number=Mobile_Number
        self.Initial_Balance=Initial_Balance
        self.TotalBalance=Initial_Balance
        self.Atm_pin=Atm_Pin

if __name__ == "__main__":

    Banks={"Python Bank":Bank("Python Bank",3384934),"Java Bank":Bank("Java Bank",3924934),"C Bank":Bank("C Bank",3423844),"C++ Bank":Bank("C++ Bank",3974933),"C# Bank":Bank("C# Bank",3924934)}

    Bank_Data=[{"A_No":191520016,"A_H_Name":"Pratham Kumar","A_H_Mb_No":378349223,"A_Ini_Bal":5000,"Pin":2001},{"A_No":191520005,"A_H_Name":"Ankit Yadav","A_H_Mb_No":9393237492,"A_Ini_Bal":4000,"Pin":2001},{"A_No":191520023,"A_H_Name":"Sudhir Gupta","A_H_Mb_No":9393237222,"A_Ini_Bal":4500,"Pin":2001},{"A_No":191520018,"A_H_Name":"Sachin Maurya","A_H_Mb_No":9393248492,"A_Ini_Bal":4500,"Pin":2001},{"A_No":191520013,"A_H_Name":"Kritagya Chopra","A_H_Mb_No":837391492,"A_Ini_Bal":5000,"Pin":2001}]
    
    for bank in Banks.keys():
        Banks[bank].RegisterMultiAccount(Bank_Data)
    
    print("\n{:^100s}\n{:10s}\n\n{:20s} {:10s}\n".format("Welcome to Bank System","Bank list :- ","Bank Name","Bank Contact Number"))

    Bank_list={}
    for num,bank_name in enumerate(Banks.keys()):
        print("{}. {:20s} {:10d}".format(num+1,bank_name,Banks[bank_name].Bank_Contact))
        Bank_list[num+1]=bank_name
    try:
        user_input=int(input("\nChoose Your Bank :- "))
        if(user_input>=1 and user_input<=5):
            try:
                Account_Number=int(input("Enter Your Account Number :- "))
                Bank_Atm=ATM(Account_Number,Banks[Bank_list[user_input]])
            except:
                print("\nError ! Invalid Account Number (Account Number must be an integer ) Can't connect to {}".format(Bank_list[user_input]))
        else:
            print("\nError! Invalid Bank")
    except:
        print("\nError! Invalid Bank")
    finally:
        print("\n{:^100s}\n".format("Thanks for using my Bank System "))
