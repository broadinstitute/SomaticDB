from collections import defaultdict
import ast
import os
import random

import argparse
from SomaticDB.BasicUtilities.MongoUtilities import connect_to_mongo
from SomaticDB.SupportLibraries.DataGatherer import query_processor


def get_sample_name(filename):
    sample_name = filename.split('/')[4]
    return sample_name

script_description="""A protype script for figuring out what bams one needs to run one's samples on"""
script_epilog="""Created for evaluation of performance of Mutect 2 positives evaluation """




def BamAggregator(query, normal_bam_list, tumor_bam_list, interval_list):

    collection = connect_to_mongo()

    tumor_bam_list  = set([])
    normal_bam_list = set([])
    interval_list   = defaultdict(set)

    query = query_processor(query)

    for record in collection.find(ast.literal_eval(query)):

        if not record.has_key('tumor_bam'):
            print record
            continue

        tumor_bam  = record['tumor_bam']
        normal_bam = record['normal_bam']

        interval = "%s:%s-%s" % (record['chromosome'],
                                 record['start'],
                                 record['end'])

        interval_list[(tumor_bam, normal_bam)].add(interval)

    tumor_bam_file = open(tumor_bam_list,'w')
    normal_bam_file = open(normal_bam_list,'w')
    interval_file = open(interval_list,'w')

    file_stem, file_ext = os.path.splitext(tumor_bam_list)

    for pair in interval_list:
        tumor_bam, normal_bam = pair
        tumor_bam_file.write(tumor_bam+'\n')
        normal_bam_file.write(normal_bam+'\n')

        #sample = get_sample_name(tumor_bam)
        sample =\
            "".join([random.choice('abcdef0123456789') for k in range(40)])

        print sample

        current_filename = "intervals."+sample+".list"

        current_interval_file = open(current_filename,'w')

        for interval in list(interval_list[pair]):
            current_interval_file.write(interval+"\n")

        current_interval_file.close()

        interval_file.write( current_filename +'\n')

    tumor_bam_file.close()
    normal_bam_file.close()
    interval_file.close()

