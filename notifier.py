import gmail
import pyglet
import time
import urllib
import urllib2

##import pyttsx
myLists=['free-food@mit.edu','reuse@mit.edu']
displayMail=[['a','b','c'] for i in range(5)]
'''
'''
__docformat__ = 'restructuredtext'
window = pyglet.window.Window(fullscreen=True)
music = pyglet.media.Player()
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
                currentMail.insert(0,[email.subject,email.body[:-142],email.sent_at])
            else:
                currentMail.insert(0,[email.subject,email.body,email.sent_at])
            i+=1
    return currentMail

@window.event
def on_draw():
    window.clear()
    global displayMail
    for i in range(3):
        pyglet.text.Label(str(displayMail[i][2]),
                          font_name='Helvetica',
                          font_size=14,
                          bold=True,
                          italic=True,
                          color=(178,1,1,255),
                          x=(1+2*i)*window.width/6, y=11.5/12.0*window.height,
                          width=9*window.width/30,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()
        pyglet.text.Label(displayMail[i][0],
                          font_name='Helvetica',
                          font_size=14,
                          bold=True,
                          color=(178,1,1,255),
                          x=(1+2*i)*window.width/6, y=11/12.0*window.height,
                          width=9*window.width/30,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()
        pyglet.text.Label(displayMail[i][1],
                          font_name='Helvetica',
                          font_size=12,
                          bold=True,
                          color=(1,1,1,255),
                          x=(1+2*i)*window.width/6, y=10/12.0*window.height,
                          width=9*window.width/30,
                          multiline=True,
                          anchor_x='center', anchor_y='top').draw()

def voicePlayer(newMail):
    queue=[]
    checker=[]
    global music
    for mail in newMail:
        checker.append(mail[0])
    while(len(checker)>0):
        print "checker length", len(checker)
        packets=[]
        text=checker[0]
        if len(text)>40:
            i=20
            while(text[i]!=' 'and i<len(text)-2):
                i+=1
            if i==len(text)-1:
                print text
                queue.append(urllib.quote_plus(text))
                checker.pop(0)          
            else:
                print text[0:i]
                queue.append(urllib.quote_plus(text[0:i]))
                checker[0]=text[i+1:]         
        else:
            print text
            queue.append(urllib.quote_plus(text))
            checker.pop(0)
    music = pyglet.media.Player()  
    for text in queue:
        print text
        url = "https://translate.google.com/translate_tts?tl=en&q="+text
        request = urllib2.Request(url)
        request.add_header('User-agent', 'Mozilla/30.0') 
        opener = urllib2.build_opener()
        f = open("data.mp3", "wb")
        f.write(opener.open(request).read())
        f.close()
        source = pyglet.media.load('data.mp3')
        music.queue(source)
    feeling=pyglet.media.load('feeling.wav')
    music.queue(feeling)
    music.play()
    
@window.event
def notifier(dt,eLists=myLists,loud=True):
    if music.playing==False:
        playMessage=False
        global displayMail
        for e in eLists:
            newMail=get_mail('user','pass', e)
            if newMail!=[]:
                oldMail=displayMail
                displayMail=[x for x in newMail]
                displayMail.extend(oldMail)
                displayMail=displayMail[:5]
                voicePlayer(newMail)

##engine = pyttsx.init()
##engine.say("Cruft..... One. An old piece of computer equipment, possibly useless, that keeps hanging around. Two. An old alum. Reuse. This is where you find it.")
##engine.runAndWait()
pyglet.clock.schedule_interval(notifier, 10)
pyglet.app.run()


        
    
