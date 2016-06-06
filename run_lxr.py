import os
import sys
import subprocess
from with_cd import cd
import p4_util
import config

if __name__ == '__main__':
  print __file__
  print os.system('date')

  lxr = '/etc/lxr-2.0.3/lxr.conf'

  latest = p4_util.main()
  
  if latest in config.current_versions(lxr):
    print 'Config already processed'
    sys.exit(0)

  config.main(lxr,'/home/lxr/Perforce/main')

  with cd('/etc/lxr-2.0.3') as dir:
    command = './genxref --url=http://lxr/lxr --allversions'
    print command
    subprocess.check_call(command, shell=True)

  print os.system('date')
