#!/usr/bin/python3
import sewer.client, sys, time
from sewer.crypto import AcmeKey
sys.path.append("..") # Adds higher directory to python modules path.
from Class.cli import CLI
from Class import woodCDN #load woodCDN dns service

dns_class = woodCDN.woodCDNDns({})

cli = CLI()

status = cli.status()
if status is False: print("rqlite gone")
state = status['store']['raft']['state']

if state == "Leader":
    print("Getting doamins")
    domains = cli.query(["SELECT * FROM domains LEFT JOIN certs ON domains.domain=certs.domain"])
    if domains is False: print("rqlite gone")
    for row in domains['results'][0]['values']:
        print(row)
        if row[3] == None:
            print("Missing cert for",row[0])

            client = sewer.client.AcmeAccount(
                domain_name='*.'+row[0],
                dns_class=dns_class,
                acct_key=AcmeKey.create("rsa2048"),
                cert_key=AcmeKey.create("rsa2048")
            )


        else:
            print("Checking cert for",row[0])

else:
    print("Not leader, aborting.")
