*Note that this is not a recommended approach. Please read [Installing
software in
containers](../../singularity/#installing-software-in-containers) first,
and consider the approach below a last resort.*

## The Challenge

The software installed in a Singularity image must be installed via
the steps in a [Singularity definition
file](https://sylabs.io/guides/3.5/user-guide/definition_files.html)
when building the container. Once built, the image (SIF file) is
immutable, so you cannot install additional software into it at
container runtime.  
If you have downloaded a pre-defined image from for example
[NGC](https://ngc.nvidia.com/) or built an image yourself and attempt
to run some Python software inside it (for example TensorFlow or
PyTorch code), you may discover that your container is missing some
dependencies for running the software.

## The Temptation

At this point, it may be tempting to simply install the missing
packages from [PyPI](https://pypi.org/) using `pip` inside the
container in order to circumvent the hassle of rebuilding the
container image. This is also possible and may work fine at first
glance. The potential problem with this approach is that the
package(s) and associated libraries installed by pip are not installed
inside the container image itself, but instead "bleed through" to your
user directory. The files are installed in the hidden directory
'.local' in your user directory. The problems described in the
following may also apply to other directories such as '.ipython',
'.keras', '.jupyter', '.conda', '.config', etc., if present, and can
be solved in the same way. Generally, "if it ain't broken, don't fix it."

## The Headache

If at a later point you run Python software inside a different
container, Python in this container also sees the same '.local'
directory in your user directory and may use packages and libraries
from here instead of those actually installed in the container
image. This can cause incompatibilities between packages/libraries
installed in the container image and those found in
'.local'. Ultimately, this means your software fails to run.

## The Solution

The strict solution to this problem is to avoid using `pip` to install
anything when running inside a Singularity container and instead make
sure to build it properly into the container image itself. This can,
however, be inconvenient - especially if you are merely using a
pre-defined Singularity image that you downloaded from NGC.  
So, acknowledging that there are actually benefits to being able to
conveniently install things "inside" your container using `pip`, let
us see how to make it work.

When Singularity runs a container, your user directory is by default
[bind-mounted](https://sylabs.io/guides/3.5/user-guide/bind_paths_and_mounts.html)
into your container (effectively, you can also access the contents of
your user directory inside the container). We can use this bind-mount
feature of Singularity to configure additional directories to mount
into the container at specified paths. This allows us to create a
separate '.local' directory for each container image we are using, so
they do not interfere with each other.

As an example, I have the following two versions of NGC's TensorFlow
image in my user directory:

- tensorflow_20.03-tf2-py3.sif
- tensorflow_20.12-tf2-py3.sif

I want to be able to use `pip` inside containers from each of these
images without them interfering with each other. I first create two
new directories to act as the separate '.local' directories inside my
containers:

```console
cd ~
mkdir .local-tf20.03
mkdir .local-tf20.12
```

Now, when I run a container from the 'tensorflow_20.03-tf2-py3.sif'
image, I use the `-B` parameter to specify where to mount this
container's directory inside the container:

```console
srun --pty singularity shell --nv -B .local-tf20.03:$HOME/.local tensorflow_20.03-tf2-py3.sif
```

This way, inside the container you will be able to access the
directory as '~/.local', but files stored in it will really reside in
'~/.local-tf20.03'. Similary, I run a container from the
'tensorflow_20.12-tf2-py3.sif' image using this command:

```console
srun --pty singularity shell --nv -B .local-tf20.12:$HOME/.local tensorflow_20.12-tf2-py3.sif
```

The directory will still appear as '~/.local' inside the container,
but this container will really store changes in
'~/.local-tf20.12'. You can of course do this for as many different
container images and associated directories as you like. Just remember
to give the directories different names.

Note that if '.local' already exists in your user directory and you do
not wish to delete it, *this is still safe to do*. The original
contents of your '.local' will simply be hidden while the container is
running and will again be available unchanged when the container stops
running. *You can safely leave the original '.local' directory where
it is when using the above solution.*
