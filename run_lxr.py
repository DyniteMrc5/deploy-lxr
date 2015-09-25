import os
import subprocess

if __name__ == '__main__':
  print __file__
  print os.system('date')

  command = 'sudo /etc/lxr-2.0.3/genxref --url=http://localhost/lxr --version=448276'
  print command
  subprocess.check_call(command, shell=True)
  print os.system('date')