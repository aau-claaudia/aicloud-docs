# AI Cloud structure

The [AI Cloud](#ai-cloud-new) is a cluster consisting of a number of
nodes (servers).

You are always welcome to [contact the CLAAUDIA
team](https://www.claaudia.aau.dk/support-advisory/) for guidance on
how to best use the described platforms.

## AI Cloud

The AI Cloud is the second generation of CLAAUDIA's AI Cloud service which has
gradually been put into service since 2021.  
The AI Cloud consists of a front-end node (ai-fe02.srv.aau.dk) and a number of compute
nodes. The AI Cloud is a heterogeneous platform with several different
types of hardware available in the compute nodes.

The front-end node is used for logging into the platform, accessing
your files, and starting jobs on the compute nodes. The front-end node
is a relatively small server which is *not* meant for performing heavy
computations; only light-weight operations such as transferring files
to and from AI Cloud and defining and launching job scripts.

The details of defining and running jobs are described in the
[introduction](introduction.md).

## AI Cloud pilot platform

The AI Cloud pilot platform was the first generation of the AI Cloud
and was in service 2019-2022. This platform was available through the
front-end node ai-pilot.srv.aau.dk (also known as
nv-ai-fe01.srv.aau.dk), but *no longer exists*.  
If you had data in the AI Cloud pilot platform, this is still
available through the current front-end node instead.

## Operating system, file storage, and application framework

The AI Cloud is based on [Ubuntu
Linux](https://en.wikipedia.org/wiki/Ubuntu) as its operating
system. In practice, working in the AI Cloud primarily takes place via
a [command-line
interface](https://en.wikipedia.org/wiki/Command-line_interface).

Two major building blocks are essential to working with the AI Cloud:
a resource management / queuing system called Slurm and a container
system called Singularity/Apptainer.

???+ info

    The container system formerly known as Singularity [has changed name
    to
    Apptainer](http://apptainer.org/news/community-announcement-20211130). So
    far, the AI Cloud and AI Cloud pilot platform are still using a
    version by the name Singularity. It is likely that this will change
    to Apptainer in the future. So far, we refer to the product as
    Singularity/Apptainer or simply Singularity in the documentation. If
    or when we eventully switch to a version by the Apptainer name, the
    documentation will be updated accordingly.

### Slurm

Slurm is a queueing system that manages resource sharing in the AI
Cloud. Slurm makes sure that all users get a fair share of the
resources and get served in turn. Computational work in the AI Cloud
can *only* be carried out through Slurm. This means you can only run
your jobs on the compute nodes by submitting them to the Slurm
queueing system. It is also through Slurm that you request the amount
of ressources your job requires, such as amount of RAM, number of CPUs
(logical CPUs with hyperthreading = 2 &times; physical CPUs = 2
&times; cores), number of GPUs etc.  
See how to get started with Slurm in the
[introduction](introduction.md).

### Singularity/Apptainer

Singularity is a container framework which serves to provide you with
the necessary software environment to run your computational
workloads. Different researchers may have widely different software
stacks or perhaps versions of the same software stack that you need
for your work. In order to provide maximum flexibility to you as users
and to minimise potential compatibility problems between different
software installed on the compute nodes, each user's software
environment(s) is defined and provisioned as Singularity
containers. You can both download pre-defined container images or
configure or modify them yourself according to your needs.  
See details on container images from NGC in the
[introduction](introduction.md).

### File storage

Files in "user directories" and "project directories" are stored on a central network file system, and  accessible to all nodes. When you launch a job, access to the network file system is carried over to the compute node. This means that there is no need to synchronise files between nodes. When you store or edit a file in your user directory on the front-end node, the compute nodes can see the same file and its contents.

#### Storage quota expansions
When users log in to AI Cloud for the first time, a user directory is created for them. These directories are allocated 1 TB of storage by default. This should be plenty for most users, but should you need additional space, it is possible to apply for storage quota expansions for a limited time using our [Storage quota expansions form](https://forms.office.com/e/AjT0GccAPb).

!!! info

    When you log in to the platform, you can see your storage usage of the user directory at the very top line:    
    ```
    Current quota usage: 181GiB / 1.0TiB
    Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-169-generic x86_64)
    
     * Documentation:  https://help.ubuntu.com
     * Management:     https://landscape.canonical.com
     * Support:        https://ubuntu.com/pro
    
      System information as of Fri Mar 15 11:09:21 CET 2024
    ```

#### Group project directories

For projects where users need to collaborate and share files with other users, it is possible to create a group folder inside the directory `home/project`. Please consult the page [Group Project](https://aicloud-docs.claaudia.aau.dk/examples/group_projects/) to learn more about how to use this directory.
