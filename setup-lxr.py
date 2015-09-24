import os, sys
import subprocess
import urllib
import extract_tar
from with_cd import cd
import shutil

def check_executable(executable):
  check = "type {c}".format(c=executable)
  return subprocess.call(check, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def configure_make_install(setup_premake, options):
    print os.getcwd()
    if setup_premake:
      print 'Running pre-make step'
      setup_premake()
    configure = "./configure{o}".format(o=options)
    subprocess.check_call(configure, shell=True)
    make = "make"
    subprocess.check_call(make, shell=True)
    make_install = "sudo make install"
    subprocess.check_call(make_install, shell=True)

def setup(executable, target_dir, filename, source_url, options, setup_make=None, setup_premake=None):
  if executable:
    if not check_executable(executable):
      print '{e} not found'.format(e=executable)
  if not os.path.isdir(target_dir):
    print 'Downloading'
    if filename.endswith(".git"):
      command = 'git clone --depth 1 {u}'.format(u=source_url)
      print command
      subprocess.check_call(command, shell=True)
    else:
      urllib.urlretrieve(source_url, filename)
      extract_tar.extract(filename, '.')
  with cd(target_dir) as dir:
    if setup_make:
      setup_make(setup_premake, options)
    else:
      print 'No setup_make for {e}'.format(e=executable)

def setup_ctags():
  executable = "ctags"
  target_dir = 'ctags-5.8'
  filename = "{t}{e}".format(t=target_dir, e='.tar.gz')

  source_url = 'http://prdownloads.sourceforge.net/ctags/{f}'.format(f=filename)
  options = ""
  setup(executable, target_dir, filename, source_url, options, configure_make_install)

# glimpse needs a bit of manual intervention to create lib and bin directories before 'make'
def setup_glimpse_premake():
  if not os.path.exists('lib'):
    os.makedirs('lib')
  if not os.path.exists('bin'):
    os.makedirs('bin')

def setup_glimpse():
  executable = "glimpse"
  target_dir = 'glimpse'
  filename = "{t}{e}".format(t=target_dir, e='.git')
  source_url = 'https://github.com/gvelez17/{f}'.format(f=filename)
  #glimpse uses C89 syntax so do this bit of hackery to silence the errors
  options =' "CC=gcc -Wno-return-type -std=gnu89"'
  setup(executable, target_dir, filename, source_url, options, configure_make_install, setup_glimpse_premake)

def setup_swish_e():
  executable = "swish-e"
  target_dir = 'swish-e-2.4.7'
  filename = "{t}{e}".format(t=target_dir, e='.tar.gz')
  source_url = 'http://swish-e.org/distribution/{f}'.format(f=filename)
  options =''
  setup(executable, target_dir, filename, source_url, options, configure_make_install)

def setup_postgres():
  if not check_executable('psql'):
    print 'PostgreSQL not detected, installing.'
  else:
    return
  if sys.platform == 'linux2':
    command = "sudo apt-get install postgresql"
    print command
    subprocess.call(command, shell=True)
  elif sys.platform == 'darwin':
    extension = '.dmg'
    filename_bare = "postgresql-9.4.4-3-osx"
    filename = "{b}{e}".format(b=filename_bare, e=extension)
    if not os.path.exists(filename):
      url = "http://get.enterprisedb.com/postgresql/{f}".format(f=filename)
      print 'Downloading {u}'.format(u=url)
      urllib.urlretrieve(url, filename)
    mountPointRoot = '/Volumes/PostgreSQL 9.4.4-3'
    mountPoint = "{r}/{b}.app".format(r=mountPointRoot, b=filename_bare)
    try:
      os.system('hdiutil mount {f}'.format(f=filename))
      subprocess.check_call('open "{t}"'.format(t=mountPoint), shell=True)
    finally:
      os.system('hdiutil unmount "{m}"'.format(m=mountPointRoot))

def check_apache_and_restart():
  command = "sudo apachectl configtest"
  print command
  subprocess.check_call(command, shell=True)
  command = "sudo apachectl restart"
  print command
  subprocess.check_call(command, shell=True)

def setup_mod_perl():
  target_dir = 'mod_perl-2.0'
  command = "svn checkout https://svn.apache.org/repos/asf/perl/modperl/trunk/ {t}".format(t=target_dir)
  subprocess.check_call(command, shell=True)
  with cd(target_dir) as dir:
    command = "perl Makefile.PL MP_CCOPTS=-std=gnu89"
    print command
    subprocess.check_call(command, shell=True)
    command = "make"
    print command
    subprocess.check_call(command, shell=True)
    command = "sudo make install"
    print command
    check_apache_and_restart()

def get_lxr_target_dir():
  return 'lxr-2.0.3'

def update_http_conf(apache_dir, new_file):
  target = '{a}/conf-available/lxr.conf'.format(a=apache_dir)
  if os.path.exists(target):
    os.rename(target, target + '.bak')
  shutil.copyfile(new_file, target)
  check_apache_and_restart()

def setup_lxr():
  #http://sourceforge.net/projects/lxr/files/stable/lxr-2.0.3.tgz/download
  executable = None
  target_dir = get_lxr_target_dir()
  filename = "{t}{e}".format(t=target_dir, e='.tar.gz')
  source_url = 'http://downloads.sourceforge.net/project/lxr/stable/lxr-2.0.3.tgz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Flxr%2Ffiles%2Fstable%2F&ts=1443104545&use_mirror=vorboss'.format(f=filename)
  options =''
  setup(executable, target_dir, filename, source_url, options)
  command = 'sudo mv {t} /etc/{t}'.format(t=target_dir)
  print command
  subprocess.check_call(command, shell=True)

def setup_svn():
  if sys.platform == 'linux2':
    command = "sudo apt-get install svn"
    print command
    subprocess.check_call(command, shell=True)
  else:
    print "NOT IMPLEMENTED"
    sys.exit(-1)

if __name__ == '__main__':
  print __file__
  try:
    apache_dir = sys.argv[1]
    if not apache_dir.endswith('/'):
      apache_dir = apache_dir + '/'
  except:
    print "Usage: {f} <APACHE_DIR e.g. /etc/apache2 containing httpd.conf>"
    sys.exit(-1)

  print 'Setup ctags'
  setup_ctags()

  print 'Setup glimpse'
  setup_glimpse()

  print 'Setup swish-e'
  setup_swish_e()

  print 'Setup postgresql'
  setup_postgres()

  print 'Check perl'
  if not check_executable('perl'):
    sys.exit('Error: perl not found, install it')

  print 'Setup lxr'
  setup_lxr()

  print 'Setup svn'
  setup_svn()

  print 'Setup mod_perl'
  setup_mod_perl()

  print 'Run database setup script.'
  print 'Passwords required are as follows: postgres, postgres, postgres... when promted for the new password insert lxrpw'
  print 'Then the password required switches to lxrpw from the 2nd request after the mention of database'
  command = 'initdb.sh'
  print command
  subprocess.check_call(command, shell=True)

  update_http_conf(apache_dir, 'httpd.conf')

