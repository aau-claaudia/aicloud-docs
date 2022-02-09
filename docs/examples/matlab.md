It is possible to run Matlab both with and without GUI

First, build your Matlab image, e.g. like

```console
srun --cpus-per-task=6 singularity build matlab.sif docker://nvcr.io/partners/matlab:r2019b
```

Then we need to set an environment variable such that matlab knows your license. In this case its convenient to point to the AAU license server

```console
export MLM_LICENSE_FILE=27000@matlab.srv.aau.dk
```

Now you can start Matlab with pure command line as

```console
srun --pty --gres=gpu:1 singularity exec --nv matlab.sif matlab -nodesktop
```

