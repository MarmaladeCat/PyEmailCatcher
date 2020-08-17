
from allinOne import sendmail
import time
import random

if __name__ == "__main__":

    i = 1
    print("send qq mails begin")
    while i < 22:
        path = './mails/mail'+str(i)+'.json'
        x = random.randint(1, 4)
        if x != 1:
            path = './mails/mail'+str(1)+'.json'

        else:
            path = './mails/mail'+str(i)+'.json'
            i = i+1
        print("prepare to send %s ---------------->\t " % path, end="")
        time.sleep(random.randint(3, 8))

        try:
            sendmail(path)
        except BaseException as e:
            print("Failed ", e)
        else:
            print("Success！")

    print("send qq mails end\n")

    print("send 163 mails begin")
    i = 1
    while i < 22:
        path = './mails/mail'+str(i)+'.json'
        x = random.randint(1, 4)
        if x != 1:
            path = './mails/mail'+str(1)+'.json'

        else:
            path = './mails_163/mail'+str(i)+'.json'
            i = i+1
        print("prepare to send %s ---------------->\t " % path, end="")
        time.sleep(random.randint(3, 8))

        try:
            sendmail(path)
        except BaseException as e:
            print("Failed ", e)
        else:
            print("Success！")

    print("send 163 mails end\n")
