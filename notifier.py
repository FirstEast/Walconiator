import gmail
import pyglet
import time

myLists=['free-food@mit.edu','reuse@mit.edu']
displayMail=[['a','b','c'] for i in range(5)]
'''
'''
__docformat__ = 'restructuredtext'
window = pyglet.window.Window(fullscreen=True)
pyglet.gl.glClearColor(1, 1, 1, 1)
notification = pyglet.media.load('target_acquired.wav', streaming=False)

def get_mail(user,passwd,list):
    g = gmail.login(user, passwd)
    emails=g.inbox().mail(unread=True, to=list)
    data=[]
    i=0
    currentMail=[]
    for email in emails:
        if(i==5):
            break
        email.fetch()
        email.read()
        if (email.thread_id==email.message_id and email.subject[:3]!="Re:"):
            print email.sent_at
            print email.subject
            print
            if list=='reuse@mit.edu':
                print email.body[:-142]
                currentMail.insert(0,[email.subject,email.body[:-142],email.sent_at])
            else:
                print email.body
                currentMail.insert(0,[email.subject,email.body,email.sent_at])
            print
            i+=1
    return currentMail

@window.event
def on_draw():
    window.clear()
    global displayMail
    for i in range(3):
        pyglet.text.Label(str(displayMail[i][2]),
                          font_name='Times New Roman',
                          font_size=14,
                          bold=True,
                          color=(80,1,255,255),
                          x=(1+2*i)*window.width/6, y=11.5/12.0*window.height,
                          width=600,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()
        pyglet.text.Label(displayMail[i][0],
                          font_name='Times New Roman',
                          font_size=14,
                          bold=True,
                          color=(80,1,255,255),
                          x=(1+2*i)*window.width/6, y=11/12.0*window.height,
                          width=600,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()
        pyglet.text.Label(displayMail[i][1],
                          font_name='Times New Roman',
                          font_size=12,
                          bold=True,
                          color=(1,1,1,255),
                          x=(1+2*i)*window.width/6, y=10/12.0*window.height,
                          width=600,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()

@window.event
def notifier(dt,eLists=myLists,loud=True):
    playMessage=False
    global displayMail
    for e in eLists:
        global displayMail
        newMail=get_mail('Walconiator','fuckthisshit7', e)
        if newMail!=[]:
            playMessage=True
        newMail.extend(displayMail)
        displayMail=newMail[:5]
    if playMessage:
        notification.play()
    print displayMail


pyglet.clock.schedule_interval(notifier, 10)
pyglet.app.run()


        
    
