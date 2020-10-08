from makeMail import MIMEmail
import time
import random


if __name__== "__main__":

    path = "mails_pop3/pop5.json"
    try:
    print(path)
        oneMail = MIMEmail()
        oneMail.load_pop3(path)
        oneMail.getByPOP3()
    except BaseException as e:
        print("Failed ", e)
    else:
        print("Success！")


   
