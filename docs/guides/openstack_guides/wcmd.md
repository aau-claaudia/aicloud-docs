# SSH using Windows command

If you're using a more recent version of Windows, you might have access to an OpenSSH client. 

# SSH to instance

1. You need to get the key as described in the [quick start guide](../quick-start.md) and save it as "yourPersonalKey.pem"
2. Use Explorer and locate the directory of "yourPersonalKey.pem"
3. Right click "yourPersonalKey.pem" and select Properties->Security->Edit and remove all users that are not you, SYSTEM or Administrator.
4. Open Windows Command Prompt (CMD) and type
```bash
ssh ubuntu@<your floating IP> -i <yourPersonalKey.pem>
```
e.g.
```bash
ssh ubuntu@130.226.98.166 -i yourPersonalKey.pem
```
if you are located in the same directory as yourPersonalKey.pem file.
