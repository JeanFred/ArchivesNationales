# -*- coding: utf-8 -*-

"""Partnership with the Archives Nationales."""

__authors__ = 'User:Jean-Frédéric'

import os
import sys
import re
from uploadlibrary import metadata
from uploadlibrary.UploadBot import DataIngestionBot, UploadBotArgumentParser
from processors import split_and_apply_template_on_each, look_for_sizes
import uploadlibrary.PostProcessing as commonprocessors
reload(sys)
sys.setdefaultencoding('utf-8')



class ArchivesMetadataCollection(metadata.MetadataCollection):

    """Handling the metadata collection."""

    def handle_record(self, image_metadata):
        """Handle a record."""
        filename = image_metadata['Fichier']
        path = os.path.abspath(os.path.join('.', 'third', filename))
        return metadata.MetadataRecord(path, image_metadata)


def main(args):
    """Main method."""
    collection = ArchivesMetadataCollection()
    csv_file = 'Metadata_ArchivesNationales3-Cut.csv'
    collection.retrieve_metadata_from_csv(csv_file, delimiter=';')

    alignment_template = 'User:Jean-Frédéric/AlignmentRow'.encode('utf-8')

    if args.prepare_alignment:
        for key, value in collection.count_metadata_values().items():
            collection.write_dict_as_wiki(value, key, 'wiki',
                                          alignment_template)

    if args.post_process:
        mapping_fields = []
        mapper = commonprocessors.retrieve_metadata_alignments(mapping_fields,
                                                               alignment_template)
        mapping_methods = {
        'Support': commonprocessors.map_and_apply_technique(),
        'Dimensions du document': (commonprocessors.parse_format, {}),
        'Date du document': (commonprocessors.look_for_date, {}),
        'Description du document': (commonprocessors.remove_linebreaks, {}),
        'Cote du document': (commonprocessors.remove_linebreaks, {}),
        'Titre du document': (commonprocessors.remove_linebreaks, {})
        }

        categories_counter, categories_count_per_file = collection.post_process_collection(mapping_methods)
        #metadata.categorisation_statistics(categories_counter, categories_count_per_file)


    template_name = 'Commons:Archives_Nationales/Ingestion'.encode('utf-8')
    front_titlefmt = ""
    variable_titlefmt = "%(Titre du document)s %(Page)s"
    rear_titlefmt = " - Archives Nationales - %(Cote du document)s"
    reader = iter(collection.records)
    uploadBot = DataIngestionBot(reader=reader,
                                 front_titlefmt=front_titlefmt,
                                 rear_titlefmt=rear_titlefmt,
                                 variable_titlefmt=variable_titlefmt,
                                 pagefmt=template_name)

    reader = iter(collection.records)
    uploadBot = DataIngestionBot(reader=iter(reader),
                                 front_titlefmt=front_titlefmt,
                                 rear_titlefmt=rear_titlefmt,
                                 variable_titlefmt=variable_titlefmt,
                                 pagefmt=template_name,
                                 subst=True,
                                 verifyDescription=False
                                 )

    if args.upload:
        uploadBot.run()
    elif args.dry_run:
        uploadBot.dry_run()


if __name__ == "__main__":
    parser = UploadBotArgumentParser()
    arguments = parser.parse_args()
    if not any(arguments.__dict__.values()):
        parser.print_help()
    else:
        main(arguments)
