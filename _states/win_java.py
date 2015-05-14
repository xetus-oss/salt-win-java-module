'''
Windows Java
============

The win_java state handles some useful java configuration items past just
JRE or JDE installation.
'''

from __future__ import print_function
import sys

def java_home(name, set_to_current_version=False):
  '''
  Sets the JAVA_HOME environment variable on a windows system that has
  powershell.

  The state's ``name`` will determine what the new java home should be unless
  ``set_to_current_version`` is set to True.

  ``set_to_current_version`` will disregard the ``name`` of the state and 
  automagically set JAVA_HOME from registry keys that were set when the version 
  of java was installed.

  .. note::

    The JAVA_HOME environment variable should be set to the java directory 
    containing the bin and libs folders.

  .. code-block:: yaml

    "c:\\some\\version\\of\\java":
      win_java.java_home

  or, alternately, if you wish to take advantage of the state automagically 
  setting the JAVA_HOME environment variable for you

  .. code-block:: yaml

    set_me_some_java_home:
      win_java.java_home:
        - set_to_current_version: True

  '''
  if set_to_current_version:
    java_home = __salt__['home_helper.current_version_java_home']()
  else:
    java_home = name

  old = __salt__['cmd.run'](
    '[Environment]::GetEnvironmentVariable("JAVA_HOME","Machine")', 
    shell="powershell")

  if java_home != old:
    cmdResult = __salt__['cmd.script'](
      'salt://win-java-home/powershell/set_java_home.ps1', 
      args=(' "' + java_home + '"'), shell='powershell')

    if cmdResult:
      return {'name': name, 
              'changes': {'old': old, 'new': java_home}, 
              'result': True, 
              'comment': ('JAVA_HOME was set to ' + java_home)}
    else:
      return {'name': name, 
              'result': False, 
              'comment': ('attempted to set JAVA_HOME to ' + java_home + 
                ' but something went wrong...'), 
              'changes':{}}
  else:
    return {'name': name, 
            'result': True, 
            'comment': 'JAVA_HOME was already set to ' + java_home, 
            'changes':{}}

def ca_install(name, 
               java_home=None, 
               keystore=None, 
               storepass="changeit",
               certificate=None):
  '''
  Installs a certificate into a java keystore using java's keytool.

  name
    The alias to use to name the certificate installed into the java keystore

  java_home
    The base java installation directory, should contain a bin folder and a lib
    folder. This is optional, if it isn't passed, it will read the JAVA_HOME
    environment variable and use that

  keystore
    The keystore for which to install the certificate. This defaults to 
    lib\\security\\cacerts from the java_home directory passed (or the 
    JAVA_HOME environment variable if no java_home was passed)

  storepass
    The keystore password for listing or installing a certificate. Defaults to
    'changeit', which is the default java keystore password

  certificate
    The certificate to install into the java keystore

  This will verify that a certificate with the alias supplied does not already
  exist. If a certificate with the same alias as the one trying to be installed
  does exist, this state will report no changes.

  .. note::

    If a certificate with the same alias exists in the java keystore but it is
    actually a different certificate, this state will report no changes and
    complete successfully, EVEN THOUGH THE CERTIFICATES ARE NOT THE SAME!

  .. code-block:: yaml

    my_cert:
      win_java.ca_install:
        - java_home: C:\\path\\to\\java\\home
        - keystore: C:\\path\\to\\java\\home\\and\\to\\keystore
        - storepass: super_secret
        - certificate: C:\\path\\to\\my\\certificate.crt

  '''
  if java_home is None:
    java_home = __salt__['cmd.run'](
      '[Environment]::GetEnvironmentVariable("JAVA_HOME","Machine")',
      shell='powershell')

  if keystore is None:
    keystore = java_home + '\\lib\\security\\cacerts'

  verifyResult = __salt__['cmd.retcode'](
    '&"' + java_home + '\\bin\\keytool.exe"' +
    ' -alias ' + name + 
    ' -keystore "' + keystore + '"' +
    ' -storepass ' + storepass + 
    ' -list' +
    ' -noprompt', shell='powershell')

  if verifyResult != 0:
    storeResult = __salt__['cmd.retcode'](
      '&"' + java_home + '\\bin\\keytool.exe"' +
      ' -alias ' + name +
      ' -file "' + certificate + '"' +
      ' -keystore "' + keystore + '"' +
      ' -storepass ' + storepass +
      ' -import' +
      ' -trustcacerts' +
      ' -noprompt', shell="powershell")

    if storeResult == 0:
      return {'name': name, 
              'result': True, 
              'changes': {'old':'', 'new':'added ' + name + ' to java certs'},
              'comment': 'added ' + name + ' to java certs'}
    else:
      return {'name': name,
              'result': False,
              'changes': {},
              'comment': 'Encountered a problem importing ' + name + ' cert...'}

  return {'name': name,
          'result': True,
          'changes': {},
          'comment': 'The ' + name + ' certificate was already installed'}