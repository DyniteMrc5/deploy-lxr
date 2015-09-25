import os, sys
import subprocess
import urllib
import extract_tar
from with_cd import cd
import shutil

def download_p4():
  urllib.urlretrieve('http://cdist2.perforce.com/perforce/r10.2/bin.linux26x86_64/p4', 'p4')

def setup_p4():
  command = "chmod a+rx p4"
  print command
  subprocess.check_call(command, shell=True)

def get_latest_changelist():
  #-m for max 1. so just gets the latest
  command = "./p4 changes -m 1 //depot/sdk/main/..."
  print command
  output = subprocess.check_output(command, shell=True)
  changelist = output.split(' ')[1]
  return changelist

def setup_p4_client(changelist):
  client = """
Client: lxr

Owner:  mcox

Host:   lxr

Description:
        Created by mcox.

Root:   /home/lxr/Perforce

Options:        noallwrite noclobber nocompress unlocked nomodtime normdir

LineEnd:        local

View:
        //depot/sdk/main/... //lxr/main/{c}/...
""".format(c=changelist)

  print client
  command = "./p4 client -i"
  pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
  output = pipe.communicate(input=client)[0]
  print output.decode()

def sync(changelist):
  command = './p4 sync -f //depot/sdk/main/...@{c}'.format(c=changelist)
  print command
  subprocess.check_call(command, shell=True)


if __name__ == '__main__':
  print __file__

  print 'Setup p4'
  setup_p4()

  print 'Setup p4 clientspec'
  changelist = get_latest_changelist()
  setup_p4_client(changelist)

  print 'Sync'
  sync(changelist)
