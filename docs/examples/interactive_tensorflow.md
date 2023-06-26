First we pull a TensorFlow image

```console
srun singularity pull docker://nvcr.io/nvidia/tensorflow:23.05-tf2-py3
```

The pull address of the container can be found from the [NGC
catalog](https://catalog.ngc.nvidia.com/).

We can then do

```console
srun --gres=gpu:1 --pty singularity shell --nv tensorflow_23.05-tf2-py3.sif
```

or by reference to the docker image 'docker://nvcr.io/nvidia/tensorflow:23.05-tf2-py3'

You now have shell access

```console
Singularity>
```

You can exit the interactive session with

```console
exit
```
