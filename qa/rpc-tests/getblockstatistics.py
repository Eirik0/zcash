#!/usr/bin/env python2
# Copyright (c) 2018 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, connect_nodes_bi, \
    initialize_chain_clean, start_nodes, wait_and_assert_operationid_status

from os.path import expanduser
from decimal import Decimal

class GetBlockStatisticsTest (BitcoinTestFramework):
    # Setup Methods
    def setup_chain(self):
        print "Initializing test directory " + self.options.tmpdir
        initialize_chain_clean(self.options.tmpdir, 2)

    def setup_network(self, split = False):
        self.nodes = start_nodes(2, self.options.tmpdir)
        connect_nodes_bi(self.nodes, 0, 1)
        self.is_network_split = False
        self.sync_all()

    # Helper Methods
    def generate_and_sync(self):
        self.nodes[0].generate(1)
        self.sync_all()

    # Tests
    def run_test(self):
        print "Mining blocks..."
        self.nodes[0].generate(101)

        taddr = self.nodes[1].getnewaddress()
        zaddr1 = self.nodes[1].z_getnewaddress()

        self.nodes[0].sendtoaddress(taddr, Decimal('1.0'))
        self.generate_and_sync()


        # Send 1 ZEC to a zaddr
        wait_and_assert_operationid_status(self.nodes[1], self.nodes[1].z_sendmany(taddr, [{'address': zaddr1, 'amount': 1.0, 'memo': 'c0ffee01'}], 1, 0))
        self.generate_and_sync()

        res = self.nodes[0].getblockstatistics(expanduser("~") + "/Development/zcash/zcash_stats", 0)
        print res

if __name__ == '__main__':
    GetBlockStatisticsTest().main()