# -*- coding: utf-8 -*-
import os
import re
import sys
import datetime

#reload(sys)
#sys.setdefaultencoding('utf-8')

bindir         = os.path.dirname(os.path.realpath(__file__))
gitdir         = os.path.dirname(os.path.realpath('.'))
logdir         = os.path.join(gitdir, "logs")
configdir      = os.path.join(gitdir, "config")
temp           = os.path.join(gitdir, "temp")
logfile        = os.path.join(logdir, "log.txt")
mapsfile       = os.path.join(gitdir, "maps", "channels-tvbg.json")
wgexeconfig    = os.path.join(bindir, 'wgmulti.exe.config')
wglogfile      = os.path.join(logdir, "run.log.txt")

#wgpath         = os.environ.get("wgpath")
#if not wgpath:
#  print ("wgpath environment variable not set")
#  sys.exit()
#wgmulti        = os.path.join(wgpath, "wgmulti.exe")
wgmulti        = os.path.join(bindir, "wgmulti.exe")
epg_file       = os.path.join(configdir, "epg.xml")
final_epg_file = os.path.join(gitdir, "epg.xml")
commitEnabled  = True

if not os.path.exists(logdir):
  os.makedirs(logdir)

if os.path.isfile(logfile):
  os.remove(logfile)
#sys.stdout = open(logfile, "w")

def log(msg):
  text = "%s | %s" % (datetime.datetime.now(), msg)
  #with open(logfile, "a") as w:
  #  w.write(text + "\n")
  print(text)

log("Script execution started")
log("Bin dir: " + bindir)
log("Git dir: " + gitdir)
log("Logs dir: " + logdir)
log("Config dir: " + configdir)
log("Chaning dir to " + bindir)
os.chdir(bindir)
log("Current working dir: %s" % os.getcwd())


log("Generating wgmulti.exe.config")

content = ''
with open(wgexeconfig + '.tmpl', 'r') as f:
  content = f.read()

content = content.replace('$ConfigDir', configdir)
content = content.replace('$GrabbingTempFolder', temp)
content = content.replace('$ReportFolder', logdir)
content = content.replace('$MaxAsyncProcesses', '3')

with open(wgexeconfig, 'w') as w:
  w.write(content)
