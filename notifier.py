import gmail
import time

myLists=['free-food@mit.edu','reuse@mit.edu']

def get_mail(user,passwd,list):
    g = gmail.login(user, passwd)
    emails=g.inbox().mail(unread=True, to=list)
    data=[]
    i=0
    for email in emails:
        if(i==5):
            break
        email.fetch()
        email.read()
        if email.thread_id==email.message_id:
            print email.subject
            print email.body
            i+=1
    return True

def notifier(eLists,loud=True):
    while(True):
        for e in eLists:
            get_mail('user','pass', e)
        time.sleep(20)
notifier(myLists,loud=False)



        
    
