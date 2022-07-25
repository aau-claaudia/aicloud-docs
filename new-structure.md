# New structure for AI Cloud documentation

This is the existing structure of the documentation from the website,
taken from mkdocs.yml:

- Front page: almost empty front page where you have to select for
  example "Introduction" from the top menu to see something useful.
- Introduction: introduction.md
- "Additional examples":
  - "Interactive TensorFlow": examples/interactive_tensorflow.md
  - "Jupyter notebook using TensorFlow container": examples/jupyter.md
  - "PyTorch and Anaconda": examples/pytorch_anaconda.md
  - "Matlab": examples/matlab.md
  - "PyTorch and multi-precision training": torch_amp_example/README.md
  - "Multi-GPU data parallelism training with Horovod and Keras": multi_gpu_keras/README.md
  - "PyTorch and automatic mixed precision with APEX": torch_amp_example/README.md
  - "Python pip in containters": examples/pip_in_containers.md
- "Workshop": workshop/workshop.md
- "Additional resources": additional.md

This is the proposed new structure of the documentation:

- Front page: What is AI Cloud and what can I use it for?
- Overview:
  - Physical systems, distinction between AI Cloud pilot platform and
    (new) AI Cloud.
  - Major software components; SSH connectivity, Slurm resource
    management, Singularity containerisation.
- Introduction; typical minimal workflow of connecting, transferring
  data, obtaining container, running job.
- Queueing details and policy
<!-- remainder planned as unchanged for now -->
- Use cases:
  - "Interactive TensorFlow": examples/interactive_tensorflow.md
  - "Jupyter notebook using TensorFlow container": examples/jupyter.md
  - "PyTorch and Anaconda": examples/pytorch_anaconda.md
  - "Matlab": examples/matlab.md
  - "PyTorch and multi-precision training": torch_amp_example/README.md
  - "Multi-GPU data parallelism training with Horovod and Keras": multi_gpu_keras/README.md
  - "PyTorch and automatic mixed precision with APEX": torch_amp_example/README.md
  - "Python pip in containters": examples/pip_in_containers.md
- "Workshop": workshop/workshop.md
- "Additional resources": additional.md
