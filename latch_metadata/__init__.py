import sys
from os import mkdir
from os.path import isdir
from pathlib import Path
from shutil import copy, copytree
from subprocess import run

import typing_extensions
from flytekit.core.annotation import FlyteAnnotation
from latch import custom_task, map_task, medium_task, small_task
from latch.ldata.path import LPath
from latch.resources.tasks import nextflow_runtime_task

# from latch.resources.tasks import map_task
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch.types.metadata import (
    Fork,
    ForkBranch,
    LatchAuthor,
    NextflowMetadata,
    NextflowParameter,
    NextflowRuntimeResources,
    Params,
    Section,
    Spoiler,
    Text,
)

from .parameters import generated_parameters

flow = [
    Section("Input/Output", Params("input", "outdir", "run_name")),
    Section(
        "Reference Genome Options",
        Fork(
            "genome_source",
            "",
            latch_genome_source=ForkBranch(
                "Latch Certified Reference Genome", Params("genome")
            ),
            input_ref=ForkBranch(
                "Custom Reference Genome",
                Params("fasta", "gtf", "gff"),
                Spoiler(
                    "Reference Options",
                    Params("gff", "gene_bed", "tss_bed", "save_reference"),
                ),
            ),
        ),
    ),
    Section(
        "Aligners",
        Params("aligner"),
        Spoiler(
            "Aligner Options",
            Fork(
                "Aligner_Options",
                "",
                bt2=ForkBranch("BowTie2", Params("bowtie2_index")),
                bwa=ForkBranch("BWAMem", Params("bwa_index", "nwq_min_index")),
                chrmap=ForkBranch("Chromap", Params("chromap_index")),
                star=ForkBranch("Star", Params("star_index")),
            ),
        ),
        Spoiler(
            "Alignment Filters",
            Params(
                "keep_dups",
                "keep_multi_map",
                "save_align_intermeds",
                "save_unaligned",
                "blacklist",
                "mito_name",
                "keep_mito",
            ),
        ),
    ),
    Section(
        "MACS2 Options",
        Params("macs_gsize", "read_length"),
        Spoiler(
            "MACS2 Optional Parameters",
            Params(
                "narrow_peak",
                "broad_cutoff",
                "macs_fdr",
                "macs_pvalue",
                "min_reps_consensus",
                "save_macs_pileup",
                "skip_peak_qc",
                "skip_peak_annotation",
                "skip_consensus_peaks",
                "skip_merge_replicates",
            ),
        ),
    ),
    Spoiler(
        "Optional Parameters",
        Spoiler(
            "Adapter trimming options",
            Params(
                "clip_r1",
                "clip_r2",
                "three_prime_clip_r1",
                "three_prime_clip_r2",
                "trim_nextseq",
                "min_trimmed_reads",
                "skip_trimming",
                "save_trimmed",
            ),
        ),
        Spoiler(
            "DESeq2 Options",
            Params("skip_deseq2_qc", "deseq2_vst"),
        ),
        Spoiler(
            "MultiQC Options",
            Params("multiqc_title", "skip_multiqc", "multiqc_methods_description"),
        ),
        Spoiler("ATAQV Options", Params("ataqv_mito_reference", "skip_ataqv")),
        Spoiler(
            "Skip Tools",
            Params(
                "skip_fastqc",
                "skip_picard_metrics",
                "skip_preseq",
                "skip_plot_profile",
                "skip_plot_fingerprint",
                "skip_igv",
            ),
        ),
        Spoiler(
            "Misc. Sample Information",
            Params("fragment_size", "seq_center", "with_control"),
        ),
    ),
]
NextflowMetadata(
    display_name="nf-core/atacseq",
    author=LatchAuthor(
        name="Your Name",
    ),
    parameters=generated_parameters,
    runtime_resources=NextflowRuntimeResources(
        cpus=4,
        memory=8,
        storage_gib=100,
    ),
    log_dir=LatchDir("latch:///your_log_dir"),
    flow=flow,
)
