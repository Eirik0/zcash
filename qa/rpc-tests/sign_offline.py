#!/usr/bin/env python2

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, initialize_chain_clean, start_node

class SignOfflineTest (BitcoinTestFramework):
# Setup Methods
    def setup_chain(self):
        print "Initializing test directory " + self.options.tmpdir
        initialize_chain_clean(self.options.tmpdir, 2)

    def setup_network(self):
        self.nodes = [ start_node(0, self.options.tmpdir) ]
        self.is_network_split = False
        self.sync_all()

    # Tests
    def run_test(self):
        print "Mining blocks..."
        self.nodes[0].generate(101)

        offline_node = start_node(1, self.options.tmpdir, ["-maxconnections=0"])
        self.nodes.append(offline_node)

        assert_equal(0, len(offline_node.getpeerinfo())) # make sure node 1 has no peers

        privkeys = [self.nodes[0].dumpprivkey(self.nodes[0].getnewaddress())]
        taddr = self.nodes[0].getnewaddress()

        tx = self.nodes[0].listunspent()[0]
        txid = tx['txid']
        scriptpubkey = tx['scriptPubKey']

        create_inputs = [{'txid': txid, 'vout': 0}]
        sign_inputs = [{'txid': txid, 'vout': 0, 'scriptPubKey': scriptpubkey}]

        create_hex = self.nodes[0].createrawtransaction(create_inputs, {taddr: 9.9999})
        print "create:"
        print create_hex

        signed_tx = offline_node.signrawtransaction(create_hex, sign_inputs, privkeys)
        print "sign:"
        print signed_tx

        signed_hex = signed_tx['hex']
        print "decoded:"
        print self.nodes[0].decoderawtransaction(signed_hex)
        print "sent:"
        print self.nodes[0].sendrawtransaction(signed_hex)

if __name__ == '__main__':
    SignOfflineTest().main()