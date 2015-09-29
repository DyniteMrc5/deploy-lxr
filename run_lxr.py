import os
import subprocess
from with_cd import cd

if __name__ == '__main__':
  print __file__
  print os.system('date')

  with cd('/etc/lxr-2.0.3') as dir:
    command = './genxref --url=http://localhost/lxr --version=448276'
    print command
    subprocess.check_call(command, shell=True)
  print os.system('date')