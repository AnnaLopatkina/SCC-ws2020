from flask import session

service_ip = "localhost"
userservice_ip = "localhost"
service_port = "5000"
userservice_port = "5001"

# API Version when working with real service
api_version = "api"

# api_version = "test/api"

headers = {
    "Accept-Encoding": "gzip",
    "User-Agent": "Web-Client"
}

# When db is created, set admin:

# username / email:

admin_username = "admin"
admin_email = "admin@fwao.de"
admin_password = "admin"

admin_api_password = "superadmin"
