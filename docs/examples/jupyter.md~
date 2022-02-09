## TensorFlow and Jupyter notebook using TensorFlow container

*This section needs an update*

We have provided a script for this. You can do the following and type in a password

```console
$ /user/share/scripts/jupyter.sh
Using tensorflow.sif
srun: job 45060 queued and waiting for resources
srun: job 45060 has been allocated resources
slurmstepd: task_p_pre_launch: Using sched_affinity for tasks
Enter password: 
Verify password: 
[NotebookPasswordApp] Wrote hashed password to /user/its.aau.dk/tlj/.jupyter/jupyter_notebook_config.json
LIST
Point your browser to http://nv-ai-01.srv.aau.dk:8888
Press any key to close your jupyter server
```

The first time, this will download a new TensorFlow image. Then follow the guide printed in your terminal window on how to open the Jupyter notebook in a browser and type in your password. You have to be on the AAU network (on campus or VPN). Try e.g. new->Python 3 and execute the following cell.

```console
!nvidia-smi
```

or

```console
from tensorflow.python.client import device_lib
device_lib.list_local_devices()
```

You should see you have one V100 GPU available. You can close again by pressing any key in the terminal, or cancel the slurm allocation.
