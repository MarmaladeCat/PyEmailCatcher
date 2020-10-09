
from makeMail import MIMEmail
import time
import random

if __name__ == "__main__":
    themes = ["126","sina"]
    for theme in themes:
        i = 1
        print("send %s mails begin" % theme)
        while i < 24:

            x = random.randint(1, 4)
            if x != 1:
                x=1
            else:
                x=i
                i = i+1
            path = './mails_%s/mail%d.json' % (theme,x)
            print(time.asctime(),end="\t")
            print("prepare to send %s ---------------->\t " % path, end="")
            if theme == theme[1]:
                time.sleep(random.randint(240,360))
            else:
                time.sleep(random.randint(120,180))

            try:
                # print(path)
                oneMail = MIMEmail()
                oneMail.loadConfigFromJson(path)
                oneMail.sendBySMTP()
            except BaseException as e:
                print("Failed ", e)
            else:
                print("Success！")

        print("send %s mails end\n" % theme)

   
