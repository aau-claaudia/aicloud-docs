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

For now we explain the methods 1. and 4. above here. Guidance on
methods 2. and 3. is coming...

### Create a writable sandbox container image

First create a so-called sandbox container:
```console
srun singularity build --sandbox [sandbox-dir-name] [container image]
```
where you replace `[sandbox-dir-name]` by a name you decide for the
directory that holds your sandbox container, and replace `[container
image]` by the name of a container image you already have in AI Cloud
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

### Install Python packages with `pip` or `conda` outside the container

This is not recommended, as the method is a bit "brittle". It is easy
to set it up wrong and end up in a situation where versions of
packages installed for different container images get mixed up and
cause problems. Consider this a last resort: [Please see this
guide](../examples/pip_in_containers).

## Work-arounds for slow and memory-consuming container builds

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
   `srun --pty --nodelist nv-ai-01.srv.aau.dk bash -l`  
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
