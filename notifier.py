import gmail
import pyglet
import time
import urllib
import urllib2
from pygame import mixer

##import pyttsx
myLists=['free-food@mit.edu','reuse@mit.edu','vultures@mit.edu']
mixer.init(16000)
mixer.music.load('welcome.wav')
mixer.music.play()
newMail=[]
allMail=[['subject','message','time'] for i in range(3)]
'''
'''
__docformat__ = 'restructuredtext'
window = pyglet.window.Window(fullscreen=True)
pyglet.gl.glClearColor(1, 1, 1, 1)

def get_mail(user,passwd,list):
    g = gmail.login(user, passwd)
    emails=g.inbox().mail(unread=True, to=list)
    data=[]
    i=0
    currentMail=[]
    for email in emails:
        if(i==3):
            break
        email.fetch()
        email.read()
        if (email.thread_id==email.message_id and email.subject[:3]!="Re:"):
            if list=='reuse@mit.edu':
                currentMail.insert(0,[email.subject,email.body,email.sent_at])
            else:
                currentMail.insert(0,[email.subject,email.body,email.sent_at])
            i+=1
    return currentMail

@window.event
def on_draw(allMail=allMail):
    global newMail
    print "draw"
    window.clear()
    displayMail=allMail[:3]
    pyglet.text.Label('The Walconiator 2.0',
                      font_name='Helvetica',
                      font_size=30,
                      bold=True,
                      italic=True,
                      color=(145,7,122,255),
                      x=220, y=window.height-30,
                      width=9*window.width/30,
                      anchor_x='center', anchor_y='top').draw()
    for i in range(3):
        pyglet.text.Label(str(displayMail[i][2]),
                          font_name='Helvetica',
                          font_size=14,
                          bold=True,
                          color=(178,1,1,255),
                          x=(1+2*i)*window.width/6, y=11.5/12.0*window.height-50,
                          width=9*window.width/30,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()
        pyglet.text.Label(displayMail[i][0],
                          font_name='Helvetica',
                          font_size=14,
                          bold=True,
                          color=(178,1,1,255),
                          x=(1+2*i)*window.width/6, y=11/12.0*window.height-50,
                          width=9*window.width/30,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()
        pyglet.text.Label(displayMail[i][1],
                          font_name='Helvetica',
                          font_size=12,
                          bold=True,
                          color=(1,1,1,255),
                          x=(1+2*i)*window.width/6, y=10/12.0*window.height-50,
                          width=9*window.width/30,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()
    if not(newMail==[]):
        voicePlayer(newMail)
        newMail=[]
        

def voicePlayer(newMail):
    print "voice"
    queue=[]
    checker=[]
    for mail in newMail:
        checker.append(mail[0])
    while(len(checker)>0):
        print "checker length", len(checker)
        packets=[]
        text=checker[0]
        if len(text)>90:
            i=60
            while(text[i]!=' 'and i<len(text)-2):
                i+=1
            if i==len(text)-1:
                queue.append(urllib.quote_plus(text))
                checker.pop(0)          
            else:
                queue.append(urllib.quote_plus(text[0:i]))
                checker[0]=text[i+1:]         
        else:
            queue.append(urllib.quote_plus(text))
            checker.pop(0)
    while(mixer.music.get_busy()):
        time.sleep(0.01)
    mixer.music.load('feeling.wav')
    mixer.music.play()
    for i in range(len(queue)):
        while(mixer.music.get_busy()):
            time.sleep(0.01)
        url = "https://translate.google.com/translate_tts?tl=en&q="+queue[i]
        request = urllib2.Request(url)
        request.add_header('User-agent', 'Mozilla/30.0') 
        opener = urllib2.build_opener()
        f = open("data"+str(i)+".mp3", "wb")
        f.write(opener.open(request).read())
        f.close()
        mixer.music.load("data"+str(i)+".mp3")
        mixer.music.play()
        
@window.event
def notifier(dt,eLists=myLists,loud=True):
    global allMail
    global newMail
    print "notify"
    if mixer.get_busy()==False:
        print "not busy"
        playMessage=False
        for e in eLists:
            try:
                mails=get_mail('user','pass', e)
            except:
                print "auth error"
                mails=[]
            for mail in mails:
                allMail.insert(0,mail)
                newMail.insert(0,mail)

##engine = pyttsx.init()
##engine.say("Cruft..... One. An old piece of computer equipment, possibly useless, that keeps hanging around. Two. An old alum. Reuse. This is where you find it.")
##engine.runAndWait()
pyglet.clock.schedule_interval(notifier, 10)
pyglet.app.run()


        
    
