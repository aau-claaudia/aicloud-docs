# SSH for Windows using putty 
If you're using an older version of Windows, you might not have access to the OpenSSH client. Instead, people often use the tool [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). 


## Convert key
With the native OpenSSH client you can use this private key(pem-file) directly. For Putty you have to convert your key first, by completing the following steps:




* Start PuTTYgen (e.g., from the Start menu, click All Programs > PuTTY > PuTTYgen).
* Click Load

![Alt Description](../img/openstack/puttykeygenerator.png?raw=true "Title")

* Browse to the location of the private key file that you want to convert (e.g., MyPersonalKey.pem).

Note: By default, PuTTYgen displays only files with extension .ppk; you'll need to change that to display files of all types in order to see your .pem key file. The private key file must end with a newline character or PuTTYgen cannot load it correctly.

![Alt Description](../img/openstack/puttysavekey.png?raw=true "Title")

* Select your .pem key file and click Open.
* If everything went well PuTTYgen displays the following message:

![Alt Description](../img/openstack/puttygennotice.png?raw=true "Title")

* When you click OK, PuTTYgen displays a dialog box with information about the key you loaded, such as the public key and the fingerprint.
* Optional: Enter and confirm a key passphrase (If you use a passphrase you will have to enter this passphrase whenever you authenticate with your key.)
* Click Save private key to save the key in PuTTY's format.

![Alt Description](../img/openstack/puttykeygeneratorwindow.png?raw=true "Title")

* Save your yourPersonalKey.ppk file somewhere secure.



# SSH to instance

First, we need to convert yourPersonalKey.pem to the format used with Putty before we can use PuTTY. The steps are:


1. Open PuTTY. 
2. Go in the tree on the left to Connection > SSH > Auth
3. Click on the ‘Browse...’ button under Private key file for authentication:

![Alt Description](../img/openstack/putty_key_auth.png?raw=true "Title")



4. Select the PPK-file (your private key) you just saved.
5. Go in the tree on the left to ‘Session’
6. Enter in the ‘Host Name (or IP address)’ field the username and floating IP address of the instance:
![Alt Description](../img/openstack/putty_ubuntu.png?raw=true "Title")
7. Optional: Enter a name for the session in the ‘Saved Sessions’ field and click save. This saves all the settings, including the private key for this session.
8. Click Open to connect to the instance.
9. When you connect for the first time you’ll be asked if you trust this computer. Normally you can click Yes

![Alt Description](../img/openstack/putty_first.png?raw=true "Title")


10.If you’re connecting to an instance with a floating IP that you used before you’ll get this warning message. If that’s the case, it’s safe to click Yes as well.

![Alt Description](../img/openstack/putty_reuse.png?raw=true "Title")


11. If everything works alright you’re now logged in.


These steps forms a framework for other tools as well. If you like e.g. [FileZilla](https://filezilla-project.org/), locate how to use/add the pemision file "yourPersonalKey.pem", and connect with the SSH protocol.

# X11 forwaring
If you want to see GUIs using X11 forwarding, you can follow the guider [here](https://superuser.com/questions/119792/how-to-use-x11-forwarding-with-putty)
