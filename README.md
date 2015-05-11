# win_java
---

The win_java state module allows management and configuration of java installed on a computer running the Windows operating system. This module uses powershell commands, so the version of windows being used must be able to run powershell commands.

A simple example that sets the JAVA_HOME environment variable based on the registry keys set during java installation:

```
set_java_home:
	win_java.java_home:
		- set_to_current_version: True
```
	
### win_java.set_java_home
---

This state will allow you to set the JAVA_HOME environment variable. The state name will set java home, unless the ```set_to_current_version``` argument is set to true.

example of specifying java home:

```
'c:\path\to\java\home':
	win_java.set_java_home
```

Alternately, if you want to set JAVA_HOME based on registry keys set during java installation, you can set ```set_to_current_version``` to true

example:

```
set_java_home:
	win_java.java_home:
		- set_to_current_version: True
```

### win_java.ca_install
---

This state will install a certificate into a java keystore using java's keytool. You need a certificate file and either need to specify the base java installation directory where java was installed (aka java home) or have set the JAVA_HOME environment variable.

Example certificate installation:

```
certificate_alias:
	win_java.ca_install:
		- certificate: c:\\path\\to\\my\\java\\cert.crt
		- java_home: 'C:\\path\\to\\java\\home'
		- keystore: 'c:\\path\\to\\java\\home\\lib\\security\\cacerts'
		- storepass: supersecret

```

* ``` name ```

	The alias for the certificate
	
	
* ``` certificate ```
	
	The certificate file to load into the java keystore. Specify a full path, like ```C:\path\to\my\java\cert.crt```
	
	
* ``` java_home ```

	The java installation base directory. should contain a bin and a libs directory. If this is not specified, this defaults to the JAVA_HOME environment variable.

* ``` keystore ```

	The java keystore where you wish to place the certificate. Specify a full path, like ```c:\path\to\keystore```. If this is not specified, it will default to ``` java_home + 'libs\security\cacerts'``` where the java_home above is the base path and libs\security\cacerts is the relative path from that point.

* ``` storepass ```
	
	The java keystore password to install a new certificate. The default is 'changeit', so if you do not specify a password, it will default to this.

#### NOTES
---

This has been tested on Windows 8.1 and Windows Server 2012
