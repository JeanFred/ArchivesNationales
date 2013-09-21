# -*- coding: utf-8 -*-

"""Partnership with the Archives Nationales."""

__authors__ = 'User:Jean-Frédéric'

import os
import sys
import re
from uploadlibrary import metadata
from uploadlibrary.UploadBot import DataIngestionBot, UploadBotArgumentParser
from processors import split_and_apply_template_on_each, look_for_sizes
reload(sys)
sys.setdefaultencoding('utf-8')



class ArchivesMetadataCollection(metadata.MetadataCollection):

    """Handling the metadata collection."""

    def handle_record(self, image_metadata):
        """Handle a record."""
        filename = image_metadata['Fichier']
        path = os.path.abspath(os.path.join('.', 'WIKI', filename))
        image_metadata['subst'] = 'subst:'
        return metadata.MetadataRecord(path, image_metadata)


def main(args):
    """Main method."""
    collection = ArchivesMetadataCollection()
    csv_file = 'Metadata_ArchivesNationales.csv'
    collection.retrieve_metadata_from_csv(csv_file, delimiter=',')

    alignment_template = 'User:Jean-Frédéric/AlignmentRow'.encode('utf-8')

    if args.prepare_alignment:
        for key, value in collection.count_metadata_values().items():
            collection.write_dict_as_wiki(value, key, 'wiki',
                                          alignment_template)

    if args.post_process:
        alignment_fields = []
        collection.retrieve_metadata_alignments(alignment_fields,
                                                alignment_template)

        reader = collection.post_process_collection(None)
        template_name = 'subst:Commons:Archives_Nationales/Ingestion'.encode('utf-8')
        front_titlefmt = ""
        variable_titlefmt = "%(Titre du document)s"
        rear_titlefmt = " - Archives Nationales - %(Cote du document)s"
        uploadBot = DataIngestionBot(reader=reader,
                                     front_titlefmt=front_titlefmt,
                                     rear_titlefmt=rear_titlefmt,
                                     variable_titlefmt=variable_titlefmt,
                                     pagefmt=template_name)

    if args.upload:
        uploadBot.doSingle()
    elif args.dry_run:
        uploadBot.dry_run()


if __name__ == "__main__":
    parser = UploadBotArgumentParser()
    arguments = parser.parse_args()
    if not any(arguments.__dict__.values()):
        parser.print_help()
    else:
        main(arguments)
