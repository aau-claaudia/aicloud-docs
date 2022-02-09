The NVIDIA DGX-2 comes with specialized hardware for moving data between GPUs: [NVLinks and NVSwitches](https://www.nvidia.com/en-us/data-center/nvlink/). One approach to utilizing these links is using the MVDIA Collective Communication Library ([NCCL](https://developer.nvidia.com/NCCL)). NCCL is compatible with the Message Passing Interface (MPI) used in many HPC applications and facilities. This in turn is build into the Horovod framework for data parallelism training supporting many deep learning frameworks requiring only minor changes in the source code. In [this example](https://github.com/aau-claaudia/aicloud-docs/tree/master/docs/multi_gpu_keras) we show how to run Horovod on our system, including Slurm settings. You can then adapt this example for you preferred framework as described in the [Horovod documentation](https://horovod.readthedocs.io/en/stable/)

## Multi-GPU with Tensorflow-Keras and Horovod

There several methods to perform multi-GPU training. In this example we consider a example with Keras bundled with TensorFlow and Horovod.

https://horovod.readthedocs.io/en/stable/

Horovod is a distributed deep learning data parallelism framework that supports Keras, PyTorch, MXNet and TensorFlow. In this example we will look at training on a single node using Keras with OpenMPI, NCCL and NVLink behind the scenes.

Newer images from NGC [come with Horovod](https://on-demand.gputechconf.com/gtc-cn/2018/pdf/CH8209.pdf) leveraging a number of features on the system, so in this example we first build a standard TensorFlow image (including Keras).

```bash
$ make build
```

You can see how it is built in the files Makefile and Singularity. Next we update a few lines in our code. Have a look at the [Horovod-Keras](https://horovod.readthedocs.io/en/stable/keras.html) documentation or in [example.py](example.py).

Next we build our setup as a Slurm batch script

```bash
#!/bin/bash
#SBATCH --job-name MGPU
#SBATCH --time=1:00:00
#SBATCH --qos=allgpus
#SBATCH --gres=gpu:4
#SBATCH --mem=60G
#SBATCH --cpus-per-gpu=4
#SBATCH --ntasks=4

echo "Date              = $(date)"
echo "Hostname          = $(hostname -s)"
echo "Working Directory = $(pwd)"
echo "JOB ID            = $SLURM_JOB_ID"
echo ""
echo "Hostname                       = $SLURM_NODELIST"
echo "Number of Tasks Allocated      = $SLURM_NTASKS"
echo "Number of CPUs on host         = $SLURM_CPUS_ON_NODE"
echo "GPUs                           = $GPU_DEVICE_ORDINAL"

nvidia-smi nvlink -gt d > nvlink_start-$SLURM_JOB_ID.out
nvidia-smi --query-gpu=index,timestamp,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free --format=csv -l 5 > util-$SLURM_JOB_ID.csv &
singularity exec --nv -B .:/code -B output_data:/output_data tensorflow_keras.sif horovodrun -np $SLURM_NTASKS --mpi-args="-x NCCL_DEBUG=INFO" python /code/example.py
nvidia-smi nvlink -gt d > nvlink_end-$SLURM_JOB_ID.out
```

In this case we are allocating 4 GPUs. Note that we also select 4 tasks. We then proceed with recording a few pieces of information in our slurm-\<jobid\> output that could come in handy. Next we would like to collect a bit of information on the amount of data transferred over the NVLinks - we both do this at the start and end of the job such that we can see the difference. We also collect the GPU utilization in a file to see how well the GPU is utilized.

The line

```bash
singularity exec --nv -B .:/code -B output_data:/output_data tensorflow_keras.sif horovodrun -np $SLURM_NTASKS --mpi-args="-x NCCL_DEBUG=INFO" python /code/example.py
```

is the key line here. We use our TensorFlow/Keras image and run the [MPI wrapper](https://horovod.readthedocs.io/en/stable/mpi_include.html) `horovodrun` using `SLURM_NTASKS=4` processes. We here use an [inside-out or self-contained](https://developer.nvidia.com/blog/how-to-run-ngc-deep-learning-containers-with-singularity/) approach where we use `horovodrun`/`mpirun` from inside the container.

We can also check the available [features](https://horovod.readthedocs.io/en/stable/install_include.html#check-build) of Horovod from inside the container using:

```bash
horovodrun --check-build


Available Frameworks:
    [X] TensorFlow
    [ ] PyTorch
    [ ] MXNet

Available Controllers:
    [X] MPI
    [X] Gloo

Available Tensor Operations:
    [X] NCCL
    [ ] DDL
    [ ] CCL
    [X] MPI
    [X] Gloo    
```


We can then have a look at the different solutions with say 1 and 4 GPUs using the Makefile running the batch scripts as

```bash
make run
make runsingle
```

and investigate the runtime ('slurm-\<jobid\>'), GPU utilization ('util-\<jobid\>') and the amount of data moved during execution in 'nvlink_start-\<jobid\>' and 'nvlink_end-\<jobid\>'.

First, we have a look in 'slurm-\<jobid\>' and observe lines with P2P [indicating usage of NVLINK](https://on-demand.gputechconf.com/gtc-cn/2018/pdf/CH8209.pdf):

```bash
[1,0]<stdout>:nv-ai-03:62491:62509 [0] NCCL INFO Channel 11 : 0[39000] -> 1[57000] via P2P/IPC
....
[1,0]<stdout>:nv-ai-03:62491:62509 [0] NCCL INFO 12 coll channels, 16 p2p channels, 16 p2p channels per peer
```

We can also have a look and compare 'nvlink_start-\<jobid\>' and 'nvlink_end-\<jobid\>' to see the delta between the two times.

start:
```bash
...
GPU 3: Tesla V100-SXM3-32GB (UUID: GPU-295726b4-8888-d1eb-5965-a70cbb91d136)
	 Link 0: Data Tx: 19241022 KiB
	 Link 0: Data Rx: 19255516 KiB
...
```

end:

```bash
...
GPU 3: Tesla V100-SXM3-32GB (UUID: GPU-295726b4-8888-d1eb-5965-a70cbb91d136)
	 Link 0: Data Tx: 20886285 KiB
	 Link 0: Data Rx: 20904969 KiB
...
```

For the single GPU job, the delta is zero.

We can also observe the final outputs of the 4-GPU training

```bash
cat slurm-95659.out | (head -n 10; tail -n 3)
Date              = Wed  3 Feb 10:15:18 CET 2021
Hostname          = nv-ai-03
Working Directory = /user/its.aau.dk/tlj/docs_aicloud/aicloud_slurm/multi_gpu_keras
JOB ID            = 95659

Hostname                       = nv-ai-03.srv.aau.dk
Number of Tasks Allocated      = 4
Number of CPUs on host         = 8
GPUs                           = 0,1,2,3
2021-02-03 10:15:23.012238: I tensorflow/stream_executor/platform/default/dso_loader.cc:49] Successfully opened dynamic library libcudart.so.11.0
[1,0]<stdout>:Test loss: 0.01960514299571514
[1,0]<stdout>:Test accuracy: 0.9936000108718872
[1,0]<stdout>:Train time: 124.74971508979797
```

and the single-GPU training

```bash
$ cat slurm-95660.out | (head -n 10; tail -n 3)
Date              = Wed  3 Feb 10:15:21 CET 2021
Hostname          = nv-ai-03
Working Directory = /user/its.aau.dk/tlj/docs_aicloud/aicloud_slurm/multi_gpu_keras
JOB ID            = 95660

Hostname                       = nv-ai-03.srv.aau.dk
Number of Tasks Allocated      = 1
Number of CPUs on host         = 2
GPUs                           = 0
2021-02-03 10:15:24.461425: I tensorflow/stream_executor/platform/default/dso_loader.cc:49] Successfully opened dynamic library libcudart.so.11.0
[1,0]<stdout>:Test loss: 0.022991640493273735
[1,0]<stdout>:Test accuracy: 0.9926000237464905
[1,0]<stdout>:Train time: 472.6957468986511
```

Due to random start and change of effective batch size, we will not end at the exact same solution but we do observe comparable results, and that the 4-GPU solution is approximately x4 times faster.

This job is with a small model and dataset, so it is difficult to achieve high utilization. This is an example to get started :-)