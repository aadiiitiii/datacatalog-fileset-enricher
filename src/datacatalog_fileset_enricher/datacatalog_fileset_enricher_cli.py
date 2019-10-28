import argparse
import logging

from .datacatalog_fileset_enricher import DatacatalogFilesetEnricher


class DatacatalogFilesetEnricherCLI:

    @classmethod
    def run(cls):
        cls.__setup_logging()
        cls.__parse_args()

    @classmethod
    def __setup_logging(cls):
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def __parse_args(cls):
        parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        parser.add_argument('--project-id', help='Project id', required=True)

        parser.set_defaults(func=lambda *inner_args: logging.info('Must use a subcommand'))

        subparsers = parser.add_subparsers()

        enrich_filesets = subparsers.add_parser('enrich-gcs-filesets',
                                                help='Enrich filesets with Tags')

        enrich_filesets.add_argument('--entry-group-id',
                                     help='Entry Group ID')
        enrich_filesets.add_argument('--entry-id',
                                     help='Entry ID')
        enrich_filesets.set_defaults(func=cls.__enrich_fileset)

        clean_up_tags = subparsers.add_parser(
            'clean-up-templates-and-tags',
            help='Clean up the Fileset Enhancer Template and Tags From the Fileset Entries')
        clean_up_tags.set_defaults(func=cls.__clean_up_fileset_template_and_tags)

        clean_up_all = subparsers.add_parser(
            'clean-up-all',
            help='Clean up Fileset Entries, Their Tags and the Fileset Enhancer Template')
        clean_up_all.set_defaults(func=cls.__clean_up_all)

        args = parser.parse_args()
        args.func(args)

    @classmethod
    def __enrich_fileset(cls, args):
        DatacatalogFilesetEnricher(args.project_id).run()

    @classmethod
    def __clean_up_fileset_template_and_tags(cls, args):
        DatacatalogFilesetEnricher(args.project_id).clean_up_fileset_template_and_tags()

    @classmethod
    def __clean_up_all(cls, args):
        DatacatalogFilesetEnricher(args.project_id).clean_up_all()