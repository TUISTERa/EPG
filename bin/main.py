# -*- coding: utf-8 -*-
import os
import sys
import git
import epg
from helper import *

log("Script execution started")
log("Bin dir: " + bindir)
log("Git dir: " + gitdir)
log("Logs dir: " + logdir)
log("Config dir: " + configdir)
log("Chaning dir to " + bindir)
os.chdir(bindir)
log("Current working dir: %s" % os.getcwd())


log("Generating platform specific version of wgmulti.exe.config")
content = ''
with open(wgexeconfig + '.tmpl', 'r') as f:
  content = f.read()

content = content.replace('$ConfigDir', configdir)
content = content.replace('$GrabbingTempFolder', temp)
content = content.replace('$ReportFolder', gitdir)
maxAsyncProcesses = '20' if os.name == 'nt' else '3'
content = content.replace('$MaxAsyncProcesses', maxAsyncProcesses)

with open(wgexeconfig, 'w') as w:
  w.write(content)

log("Generating wgmulti.exe.config finished!")

if len(sys.argv) > 1:
  if "-n" in sys.argv:
    commitEnabled = False
    log("Running with option -n: commit disabled")

  if "-d" in sys.argv:
    grabbingEnabled = False
    log("Running with option -d: demo mode, grabbing disabled")

### Pull online changes
if commitEnabled:
  log("Updating files in folder %s" % gitdir)
  repo = git.cmd.Git(gitdir)
  repo.pull()
  log("Updating files finished")

### Generate EPG
if grabbingEnabled:
  log("Generating EPG started")
  #epg.generate_config()
  epg.grab()
  epg.queryimdb()
  epg.remove_tags()
  epg.hash()
  epg.zip(final_epg_file)
  exported_files = epg.export_other_epgs()
  for file in exported_files:
    log("zipping file %s" % file)
    epg.zip(file)
  log("Generating EPG endeded")

else:
  log("Grabbing disabled. Skipping it.")

if commitEnabled:
  ### Push local changes
  log("Pushing local changes")
  files = repo.diff(None, name_only=True).split('\n')
  l = len(files)
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

    commitmsg = "Updating EPG"
    log("Executing 'git commit -m '%s'" % commitmsg)
    log("Pushing local files")
    ## add log file last
    repo.commit('-m', commitmsg)
    repo.push()

  try:
    from shutil import copyfile
    harrygg_dir = os.path.join(gitdir, '../harrygg.github.io/')
    log("Copying report to harrygg.github.io and commiting")
    copyfile(report_file, harrygg_dir + report_file)
    log(report_file + " copied to " + harrygg_dir)    
    log("Updating files in folder %s" % harrygg_dir)
    repo = git.cmd.Git(harrygg_dir)
    repo.pull()
    log("Updating files finished")
    log("Pushing local changes")
    files = repo.diff(None, name_only=True).split('\n')
    l = len(files)
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

      commitmsg = "Updating harrygg.github.io"
      log("Executing 'git commit -m '%s'" % commitmsg)
      log("Pushing local files")
      ## add log file last
      repo.commit('-m', commitmsg)
      repo.push()  
    
  except Exception as er:
    log("Error: " + er)

log("Finished!")
