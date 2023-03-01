all: SlurmAndSingularityTraining.pdf AiCloudOverview.pdf

SlurmAndSingularityTraining.pdf: singularity-doc-preamble.md SlurmAndSingularityTraining.md
	pandoc singularity-doc-preamble.md SlurmAndSingularityTraining.md -o SlurmAndSingularityTraining.pdf -t beamer --slide-level=2 --pdf-engine=xelatex --pdf-engine-opt=-shell-escape
AiCloudOverview.pdf: singularity-doc-preamble.md AiCloudOverview.md
	pandoc singularity-doc-preamble.md AiCloudOverview.md -o AiCloudOverview.pdf -t beamer --slide-level=2 --pdf-engine=xelatex --pdf-engine-opt=-shell-escape
