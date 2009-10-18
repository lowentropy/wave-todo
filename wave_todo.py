import re, logging

from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document

TODO_RE = re.compile('TODO:[ \t]*([^.!]+)[.!]', re.I)

def OnBlipSubmitted(properties, context):
	blip = context.GetBlipById(properties['blipId'])
	doc = blip.GetDocument()
	text = doc.GetText()
	for m in TODO_RE.finditer(text):
		doc.DeleteRange(document.Range(m.start(), m.end()))
		doc.InsertText(m.start(), 'I found: "' + m.groups()[0] + '"')

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.DEBUG)
  todo = robot.Robot('wave-todo', 
      image_url='http://wave-todo.appspot.com/assets/icon.png',
      version='2',
      profile_url='http://wave-todo.appspot.com/')
  todo.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  todo.Run()
