from collections import defaultdict
from MuTest.BasicUtilities.MongoUtilities import connect_to_mongo
from MuTest.SupportLibraries.DataGatherer import query_processor
import ast
import csv

def NormalNormalAggregator(query, output_filename):

    collection = connect_to_mongo(collection='NormalNormalData')

    query = query_processor(query)

    bam_sets=defaultdict(set)

    for record in collection.find(ast.literal_eval(query)):
        bam_sets[(record['project'],record['dataset'])].add(record['file'])


    for bam_set in bam_sets:

        fieldnames=['tumor_bam','normal_bam','data_filename','project','dataset','sample','evidence_type','author']
        file = csv.DictWriter(open(output_filename,'w'),fieldnames=fieldnames,delimiter='\t')

        bams = list(bam_sets[bam_set])
        n = len(bams)

        project = bam_set[0]
        dataset = bam_set[1]

        for i in range(n):
            for j in range(n):
                if i == j: continue

                bam1 = bams[i]
                bam2 = bams[j]

                row={'tumor_bam':bam1,
                 'normal_bam':bam2,
                 'data_filename':'.' ,
                 'project': project,
                 'dataset': dataset,
                 'sample': '%d-%d'%(i,j),
                 'evidence_type': 'NN',
                 'author': 'None'}

                csv.writerow(row)
