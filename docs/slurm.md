This section describes details of how to use the resource manager /
queue system Slurm. We recommend reading [Overview](overview.md) first
and then [Introduction](introduction.md) before delving into the
details.

- [Official documentation for Slurm](https://slurm.schedmd.com/) - AI
  Cloud is currently using version
  [21.08.8-2](https://slurm.schedmd.com/archive/slurm-21.08.8-2/).
- [Interactive tutorial for Slurm](http://slurmlearning.deic.dk/) -
  this is a tutorial made by [DeiC](https://www.deic.dk/) to help
  introduce HPC users to Slurm. *Please note that this tutorial
  environment is not identical to our AI Cloud, but it enables you to
  familiarise yourself with Slurm in a safe environment where you
  cannot accicentally break anything for anyone else.*

## Bits and pieces in the queue system

The Slurm queue system is built around some concepts which
are important to know in order to understand the system and how to use
it:

Node
: We often refer to these as compute nodes in this documentations,
  because this is where the computational jobs take place.  
  The nodes are the individual servers in the platform; see
  [Overview](overview.md) for illustration and the [table in
  Introduction](introduction.md#overview) for details.
  
Partition
: You can think of partitions as different queues for the compute
  nodes. There are several partitions in the AI Cloud and the same
  nodes can be present in more than one partition.  
  For any one node, the different partitions it is present in can for
  example give access to the node under different conditions. The AI
  Cloud currently has the partitions: batch and prioritized. A few
  additional partitions are only visible to specific users of these
  (create, aicentre1, aicentre2).  
  See more details about partitions in a later section.

<!-- QoS should be added if we start using them in the new AI Cloud -->

Resources
: Slurm manages access to resources in the nodes. The important
  resources to know about in AI Cloud are CPUs, memory, and GPUs. Each
  job you submit will require certain resources. These are either
  implied by default values or explicitly requested by you when
  submitting a job.  
  *A job can only start when Slurm can find enough of the required
  resources available on one or more nodes. If resources are not
  currently available, your jobs wait in queue until other jobs have
  completed and relinquished the resources.*

Time limit
: Partitions may impose time limits. This is the longest time your job
  can run in the specific partition. If your job has not ended by this
  time limit, it will be automatically cancelled.  
  See recommendations for working within time limits in a later
  section.

## Checking the current state of the queue system

It is often desirable to be able to see what is going on in the queue
system, for example to get an idea if there are many other jobs in
queue when you wish to run a job.

### Checking the overall state of the platform

Use the command `sinfo` to see the state of the nodes in the AI
Cloud. Run `sinfo --help` or `man sinfo` in AI Cloud for detailed
documentation of the command.

???+ example

        sinfo
         
        PARTITION   AVAIL  TIMELIMIT  NODES  STATE NODELIST
        batch*         up   12:00:00      1    mix nv-ai-04.srv.aau.dk
        batch*         up   12:00:00      8   idle a256-t4-01.srv.aau.dk,a256-t4-02.srv.aau.dk, ...
        prioritized    up 1-00:00:00      8   idle a256-t4-01.srv.aau.dk,a256-t4-02.srv.aau.dk, ...

    The `sinfo` command shows basic information about partitions in the
    queue system and what the states of nodes in these partitions are.
	
	PARTITION shows which partition a line in the table	relates to.
	Multiple lines can show the same partition, because different nodes
	within a partition may be in different states.
	
	AVAIL shows the availability of the *partition* where "up" is
	normal, working state where you can submit jobs to it.
	
	TIMELIMIT shows the time limit imposed by each partition.
	
	NODES shows how many nodes are in the shown state in the specific
	partition.
	
	STATE shows which state the listed nodes are in: "mix" means that
	the nodes are partially full - some jobs are running on them and
	they still have available resources; "idle" means that they are
	completely vacant and have all resources available; "allocated"
	means that they are completely occupied. Many other states are
	possible, most of which mean that something is wrong.

### Checking details of the nodes

Use the command `scontrol show node` or `scontrol show node [node
name]` to show details about all nodes or a specific node,
respectively.  Run `scontrol --help` or `man scontrol` in AI Cloud for
detailed documentation of the command.

???+ example

        scontrol show node a256-t4-01.srv.aau.dk
		
        NodeName=a256-t4-01.srv.aau.dk Arch=x86_64 CoresPerSocket=16 
           CPUAlloc=0 CPUTot=64 CPULoad=0.00
           AvailableFeatures=(null)
           ActiveFeatures=(null)
           Gres=gpu:6
           NodeAddr=a256-t4-01.srv.aau.dk NodeHostName=a256-t4-01.srv.aau.dk Version=21.08.8-2
           OS=Linux 5.4.0-124-generic #140-Ubuntu SMP Thu Aug 4 02:23:37 UTC 2022 
           RealMemory=244598 AllocMem=0 FreeMem=252833 Sockets=2 Boards=1
           State=IDLE ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
           Partitions=batch,prioritized 
           BootTime=2022-08-15T14:32:38 SlurmdStartTime=2022-08-17T13:36:22
           LastBusyTime=2022-08-30T10:04:46
           CfgTRES=cpu=64,mem=244598M,billing=64,gres/gpu=6
           AllocTRES=
           CapWatts=n/a
           CurrentWatts=0 AveWatts=0
           ExtSensorsJoules=n/s ExtSensorsWatts=0 ExtSensorsTemp=n/s

### Nodesummary

The two commands `sinfo` and `scontrol show node` provide information
which is either too little or way too much detail in most
situations. As an alternative, we provide the tool `nodesummary` to
show a hopefully more intuitive overview of the used/available
resources in AI Cloud.

![Screenshot of `nodesummary` in use.](assets/img/nodesummary.png)

## Selecting a partition

### The *batch* partition

The default partition in AI Cloud is *batch*. If you submit a job
without specifying a partition, e.g. `sbatch --gres=gpu:1
job_script.sh`, your job automatically gets run in the *batch*
partition. As shown in the `sinfo` example above, the batch partition
has a time limit of 12 hours and furthermore, jobs can get cancelled
(pre-empted) by other jobs running in other partitions. As a regular
user, the batch partition is the only way you can get access to the
special compute nodes mentioned in [Introduction -
Overview](introduction.md#overview) which belong to particular
research groups.

### The *prioritized* partition

All users also have access to the *prioritized* partition. As shown in
the `sinfo` example above, this partition has a 6-day time limit and
other jobs cannot cancel jobs in this partition. The 6-day time limit
is a temporary feature that we may decrease in the future when
everyone gets more used to re-queueing jobs.

In order to use the *prioritized* partition, you must specify it for
your jobs with the "--partition" or "-p" option:

???+ example

        sbatch -p prioritized --gres=gpu:1 job_script.sh

    Using the "-p" option to specify a partition for a batch job.

### Special partitions

If you belong to one of the research groups with your own server in AI
Cloud, you have been informed personally how to get first-priority
access to it.

Currently, these servers are associated with the partitions: *create*,
*aicentre1*, and *aicentre2*. By submitting your jobs to your group's
partition, you can run jobs on the server, even if it requires
cancelling jobs of users in the *batch* partition to provide you the
requested resources. For example, users from VAP lab at CREATE can use
their server nv-ai-04.srv.aau.dk by submitting jobs to the *create*
partition:

???+ example

        sbatch -p create --gres=gpu:1 job_script.sh

    Using the "-p" option to access a special partition. Only designated users of these partitions can access them.

The special partitions have no time limit.

**More information to be added here soon...**
