from sewer import auth
from sewer import lib

class woodCDNDns(auth.DNSProviderBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setup(self, challenges):
        for challenge in challenges:
            fqdn = self.target_domain(challenge)
            txt_value = lib.dns_challenge(challenge["key_auth"])
            self.my_api_add_txt(fqdn, txt_value)

    def unpropagated(self, challenges):
        return []  # if service has a propagation check, use it here

    def clear(self, challenges):
        print("setup")
        # like setup, but calling my_api_del_txt; may not need txt_value

    def my_api_add_txt(self, fqdn, txt_value):
        print("adding txt record",txt_value)
        # this is where you talk to the DNS service to add a TXT

    def my_api_del_txt(self, fqdn):
        print("deleting txt record",txt_value)
        # talk to DNS service to remove TXT
