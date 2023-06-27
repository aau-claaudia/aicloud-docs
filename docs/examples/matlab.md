It is possible to run MATLAB in AI Cloud

First, build your MATLAB image, e.g. like

???+ example
    
    ```console
    srun --cpus-per-task=6 singularity build matlab.sif docker://nvcr.io/partners/matlab:r2021b
    ```
    Please note that it may be possible to build a container with a newer
    version of MATLAB than the above, but our attempts to build the R2022b
    and R2023a versions of the container in AI Cloud have so far failed.

Then we need to set an environment variable such that MATLAB knows your license. In this case its convenient to point to the AAU license server:

???+ info

    ```console
    export MLM_LICENSE_FILE=27000@matlab.srv.aau.dk
    ```

Now you can start MATLAB with command line imnterface only as:

???+ example
    
    ```console
    srun --pty --gres=gpu:1 singularity exec --nv matlab.sif matlab -nodesktop
    ```

Please note that it is not possible to run MATLAB with a graphical
user interface, because Slurm is not configured for X-forwarding in AI
Cloud.
