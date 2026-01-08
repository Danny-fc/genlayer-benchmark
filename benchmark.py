"""
Gen Layer Intelligent Contract Performance Benchmark Suite
Author: Research Contributor
Purpose: Measure and analyze performance of Intelligent Contracts on Gen Layer testnet
"""

import time
import json
import statistics
from datetime import datetime
from typing import List, Dict, Any
import csv

# You'll need to install these: pip install web3 requests pandas matplotlib
try:
    from web3 import Web3
    import requests
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
    print("Please install required packages:")
    print("pip install web3 requests pandas matplotlib")
    exit(1)


class IntelligentContractBenchmark:
    """
    Main benchmarking class for testing Intelligent Contract performance
    """
    
    def __init__(self, rpc_url: str, contract_address: str, private_key: str):
        """
        Initialize benchmark suite
        
        Args:
            rpc_url: Gen Layer testnet RPC endpoint
            contract_address: Address of the contract to benchmark
            private_key: Your wallet private key for signing transactions
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.contract_address = contract_address
        self.account = self.w3.eth.account.from_key(private_key)
        self.results = []
        
    def execute_contract(self, method_name: str, params: List[Any] = None) -> Dict:
        """
        Execute a single contract call and measure performance
        
        Returns:
            Dictionary with execution metrics
        """
        start_time = time.time()
        
        try:
            # Prepare transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            # Build transaction (adjust based on Gen Layer's actual interface)
            transaction = {
                'from': self.account.address,
                'to': self.contract_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'data': self._encode_method_call(method_name, params)
            }
            
            # Sign and send
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            end_time = time.time()
            
            # Calculate metrics
            execution_time = (end_time - start_time) * 1000  # Convert to ms
            gas_used = receipt['gasUsed']
            success = receipt['status'] == 1
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'method': method_name,
                'execution_time_ms': execution_time,
                'gas_used': gas_used,
                'success': success,
                'tx_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber']
            }
            
            return result
            
        except Exception as e:
            end_time = time.time()
            return {
                'timestamp': datetime.now().isoformat(),
                'method': method_name,
                'execution_time_ms': (end_time - start_time) * 1000,
                'gas_used': 0,
                'success': False,
                'error': str(e)
            }
    
    def _encode_method_call(self, method_name: str, params: List[Any]) -> bytes:
        """
        Encode method call - adjust based on Gen Layer's actual ABI
        """
        # This is a placeholder - you'll need to adjust based on actual Gen Layer interface
        # For now, we'll use a simple encoding
        call_data = json.dumps({
            'method': method_name,
            'params': params or []
        })
        return call_data.encode()
    
    def run_benchmark(self, method_name: str, params: List[Any] = None, 
                     iterations: int = 100, warmup: int = 5) -> Dict:
        """
        Run a complete benchmark test
        
        Args:
            method_name: Contract method to test
            params: Parameters to pass to the method
            iterations: Number of test executions
            warmup: Number of warmup runs (not counted in results)
        
        Returns:
            Aggregated benchmark results
        """
        print(f"\n{'='*60}")
        print(f"Starting Benchmark: {method_name}")
        print(f"Iterations: {iterations} (+ {warmup} warmup)")
        print(f"{'='*60}\n")
        
        # Warmup runs
        print(f"Running {warmup} warmup executions...")
        for i in range(warmup):
            self.execute_contract(method_name, params)
            print(f"  Warmup {i+1}/{warmup} complete")
        
        # Actual benchmark runs
        print(f"\nRunning {iterations} benchmark executions...")
        execution_results = []
        
        for i in range(iterations):
            result = self.execute_contract(method_name, params)
            execution_results.append(result)
            self.results.append(result)
            
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i+1}/{iterations} executions complete")
        
        # Calculate statistics
        successful_runs = [r for r in execution_results if r['success']]
        
        if not successful_runs:
            print("\n⚠️  WARNING: No successful executions!")
            return {'error': 'All executions failed'}
        
        execution_times = [r['execution_time_ms'] for r in successful_runs]
        gas_usage = [r['gas_used'] for r in successful_runs]
        
        stats = {
            'method': method_name,
            'total_executions': iterations,
            'successful_executions': len(successful_runs),
            'failed_executions': iterations - len(successful_runs),
            'success_rate': (len(successful_runs) / iterations) * 100,
            'execution_time': {
                'min_ms': min(execution_times),
                'max_ms': max(execution_times),
                'mean_ms': statistics.mean(execution_times),
                'median_ms': statistics.median(execution_times),
                'stdev_ms': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
                'p95_ms': self._percentile(execution_times, 95),
                'p99_ms': self._percentile(execution_times, 99)
            },
            'gas_usage': {
                'min': min(gas_usage),
                'max': max(gas_usage),
                'mean': statistics.mean(gas_usage),
                'median': statistics.median(gas_usage)
            },
            'throughput': {
                'transactions_per_second': 1000 / statistics.mean(execution_times)
            }
        }
        
        self._print_results(stats)
        return stats
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def _print_results(self, stats: Dict):
        """Pretty print benchmark results"""
        print(f"\n{'='*60}")
        print(f"BENCHMARK RESULTS: {stats['method']}")
        print(f"{'='*60}\n")
        
        print(f"Execution Summary:")
        print(f"  Total Runs:      {stats['total_executions']}")
        print(f"  Successful:      {stats['successful_executions']}")
        print(f"  Failed:          {stats['failed_executions']}")
        print(f"  Success Rate:    {stats['success_rate']:.2f}%\n")
        
        print(f"Execution Time (ms):")
        print(f"  Mean:            {stats['execution_time']['mean_ms']:.2f}")
        print(f"  Median:          {stats['execution_time']['median_ms']:.2f}")
        print(f"  Min:             {stats['execution_time']['min_ms']:.2f}")
        print(f"  Max:             {stats['execution_time']['max_ms']:.2f}")
        print(f"  Std Dev:         {stats['execution_time']['stdev_ms']:.2f}")
        print(f"  95th percentile: {stats['execution_time']['p95_ms']:.2f}")
        print(f"  99th percentile: {stats['execution_time']['p99_ms']:.2f}\n")
        
        print(f"Gas Usage:")
        print(f"  Mean:            {stats['gas_usage']['mean']:.0f}")
        print(f"  Median:          {stats['gas_usage']['median']:.0f}")
        print(f"  Min:             {stats['gas_usage']['min']}")
        print(f"  Max:             {stats['gas_usage']['max']}\n")
        
        print(f"Throughput:")
        print(f"  TPS:             {stats['throughput']['transactions_per_second']:.2f}\n")
    
    def export_results(self, filename: str = None):
        """Export results to CSV and JSON"""
        if not self.results:
            print("No results to export")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to CSV
        csv_filename = filename or f"benchmark_results_{timestamp}.csv"
        with open(csv_filename, 'w', newline='') as f:
            if self.results:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)
        print(f"✓ Results exported to CSV: {csv_filename}")
        
        # Export to JSON
        json_filename = csv_filename.replace('.csv', '.json')
        with open(json_filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"✓ Results exported to JSON: {json_filename}")
    
    def generate_charts(self, output_dir: str = "benchmark_charts"):
        """Generate visualization charts"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        if not self.results:
            print("No results to visualize")
            return
        
        df = pd.DataFrame(self.results)
        successful = df[df['success'] == True]
        
        if successful.empty:
            print("No successful executions to visualize")
            return
        
        # Execution time distribution
        plt.figure(figsize=(10, 6))
        plt.hist(successful['execution_time_ms'], bins=30, edgecolor='black')
        plt.xlabel('Execution Time (ms)')
        plt.ylabel('Frequency')
        plt.title('Execution Time Distribution')
        plt.savefig(f"{output_dir}/execution_time_distribution.png")
        print(f"✓ Chart saved: {output_dir}/execution_time_distribution.png")
        
        # Execution time over time
        plt.figure(figsize=(12, 6))
        plt.plot(successful['execution_time_ms'], marker='o', markersize=2)
        plt.xlabel('Execution Number')
        plt.ylabel('Execution Time (ms)')
        plt.title('Execution Time Over Test Duration')
        plt.savefig(f"{output_dir}/execution_time_trend.png")
        print(f"✓ Chart saved: {output_dir}/execution_time_trend.png")
        
        # Gas usage distribution
        plt.figure(figsize=(10, 6))
        plt.hist(successful['gas_used'], bins=30, edgecolor='black', color='orange')
        plt.xlabel('Gas Used')
        plt.ylabel('Frequency')
        plt.title('Gas Usage Distribution')
        plt.savefig(f"{output_dir}/gas_usage_distribution.png")
        print(f"✓ Chart saved: {output_dir}/gas_usage_distribution.png")
        
        plt.close('all')


def main():
    """
    Example usage of the benchmark suite
    """
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Gen Layer Intelligent Contract Benchmark Suite         ║
    ║   Performance Testing & Analysis Tool                     ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Configuration - UPDATE THESE WITH YOUR ACTUAL VALUES
    config = {
        'rpc_url': 'https://genlayer-testnet.rpc.caldera.xyz/http',  # Replace with actual RPC
        'contract_address': '0xed7f2512f57e4d6c314c886755b231d5f13449189aad69bcfb95225f832f43cc',  # Replace with your contract address
        'private_key': 'edskRn8esXg8GK6vamHd2MX489jsEP8Y8YUGnoQyBNQQmxECyhxJMNQysG3ktM9M4fQA8L2vb6KJ6PAbVofiVznRmA2FE3k62R'  # Replace with your private key
    }
    
    print("⚠️  CONFIGURATION REQUIRED")
    print("Please update the config dictionary with:")
    print("  - Gen Layer testnet RPC URL")
    print("  - Your deployed contract address")
    print("  - Your wallet private key")
    print("\nThis is a template - adapt it to Gen Layer's actual API\n")
    
    # Initialize benchmark
    # benchmark = IntelligentContractBenchmark(
    #     rpc_url=config['rpc_url'],
    #     contract_address=config['contract_address'],
    #     private_key=config['private_key']
    # )
    
    # Example benchmark tests
    # Test 1: Simple contract method
    # results1 = benchmark.run_benchmark(
    #     method_name='simpleCalculation',
    #     params=['input_data'],
    #     iterations=100
    # )
    
    # Test 2: Complex AI reasoning
    # results2 = benchmark.run_benchmark(
    #     method_name='complexAnalysis',
    #     params=['detailed_input'],
    #     iterations=50
    # )
    
    # Export results
    # benchmark.export_results()
    # benchmark.generate_charts()
    
    print("\n" + "="*60)
    print("NEXT STEPS TO USE THIS TOOL:")
    print("="*60)
    print("\n1. Install Gen Layer SDK/tools")
    print("2. Get testnet tokens from faucet")
    print("3. Deploy test contracts to testnet")
    print("4. Update config with your contract details")
    print("5. Run benchmarks: python benchmark.py")
    print("6. Analyze results in CSV/JSON files")
    print("7. Review generated charts in benchmark_charts/")
    print("\nThis tool measures:")
    print("  ✓ Execution times (min/max/avg/percentiles)")
    print("  ✓ Gas consumption")
    print("  ✓ Success rates")
    print("  ✓ Throughput (transactions per second)")
    print("  ✓ Performance trends over time")


if __name__ == "__main__":
    main()