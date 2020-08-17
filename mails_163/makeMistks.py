import json
import random
import copy


def str_cg(str1):
    a = bytearray(str1, "UTF-8")

    x = random.randint(0, len(str1)-1)
    a[x] = a[x] ^ 0x01
    str2 = a.decode(encoding="UTF-8 ")
    return str2


#
if __name__ == "__main__":
    for i in range(1, 22):
        with open('./mail%d.json' % i, "r") as f:
            MailConfig = json.load(f)
            MailConfig["basic"]["host"] = "smtp.***.com"
            MailConfig["basic"]["authMail"] = "********@**.com"
            MailConfig["basic"]["fromMail"] = "********@**.com"
            MailConfig["basic"]["authPasswd"] = "*************"
            MailConfig["basic"]["toMail"]["to1"] = "*************"
            MailConfig["basic"]["toMail"]["to2"] = "*************"
            MailConfig["basic"]["Cc"]["to1"] = "*************"
            
        with open('./mail%d.json' % i, "w+") as f:
            json.dump(MailConfig, f)
