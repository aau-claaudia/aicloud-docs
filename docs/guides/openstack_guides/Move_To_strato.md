![Alt Description](../img/logo.png?raw=true "Title")

# Move data to strato-new
This guide is for you, if you have been a user on the "old" strato compute cloud pilot and want to move to the new strato, but have some data that should be moved as well.

If you have data, that you can't easily recreate you can move your date with [SCP](https://www.howtogeek.com/66776/how-to-remotely-copy-files-over-ssh-without-entering-your-password/), [SFTP](https://linuxconfig.org/how-to-setup-sftp-server-on-ubuntu-18-04-bionic-beaver-with-vsftpd), [Rsync](https://www.digitalocean.com/community/tutorials/how-to-copy-files-with-rsync-over-ssh) etc. to your new instance on strato.

In the following we will always execute the command from the new instance on strato-new. To that we first need to copy the old private key to the new instance. This can be done with e.g. SCP

## Copy key with SCP
First we will copy the private key to the new instance. This can be done with e.g. SCP

```
scp -i <private_key_new_strato> <private_key_old_strato> ubuntu@<To_Address>:<to_folder>
```

Example:
```
scp -i keynew.pem keyold.pem ubuntu@10.92.0.87:/home/ubuntu
```

You can then SSH (with keynew.pem) to your new instance and start copying.

## Copy data with SCP

You can then copy with SCP. An example could by
```
scp -i <private_key_old_strato> ubuntu@<from_address>:<from_folder> <to_folder>
```

Example:
```
scp -i keyold.pem ubuntu@130.226.98.198:/home/ubuntu/data/data1.csv .
```

or recursively
```
scp -i keyold.pem -r ubuntu@130.226.98.198:/home/ubuntu/data/ .
```

### Copy data with Rsync

For larger amounts of data we recommend rsync, since if something goes wrong in the process, we can start the sync process again.

The command is something like the following for recursively transfer
```
rsync -Pavr -e "ssh -i <private_key_old>" ubuntu@<from_address>:<from_folder_path> <to_folder>

```

Example:

```
rsync -Pavr -e "ssh -i stratocommon.pem" ubuntu@130.226.98.119:/home/ubuntu/data /home/ubuntu/data
```

