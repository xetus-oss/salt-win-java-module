from __future__ import print_function
import sys

def current_version_java_home():
  '''
  Automagically finds the java home directory for the currently installed and 
  used version of the java jre.
  '''
  jre_current_version = __salt__['reg.read_value'](
    'HKEY_LOCAL_MACHINE',
    'SOFTWARE\JavaSoft\Java Runtime Environment',
    'CurrentVersion')['vdata']

  return __salt__['reg.read_value'](
    'HKEY_LOCAL_MACHINE',
    ('SOFTWARE\\JavaSoft\\Java Runtime Environment\\' + jre_current_version),
    'JavaHome')['vdata']