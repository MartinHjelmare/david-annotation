"""Handle chart report."""
# by courtesy of HuangYi @ 20110424
# modified by Martin Hjelmare @20160505
import csv
import os

from suds.client import Client

USER = 'user@email.org'


def david_enrich(list_file, id_type, bg_file=None, res_file=None,
                 bg_name='Background1', list_name='List1', category=None,
                 thd=0.1, count=2):
    """Get chart report and write it to file."""

    if list_file and os.path.exists(list_file):
        input_list_ids = ','.join(open(list_file).read().split('\n'))
        print 'List loaded.'
    else:
        print 'No list loaded.'
        return

    flag_bg = False
    if bg_file and os.path.exists(bg_file):
        input_bg_ids = ','.join(open(bg_file).read().split('\n'))
        flag_bg = True
        print 'Use file background.'
    else:
        print 'Use default background.'

    client = Client(
        'https://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService?'
        'wsdl')
    client.wsdl.services[0].setlocation(
        'https://david.abcc.ncifcrf.gov/webservice/services/DAVIDWebService.'
        'DAVIDWebServiceHttpSoap11Endpoint/')
    print 'User Authentication:', client.service.authenticate(
        USER)

    list_type = 0
    print 'Percentage mapped(list):', client.service.addList(
        input_list_ids, id_type, list_name, list_type)
    if flag_bg:
        list_type = 1
        print 'Percentage mapped(background):', client.service.addList(
            input_bg_ids, id_type, bg_name, list_type)

    print 'Use categories:', client.service.setCategories(category)
    chart_report = client.service.getChartReport(thd, count)
    print 'Total chart records:', len(chart_report)

    if not res_file or not os.path.exists(res_file):
        if flag_bg:
            res_file = list_file + '.withBG.chart_report.csv'
        else:
            res_file = list_file + '.chart_report.csv'

    with open(res_file, 'w') as csvfile:
        fieldnames = ['categoryName', 'termName', 'listHits', 'percent',
                      'ease', 'geneIds',
                      'listTotals', 'popHits', 'popTotals', 'foldEnrichment',
                      'bonferroni', 'benjamini', 'afdr']
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for row in chart_report:
            writer.writerow(dict(row))
        print 'write file:', res_file, 'finished!'

if __name__ == '__main__':
    david_enrich(list_file='./list1.txt', id_type='ENSEMBL_GENE_ID',
                 list_name='list1',
                 category='abcd,GOTERM_BP_FAT')
