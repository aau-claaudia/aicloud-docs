This page provides additional instructions and advice on using
Singularity containers in AI Cloud. We will keep adding more material,
so it is a good idea to check in here from time to time for helpful
information.  
You are welcome to suggest topics you would like to know more about by
creating an issue:
[here](https://github.com/aau-claaudia/aicloud-docs/issues).

## Installing software in containers

The Singularity container images ('.sif' files) you get by downloading
a pre-defined container from for example NGC with `singularity pull`
(see also [Introduction](../introduction/#obtaining-containers)) are
read-only. This means you cannot install additional software in them
directly. There are several different ways you can go about it instead
to be able to install additional software into your containers:

1. Create a writable sandbox container image
2. Build a new container image file with Cotainr
3. Build a new container image file from a definition file
4. Install Python packages with `pip` or `conda` outside the container

### Create a writable sandbox container image

First create a so-called sandbox container:
```console
srun singularity build --sandbox [sandbox-dir-name] [container image]
```
where you replace `[sandbox-dir-name]` with a name you decide for the
directory that holds your sandbox container, and replace `[container
image]` with the name of a container image you already have in AI Cloud
(e.g. "pytorch_23.04-py3.sif") or the URI of a container to download
(e.g. "docker://nvcr.io/nvidia/pytorch:23.04-py3").

???+ example
    
	```console
	srun singularity build --sandbox pytorch-23.04 docker://nvcr.io/nvidia/pytorch:23.04-py3
    ```
	
Then when you wish to install additional software in the container, open a shell in the container:

???+ example
    
	```console
	srun singularity shell --writable --fakeroot pytorch-23.04
    ```

While inside the container, install additional packages using for
example the `apt` package manager:
```console
Singularity> apt install [package name]
```
or `pip` (for Python):
```console
Singularity> pip install [package name]
```

When not installing software in the container you can run applications
in it as usual, without the ability to write to the container. See
commands in the
[Introduction](../introduction/#running-applications-in-containers).

### Build a new container image file with Cotainr

[Cotainr]("https://cotainr.readthedocs.io/en/stable/index.html") is a tool developed by [DeiC]("https://www.deic.dk/en/om-deic") to ease building of Singularity containers.
It can be used to build custom containers with additional software installable by Conda and Pip. This means it is primarily for adding Python packages to a container. 
It works from a base container image that you specify and then build additional Anaconda and pip packages which you supply as a conda environment specification.
We plan on installing this tool system-wide on AI Cloud in the near future.
Until then you can download the software to your own user directory, and launch it by specifying the path to the executable.

We begin by downloading the latest release from the [Cotainr repository]("https://github.com/DeiC-HPC/cotainr/releases"). In the example below we are downloading the latest version as of late 2023. Be sure to check for newer versions at the aforementioned repository. Look for the zip archive "Assets" section, and copy the link.

```console
wget https://github.com/DeiC-HPC/cotainr/archive/refs/tags/2023.11.0.zip
```

You should now have a zip archive, which you can unzip with:
```
unzip 2023.11.0.zip
```

After this has been done, you should have a directory called `cotainr-2023.11.0`. We should now be able to launch Cotainr and access its commands from within this directory. In a generalised manner the command structure is:
```console
srun [path/to/cotainr] build [name of output file] --base-image=[base image] --conda-env=[name of environment]
```
As always we use `srun` to ask Slurm to delegate the subsequent command to a compute node. 
We then need to specify the path to `cotainr/bin/cotainr` and call `build`. Then choose a name for your container and replace `[name of output file]` with this newly chosen name. We recommend appending the conventional suffix `.sif` to this name.
After that you will need to specify a `[base image]`, which can be an existing container in your directory or one from a remote source. Finally use the parameter `--conda-env` to specify which Conda environment file you want to use. If you have an existing Conda environment somewhere, you can export this environment `conda env export > my_environemt.yml`.

???+ example
    ```console
    srun ~/cotainr/bin/cotainr build amber.sif --base-image=docker://ubuntu:22.04 --conda-env=amber.yml
    ```

Also don't forget to check out the [offical Cotainr documentation]("https://cotainr.readthedocs.io/en/stable/index.html") for more information.

### Build a new container image file from a definition file

You can also build containers from scratch or from an existing base
image directly with Singularity. This is a somewhat more difficult
approach than the above Cotainr tool, because it requires you to write
the Singularity definition file yourself. The build process can be
lengthy (see also [work-arounds](#work-arounds) below on how to
improve build speed) and so, it can take a long time with
trial-and-error to get the definition right and produce a working
container. Please see the [Singularity
documentation](https://docs.sylabs.io/guides/3.8/user-guide/build_a_container.html#building-containers-from-singularityce-definition-files)
for details on how to build containers from definition files.

### Install Python packages with `pip` or `conda` outside the container

This is not recommended, as the method is a bit "brittle". It is easy
to set it up wrong and end up in a situation where versions of
packages installed for different container images get mixed up and
cause problems. Consider this a last resort: [Please see this
guide](../examples/pip_in_containers).

## Work-arounds for slow and memory-consuming container builds {#work-arounds}

The two work-arounds below demonstrate how to build Singularity
container images:

1. without excessive memory requirements, and
2. finishing builds faster.

These to work-arounds can be combined into one by using both the
temporary directory in "/tmp" and the local cache directory in "/raid"
and specifying both the `SINGULARITY_TMPDIR` and the
`SINGULARITY_CACHEDIR` environment variables shown in the following
instructions.

### Building container images without excessive memory requirements {#work-around-mem}

Building some Singularity containers in AI Cloud may require an
unreasonably large amount of memory to succeed, such as:

???+ example
    
	**Not the right way to do it:**
	```console
	srun singularity pull docker://nvcr.io/nvidia/tensorflow:23.03-tf1-py3
	```

If you simply run this command as-is, you are likely to experience an
out-of-memory error during build of the container image. A crude
work-around for this issue is to simply allocate more memory to your
job using the `--mem` option for `srun` (it could easily require
40-50GB). This may cause your job to have to wait for a long time
before it can start. There is, however, a better way to run
Singularity to avoid the unreasonable memory requirement. Please
follow these steps to use the "/tmp" partition of a compute node
during build of your container:

1. Start an interactive job for building your container:  
   `srun --pty bash -l`  
   (You may add the `--nodelist` parameter to request a particular
   compute node as usual with `srun`.)
2. Create a temporary directory for yourself to use during build of
   your container image:  
   ``mkdir /tmp/`whoami` ``  
   *Take note of the back-tick characters in the above command; this
   is just to create a directory called "/tmp/username" if your
   username is "username". You can call it something else instead, but
   it is important to create it under "/tmp".*
3. Run Singularity to build your container image, using your new
   directory in "/tmp" for temporary data storage:  
   ``SINGULARITY_TMPDIR=/tmp/`whoami` singularity pull docker://nvcr.io/nvidia/tensorflow:23.03-tf1-py3``  
   *The SINGULARITY_TMPDIR variable should be set to whatever you
   named your temporary directory in step 2.*
4. After Singularity has finished building, delete your temporary
   directory:  
   ``rm -r /tmp/`whoami` ``
5. Exit your interactive job:  
   ``exit``

### Building container images faster {#work-around-slow}

When building Singularity container images, you may experience very
slow performance. This is due to the fact that when writing files to
your user directory, you write to a network file system which is
known to be slow in some situations. This can cause container image
builds to take hours to complete.

In order to make this build process much faster, there is a
work-around you can use to build your containers. In order to do this,
you must use one of the compute nodes that have local storage; please
see [this overview](introduction.md#overview) - look for the "Disk"
column in the table.

Please follow these steps to use the local storage of a compute node
during build of your container:

1. Start an interactive job for building your container:  
   `srun --pty --nodelist nv-ai-01 bash -l`  
   *It is important to use the `--nodelist` parameter to request a
   compute node with local storage.*
2. Create a cache directory for yourself to use during build of
   your container image:  
   ```console
   mkdir /raid/`whoami`
   cd /raid/`whoami`
   ```  
   *Take note of the back-tick characters in the above command; this
   is just to create a directory called "/raid/username" if your
   username is "username". You can call it something else instead, but
   it is important to create it under "/raid".*
3. Run Singularity to build your container image, using your new
   directory in "/raid" for cache data storage:  
   ``SINGULARITY_CACHEDIR=/raid/`whoami` singularity pull docker://nvcr.io/nvidia/tensorflow:23.03-tf1-py3``  
   *The SINGULARITY_CACHEDIR variable should be set to whatever you
   named your cache directory in step 2.*  
5. Exit your interactive job:  
   ``exit``

You have now built your container image in the directory
"/raid/username" on a specific compute node, so you can only access it
on that compute node. You can choose to keep using it on that specific
compute node by making sure to use the `--nodelist` parameter with the
same compute node for subsequent jobs using this container image and
accessing it from your "/raid/username" directory. You can also copy
the image from there to your user directory in order to access it from
all compute nodes. Again, this copy operation may be slow due to slow
access to your user directory.  
*Please remember to delete any files you have in "/raid" on the
specific compute nodes involved when you no longer need them.*
