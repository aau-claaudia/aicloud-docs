# Installing Anaconda

We will install a version of Anaconda by downloading a specific version of Anaconda, install and add the binaries to the PATH:

```bash
anacondaType=Anaconda3-2021.11-Linux-x86_64.sh
wget -q https://repo.anaconda.com/archive/$anacondaType
chmod +x $anacondaType

./$anacondaType -b -p
sudo rm -f $anacondaType

export PATH="$HOME/anaconda3/bin:$PATH"

conda init bash
```

If you like to access a jupyter notebook on the machine, you need to

1. Add port 8888 as custom rule to a Security Group, [see this guide](../../openstack_guides/Access_to_instance.md#custom-rule)
2. Start the service

```bash
jupyter notebook --ip 0.0.0.0

```
The latter argument is to allow for access from other than the host itself. Point your browser to e.g. 10.92.0.55:8888 and login using the token shown in the output when starting the jupyter notebook.
