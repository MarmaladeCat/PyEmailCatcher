# SMTPcatch
python send emails 


use smtp protocal


allinone.py: send email(use configFile)


smtpCatcher.py:send emails (ignore ERROR)



Example of email configFile:


json file 


// Comments


```
{
    // basic part 
    "basic": {
        "host": "smtp.****.com",
        "port": 25,
        "authMail": "********@****.com",
        "authPasswd": "***********",
        "fromMail": "************@****.com",
        "toMailNum": 2,
        // tomail can be one or more
        "toMail": {
            "to1": "**********@***.com",
            "to2": "************@****.com"
        },
        // Cc can be one or more
        "Cc": {
            "to1": "**************@***.com"
        },
        "subject": "The subject of email"
    },
    // content can be html or plainText
    "content": {
        "contentNum": 1,
        "contentPart": {
            "id2-example": {
                "contentType": "html",
                "path": "./content3.html"
            }
        }
    },

    // images shown in html
    "image": {
        "imageNum": 2,
        "imagePath": {
            "id1": {
                // desc is cid in html
                "desc": "image01",
                "path": "./image1.jpeg"
            },
            "id2": {
                "desc": "image02",
                "path": "./image2.jpeg"
            }
        }
    },

    // attachments can be one file or more
    "attachment": {
        "attachNum": 2,
        "attachPath": {
            "id1": {
                "desc": "atta1.pdf",
                "path": "./att1.pdf"
            },
            "id2": {
                "desc": "atta2.cpp",
                "path": "./att2.cpp"
            }
        }
    }
}

```