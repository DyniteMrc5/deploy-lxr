import os, sys, tarfile

def extract(tar, extract_path='.'):
  print tar
  try:
    file = tarfile.open(tar, 'r:gz')
  except:
    file = tarfile.open(tar, 'r')
  file.extractall(extract_path)

if __name__ == '__main__':
  try:
    extract(sys.argv[1])
  except:
    print "Usage: {f} <tar file>".format(f=__file__)