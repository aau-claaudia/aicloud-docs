Some images, like the PyTorch images from NGC, come with [Anaconda](https://anaconda.org/), which is a widely used Python distribution. In this example we will build a PyTorch image and install additional Anaconda packages in the image.

First build our Singularity image from a Docker PyTorch image and install additional conda packages. The Singularity file contains:

```console
BootStrap: docker
From: nvcr.io/nvidia/pytorch:23.05-py3

%post
/opt/conda/bin/conda install -c anaconda beautifulsoup4 
```

Paste this into a file on AI Cloud you call pytorch.sif and build using:

```console
srun singularity build --fakeroot pytorch.sif Singularity
```

Again this may take some time. Notice that we pull the [PyTorch Docker image from NGC](https://ngc.nvidia.com/catalog/containers/nvidia:pytorch)

Next we can, e.g., run our container in interactive mode:

```console
srun --pty --gres=gpu:1 singularity shell --nv pytorch.sif
```

and we can then use the Anaconda Python distribution to for example run IPython

```console
$ ipython
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
Type 'copyright', 'credits' or 'license' for more information
IPython 8.9.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import torch

In [2]: import bs4
```
