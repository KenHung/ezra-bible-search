"""Get phases got cut accidentally in tokenization."""
from __future__ import absolute_import

import argparse
import logging
import sys

import apache_beam as beam
from apache_beam.io import ReadFromText, WriteToText
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from past.builtins import unicode


def run(argv=None, save_main_session=True):
    """Main entry point"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='test_vocabs.txt',
        help='Input file to process.')
    parser.add_argument(
        '--output',
        dest='output',
        default='phases_got_cut.txt',
        help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_args.extend([
        '--runner=DataflowRunner',
        '--project=ezra-bible-search',
        '--region=asia-east1',
        '--staging_location=gs://ezra-bible-data/staging',
        '--temp_location=gs://ezra-bible-data/tmp',
        '--job_name=phases-got-cut-job',
    ])

    with open('tokenized_verses.txt') as f:
        lines = f.readlines()[:10]

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(
        SetupOptions).save_main_session = save_main_session
    with beam.Pipeline(options=pipeline_options) as p:

        # Read the text file[pattern] into a PCollection.
        vocabs = p | ReadFromText(known_args.input)

        def check_vocab_got_cut(vocab: str) -> bool:
            for line in lines:
                words = line.split()
                for n in range(len(words) - 1):
                    possible_phase = words[n] + words[n + 1]
                    if vocab == possible_phase:
                        return True
            return False

        phases_got_cut = (
            vocabs
            | 'check' >> beam.Map(lambda v: (v, check_vocab_got_cut(v)))
            | 'phases cut' >> beam.Filter(lambda x: x[1]))

        # Write the output using a "Write" transform that has side effects.
        # pylint: disable=expression-not-assigned
        phases_got_cut | WriteToText(known_args.output)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
