## PyTorch and Anaconda

Some images, like the PyTorch images from NGC, come with [Anaconda](https://anaconda.org/), which is a widely used Python distribution. In this example we will build a PyTorch image and install additional Anaconda packages in the image.

First build our Singularity image from a Docker PyTorch image and install additional conda packages. The Singularity file is

```console
BootStrap: docker
From: nvcr.io/nvidia/pytorch:21.12-py3

%post
/opt/conda/bin/conda install -c anaconda beautifulsoup4 
```

Go into the folder 'docs_aicloud/aicloud_slurm/pytorch_anaconda_example' and build using

```console
srun singularity build --fakeroot pytorch.sif Singularity
```

Again this may take some time. Notice that we pull the [PyTorch Docker image from NGC](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch)

Next we can, e.g., run our container in interactive mode

```console
srun --pty --gres=gpu:1 singularity shell --nv pytorch.sif
```

and we can then use the Anaconda Python distribution to for example run IPython

```console
$ ipython
Python 3.6.9 |Anaconda, Inc.| (default, Jul 30 2019, 19:07:31) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.12.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import torch

In [2]: import bs4
```
