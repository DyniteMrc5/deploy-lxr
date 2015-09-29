import os
import sys
import p4_util

def new_changelists(current):
  latest = p4_util.read_latest()
  current = current.strip()

  if current == "":
    return latest

  versions = current.split(',')
  lowest = versions[0]
  for v in versions:
    if int(v) < int(lowest):
      lowest = v

  output = ""
  for v in versions:
    if not v == lowest:
      if len(output) > 0:
        output = output + ', ' + v
      else:
        output = output + v

  if len(output) > 0:
    output = output + ', ' + str(latest)
  else:
    output = str(latest)
  return output

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


if __name__ == "__main__":
  print __file__
  try:
    lxr = sys.argv[1]
    source_dir = sys.argv[2]
  except:
    print 'Usage: {f} <LXR_CONF> <SOURCE_DIR e.g. /home/lxr/Perforce/main> (where main contains /<changelist>)'.format(f=__file__)
    sys.exit(-1)
  main(lxr, source_dir)
