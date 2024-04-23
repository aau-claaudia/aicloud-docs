FILENAME=tensorflow_keras.sif
GPUS=2

build:
	rm -f $(FILENAME)
	srun --time=1:00:00 --mem=60G singularity build --fakeroot $(FILENAME) Singularity

run:
	sbatch jobscript.sh

runsingle:
	sbatch jobscript_single.sh

interactive:
	srun --ntasks=$(GPUS) --pty --time=1:00:00 --gres=gpu:$(GPUS) --qos=allgpus singularity shell --nv -B .:/code -B output_data:/output_data $(FILENAME)
