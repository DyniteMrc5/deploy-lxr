import os, sys
import subprocess
import urllib
import extract_tar
from with_cd import cd
import shutil

DEFAULT_MAX_SYNC=5

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


def check_p4():
  try:
    p4user = os.environ['P4USER']
  except:
    print 'Set P4USER environment variable'
    sys.exit(-1)

  try:
    p4pass = os.environ['P4PASSWD']
  except:
    print 'Set P4PASSWD environment variable'
    sys.exit(-1)

def write_latest(changelist):
  with open('perforce_latest.plist', 'w') as plist:
    print 'Writing {f}'.format(f=plist.name)
    plist.write('LATEST={c}'.format(c=changelist))

def read_latest():
  try:
    with open('perforce_latest.plist', 'r') as plist:
      data = plist.read()
      changelist = data.split('=')[1]
      return changelist
  except:
    return 0

def cleanup_oldest():
  path = '/home/lxr/Perforce/main'
  dirs = [ f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
  number = len(dirs)
  if number > DEFAULT_MAX_SYNC:
    oldest = min(dirs)
    print "{c} changelists sync'd - deleting oldest ({o})".format(c=number, o=oldest)
    shutil.removetree(oldest)

def main():
  check_p4()

  print 'Setup p4'
  setup_p4()

  print 'Get latest server changelist'
  changelist = get_latest_changelist()

  print "Get latest sync'd chagnelist"
  latest = read_latest()

  if(latest >= changelist):
    print 'Already have latest'
  else:
    print 'Setup p4 clientspec'
    setup_p4_client(changelist)

    print 'Sync'
    sync(changelist)

    print 'Write latest to file'
    write_latest(changelist)

    latest = changelist

  print 'Try cleanup'
  cleanup_oldest()

  print 'LATEST={l}'.format(l=latest)
  return latest

if __name__ == '__main__':
  print __file__
  main()


