#!/usr/bin/python3
import json
import requests
import xmltodict

yeezy = 'https://yeezysupply.com/sitemap.xml'
boring = 'https://www.boringcompany.com/sitemap.xml'
kith = 'https://kith.com/sitemap.xml'


class Sitemap():
    def __init__(self):
        self.xml_dict = {}

    def build_dict(self, sitemap_url, sitemap_data):
        for url in sitemap_data['urlset']['url']:
            try:
                # need to include url['image:image']['image:title'] and make the datatype dict
                self.xml_dict[sitemap_url].update({url['image:image']['image:title']:url['loc']})
            except:
                # if self.xml_dict[sitemap_url].get(url['loc'].split('/')[-1]) is not None:
                #     print('Url key already exists')
                if url['loc'].split('/')[-1] == '':
                    url_key = 'ROOT'
                else:
                    url_key = url['loc'].split('/')[-1]
                self.xml_dict[sitemap_url].update({url_key:url['loc']})

    def parse_sitemap(self, xml_urls):
        for xml_url in xml_urls:
            self.xml_dict[xml_url] = {}
            xml = requests.request('GET', xml_url).content
            data = xmltodict.parse(xml)
            if data.get('sitemapindex') is not None:
                for sitemaps in data['sitemapindex']['sitemap']:
                    self.xml_dict[xml_url].update({sitemaps['loc']:''})
                for sitemaps in data['sitemapindex']['sitemap']:
                    self.parse_sitemap([sitemaps['loc']])
            else:
                self.build_dict(xml_url, data)
        return self.xml_dict


s = Sitemap()
print(json.dumps(s.parse_sitemap([yeezy, boring, kith]), indent=4))
