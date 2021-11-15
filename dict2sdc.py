#!/usr/bin/python
# -*- coding: utf-8-sig -*-
import csv
import json
import pywikibot


class WikidataSDCBot:
    """
    A bot to enrich and create paintings on Wikidata
    """
    def __init__(self):
        """
        Arguments:
            * generator    - A generator that yields Dict objects.

        """
        self.site = pywikibot.Site('commons', 'commons')
        self.site.login()
        self.site.get_tokens('csrf')
        self.repo = self.site.data_repository()
        self.duplicates = []
        self.processeditems = []

    def run(self):
        """
        Starts the robot.
        """
        
        with open( 'dict.csv', 'r', encoding='UTF8' ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                claims = []
             
                # Source
                toclaim = {'mainsnak': { 'snaktype': 'value',
                                         'property': 'P7482',
                                         'datavalue': { 'value': { 'numeric-id': 74228490,
                                                                   'id' : 'Q74228490',
                                                                   },
                                                        'type' : 'wikibase-entityid',
                                                        }

                                         },
                           'type': 'statement',
                           'rank': 'normal',
                           'qualifiers' : {'P973' : [ {'snaktype': 'value',
                                                       'property': 'P973',
                                                       'datavalue': { 'value': row['URL'],
                                                                      'type' : 'string',
                                                                      },
                                                       } ],
                                           },
                           }
                toclaim['qualifiers']['P137'] = [ {'snaktype': 'value',
                                                   'property': 'P137',
                                                   'datavalue': { 'value': { 'numeric-id': 1526131,
                                                                             'id' : 'Q1526131',
                                                                             },
                                                                  'type' : 'wikibase-entityid',
                                                                  },
                                                   } ]

                claims.append(toclaim)
                itemdata = {'claims' : claims}
                token = self.site.tokens['csrf']
                postdata = {'action' : 'wbeditentity',
                            'format' : 'json',
                            'id' :  row['MID'],
                            'data' : json.dumps(itemdata),
                            'token' : token,
                            'summary' : "Add SDC",
                            'bot' : True,
                            }
                #print (json.dumps(postdata, sort_keys=True, indent=4))
                request = self.site._simple_request(**postdata)
                     
                data = request.submit()

def main():
    wikidataSDCBot = WikidataSDCBot()
    wikidataSDCBot.run()

if __name__ == "__main__":
    main()
