First we pull a TensorFlow image

```console
srun singularity pull docker://nvcr.io/nvidia/tensorflow:21.12-tf2-py3
```

The pull address of the container can be found from the [NGC catalog](https://ngc.nvidia.com/catalog/containers?orderBy=modifiedDESC&pageNumber=1&query=&quickFilter=containers&filters=).

We can then do

```console
srun --gres=gpu:1 --pty singularity shell --nv tensorflow_21.12-tf2-py3.sif
```

or by reference to the docker image 'docker://nvcr.io/nvidia/tensorflow:21.12-tf2-py3'

You now have shell access

```console
Singularity>
```

You can exit the interactive session with

```console
exit
```
