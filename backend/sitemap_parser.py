import xmltodict
import requests
from typing import List

def extract_sitemap(domain: str) -> List[str] | None:
    try:
        url = f'https://{domain}/sitemap.xml'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'No sitemap available for {domain}')
            return None

        data = response.text

        sitemap = xmltodict.parse(data)['urlset'] # the top-level element is <urlset>
        urls = [url.loc for url in sitemap['url']]
        return urls
    except requests.exceptions.RequestException as e:
        print(f'Unable to get sitemap for domain {domain}:', e)
    except requests.exceptions.ConnectTimeout as e:
        print(f'Unable to reach {domain} in time', e)
    return None
