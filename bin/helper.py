# -*- coding: utf-8 -*-

import os
import sys
import git
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
report_file    = os.path.join(gitdir, "report.html")
config_file    = os.path.join(configdir, "wgmulti.config.json")

commitEnabled  = True
grabbingEnabled = True

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

def commit(folder, commitmsg = None):
  ### Push local changes
  log("Commiting local changes from folder %s" % folder)
  repo = git.cmd.Git(folder)
  files = repo.diff(None, name_only=True).split('\n')
  l = len(files)
  log(l)
  if l == 0:
    log("No files were modified")
  elif l == 1:
    if files[0] != "":
      log("1 file was modified")
  else:
    log("%s files were modified" % l)

  if l > 0 and files[0] != "":
    for f in files:
      log("Executing 'git add %s'" % f)
      repo.add(f)

    if commitmsg == None:
      commitmsg = "Scheduled update"

    log("Executing 'git commit -m '%s'" % commitmsg)
    repo.commit('-m', commitmsg)
    log("Pushing local files")
    repo.push()
    log("Files uploaded!")


