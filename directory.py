#!/usr/bin/python3.5
class directory:
    folders = {
        "root": {
            "etc": {},
            "home": {
                "user": {
                    "Downloads": {},
                    "Desktop": {},
                    "Documents": {}
                }
            },
            "var": {
                "www": {
                    "html":{}
                }
            }
        }
    }
    files = {
        0:{
            "name": "index.php",
            "content":"<html>\n<head>\n\t<title>This is a simple website</title>\n</head>\n<body>\n\t<h3 style='text-align:center'>Welcome to this Simple Website</h3>\n</body>\n</html>",
            "folder": "/var/www/html"
        },
        1:{
            "name": ".tmp",
            "content": "temp notes",
            "folder": "/home/user"
        },
        2:{
            "name": ".config",
            "content":"settings",
            "folder": "/root"
    }
    }