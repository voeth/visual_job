# Author:LiTing
def log_request(req,res):
    with open("vsearch.log","a") as log:
        print(req.form,remote_addr,request.user_agent)
