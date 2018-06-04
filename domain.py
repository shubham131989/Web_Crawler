from urllib.parse import urlparse

def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).spilt('.')
        return results[-2] + '.' + results[-1]

    except:
        return ''

def get_sub_domain_name(url):
    try:
        return urlparse(url).neloc
    except:
        return ''
