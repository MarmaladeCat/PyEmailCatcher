
from makeMail import MIMEmail
import time
import random

if __name__ == "__main__":

    theme = "qq"
    i = 1
    print("send qq mails begin")
    while i < 24:

        x = random.randint(1, 4)
        if x != 1:
            x=1
        else:
            x=i
            i = i+1
        path = './mails_%s/mail%d.json' % (theme,x)

        print("prepare to send %s ---------------->\t " % path, end="")
        # time.sleep(random.randint(3, 8))

        try:
            # print(path)
            oneMail = MIMEmail()
            oneMail.loadConfigFromJson(path)
            oneMail.sendBySMTP()
        except BaseException as e:
            print("Failed ", e)
        else:
            print("Success！")

    print("send qq mails end\n")

   
