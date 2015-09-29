import os
import subprocess
from with_cd import cd
import p4_util
import config

if __name__ == '__main__':
  print __file__
  print os.system('date')

  latest = p4_util.main()

  with cd('/etc/lxr-2.0.3') as dir:
    command = './genxref --url=http://lxr/lxr --version={cl}'.format(cl=latest)
    print command
    subprocess.check_call(command, shell=True)

  config.main('/etc/lxr-2.0.3/lxr.conf','/home/lxr/Perforce/main')

  print os.system('date')