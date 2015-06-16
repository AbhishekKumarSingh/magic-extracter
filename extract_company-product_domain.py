import re
import subprocess


def findAllChar(str, ch):
    '''finds all the occurrences of letter ch in string str
       and returns corrosponding indexes
    '''
    return [i for i, letter in enumerate(str) if letter == ch]

def extract_domain(raw_domain):
    '''returns a higher level domain from
       a given domain tree.
    '''
    indexes = findAllChar(raw_domain, '.')
    if len(indexes) > 1:
        indexes.pop()
        i = indexes.pop()
        return raw_domain[i+1:]
    else:
        return raw_domain

def store(input_domain, raw_domain_list):
    '''takes company domain name and their product domain
       name as input and write the info to a file
    '''
    pdomain = []
    for dname in raw_domain_list:
        domain = extract_domain(dname).lower()
        if domain != 'google.com' and domain[0] != input_domain[0] and domain not in pdomain:
            pdomain.append(domain)

    # write info to data.txt file
    f = open('data.txt', 'a')

    f.write(input_domain+' : '+str(pdomain)+'\n')
    f.close()

def extract_product_domain_info(cdomain_list):
    '''dig lookup is performed on each company domain from the cdomain_list
       and the output is parsed to get product domain info and further the
       whole company-product domain info is written to data.txt file.
    '''
    regex = '(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}'
    pattern = re.compile(regex)

    for cdomain in cdomain_list:
        output = subprocess.check_output(['dig', cdomain, 'any'])
        raw_domain_list = re.findall(pattern, output)
        store(cdomain, raw_domain_list)


if __name__ == '__main__':
    cdomain_list = ['supportbee.com', 'mailgun.com', 'credii.com']
    extract_product_domain_info(cdomain_list)
