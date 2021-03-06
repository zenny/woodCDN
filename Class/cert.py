from Class.rqlite import rqlite
from Class.cli import CLI
import simple_acme_dns, json, time, os

class Cert(rqlite):

    def __init__(self):
        self.cli = CLI()

    def addCert(self,data):
        print("adding",data[0])
        response = self.execute(['INSERT INTO certs(domain,subdomain,fullchain,privkey,updated) VALUES(?, ?, ?, ?, ?)',data[0],data[1],data[2],data[3],data[4]])
        print(json.dumps(response, indent=4, sort_keys=True))

    def updateCert(self,data):
        print("updating",data[0])
        response = self.execute(['UPDATE certs SET fullchain = ?,privkey = ?,updated = ? WHERE domain = ? AND subdomain =?',data[2],data[3],data[4],data[0],data[1]])
        print(json.dumps(response, indent=4, sort_keys=True))

    def deleteCert(self,data):
        response = self.execute(['DELETE FROM certs WHERE domain=? and subdomain=?',data[0],data[1]])
        print(json.dumps(response, indent=4, sort_keys=True))

    def getCert(self,fullDomain,domain,subdomain,email,update=False):
        directory = "https://acme-v02.api.letsencrypt.org/directory"
        #directory = "https://acme-staging-v02.api.letsencrypt.org/directory"
        try:
            client = simple_acme_dns.ACMEClient(domains=[fullDomain],email=email,directory=directory,nameservers=["8.8.8.8", "1.1.1.1"],new_account=True,generate_csr=True)
        except Exception as e:
            print(e)
            return False

        for acmeDomain, token in client.request_verification_tokens():
            print("adding {domain} --> {token}".format(domain=acmeDomain, token=token))
            response = self.cli.addVHost([domain,"_acme-challenge."+subdomain,'TXT',token])
            if response is False: return False

        print("Waiting for dns propagation")
        try:
            if client.check_dns_propagation(timeout=1200):
                print("Requesting certificate")
                client.request_certificate()
                fullchain = client.certificate.decode()
                privkey = client.private_key.decode()
                if update is False:
                    self.addCert([domain,subdomain,fullchain,privkey,int(time.time())])
                else:
                    self.updateCert([domain,subdomain,fullchain,privkey,int(time.time())])
            else:
                print("Failed to issue certificate for " + str(client.domains))
                client.deactivate_account()
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            self.cli.deleteVhost([domain,"_acme-challenge."+subdomain,'TXT'])

        return True

    def syncCerts(self,current,files,path):
        #certs removed from database
        for file in files:
            if file not in current:
                os.remove(path+file)
