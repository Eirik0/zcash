#!/usr/bin/env python2
# Copyright (c) 2018 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal, assert_true


class ZCBenchmarksTest(BitcoinTestFramework):
    # Helper method
    def test_benchmark(self, benchmark, num_times, extra_parameter=None):
        if extra_parameter:
            print("./zcash-cli zcbenchmark {} {} {}".format(benchmark, num_times, extra_parameter))
            results = self.nodes[0].zcbenchmark(benchmark, 1, extra_parameter)
        else:
            print("./zcash-cli zcbenchmark {} {}".format(benchmark, num_times))
            results = self.nodes[0].zcbenchmark(benchmark, 1)
        assert_equal(1, len(results))
        assert_true(results[0]['runningtime'] > 0, "Benchmark %s hould have non-zero running time" % benchmark)
        print("... {}s".format(results[0]['runningtime']))

    def run_test(self):
        # Benchmarks which are called with no additional parameters
        single_threaded_benchmarks = [
            'sleep',
            'parameterloading',
            'verifyequihash',
            # TODO 'connectblockslow' fails with:
            # Unexpected exception caught during testing: [Errno 111] Connection refused
            # 'connectblockslow',
            'loadwallet',
            'listunspent',
            'createsaplingspend',
            'createsaplingoutput',
            'verifysaplingspend',
            'verifysaplingoutput'
        ]
        # Benchmarks which can optionally use a 3rd parameter for the number of threads
        multi_threaded_bencharks = [
            'createjoinsplit',
            # TODO: 'solveequihash' returns 1 result per thread so we need special logic
            # 'solveequihash'
        ]
        # Other benchmarks which can optionally use 3rd parameter
        optional_param_benchmarks = [
            ('validatelargetx', 100)  # param: Number of inputs
        ]
        # Benchmarks which require a 3rd parameter
        required_param_benchmarks = [
            # TODO get a sample JSDescription
            # ('verifyjoinsplit', ...),  # param: JSDescription passed as a string
            ('trydecryptnotes', 10),  # param: Number of addresses
            ('incnotewitnesses', 10),  # param: Number of transactions
            ('sendtoaddress', 1)  # param: Amount to send
        ]

        for benchmark in single_threaded_benchmarks + multi_threaded_bencharks:
            self.test_benchmark(benchmark, 1)

        for benchmark in multi_threaded_bencharks:
            self.test_benchmark(benchmark, 1, 2)  # 2 threads

        for (benchmark, _) in optional_param_benchmarks:
            self.test_benchmark(benchmark, 1)

        for (benchmark, parameter) in optional_param_benchmarks + required_param_benchmarks:
            self.test_benchmark(benchmark, 1, parameter)


if __name__ == '__main__':
    ZCBenchmarksTest().main()
