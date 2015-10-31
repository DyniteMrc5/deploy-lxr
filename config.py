import os
import sys
import subprocess
import p4_util

def current_versions(lxr):
  with open(lxr, 'rw') as file:
    content = file.readlines()
    nextLine = False
    for line in content:
      if nextLine:
        versions = line.split(' ')
        versions = [v.strip() for v in versions]
        return versions

      if "'range' => [qw(" in line:
        nextLine = True

  sys.exit("No versions found in {l}".format(l=lxr))

def new_changelists(current):
  latest = p4_util.read_latest()
  current = current.strip()

  if current == "":
    return latest

  versions = current.split(' ')
  lowest = versions[0]
  for v in versions:
    if int(v) < int(lowest):
      lowest = v

  versionsNum = []
  for v in versions:
    versionsNum.append(int(v))
  versionsNum.append(int(latest))

  srted = sorted(versionsNum)[-(p4_util.DEFAULT_MAX_SYNC-1):]
  srted.append(int(latest))
  srted = set(srted)

  output = ""
  for v in srted:
    if len(output) > 0:
      output = output + ' ' + str(v)
    else:
      output = output + str(v)

  return output + '\n'

def main(lxr, source_dir):
  print "main ({l}, {s})".format(l=lxr, s=source_dir)

  if not os.path.exists(lxr):
    print 'LXR not found'
    sys.exit(-1)

  dirs = [ f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]

  with open(lxr+'.new', 'w') as output:
    with open(lxr, 'rw') as file:
      content = file.readlines()
      nextLine = False
      for line in content:
        if nextLine:
          newoutput = new_changelists(line)
          becomes = " => " + newoutput
          print line + becomes
          output.write(newoutput)
          nextLine = False
          continue

        if "'range' => [qw(" in line:
          nextLine = True

        output.write(line)
  
  if os.path.exists("{l}.bak".format(l=lxr)):
    command = "sudo rm {l}.bak".format(l=lxr)
    print command
    subprocess.check_call(command, shell=True)

  command = "sudo mv {l} {l}.bak".format(l=lxr)
  print command
  subprocess.check_call(command, shell=True)

  command = "sudo mv {l}.new {l}".format(l=lxr)
  print command
  subprocess.check_call(command, shell=True)


if __name__ == "__main__":
  print __file__
  try:
    lxr = sys.argv[1]
    source_dir = sys.argv[2]
  except:
    print 'Usage: {f} <LXR_CONF> <SOURCE_DIR e.g. /home/lxr/Perforce/main> (where main contains /<changelist>)'.format(f=__file__)
    sys.exit(-1)
  main(lxr, source_dir)
