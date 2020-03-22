# -*- coding: utf-8 -*-

import os
import sys
import datetime

bindir         = os.path.dirname(os.path.realpath(__file__))
gitdir         = os.path.dirname(os.path.realpath('.'))
logdir         = os.path.join(gitdir, "logs")
configdir      = os.path.join(gitdir, "config")
temp           = os.path.join(gitdir, "temp")
logfile        = os.path.join(logdir, "log.txt")
mapsfile       = os.path.join(gitdir, "maps", "channels-tvbg.json")
wgexeconfig    = os.path.join(bindir, 'wgmulti.exe.config')
wglogfile      = os.path.join(logdir, "run.log.txt")
wgmulti        = os.path.join(bindir, "wgmulti.exe")
epg_file       = os.path.join(configdir, "epg.xml")
final_epg_file = os.path.join(gitdir, "epg.xml")
config_file    = os.path.join(configdir, "wgmulti.config.json")

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
