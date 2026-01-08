# Gen Layer Intelligent Contract Performance Benchmark Suite

A comprehensive benchmarking tool for measuring and analyzing the performance of Intelligent Contracts on the Gen Layer testnet.

## Features

- ⚡ **Performance Metrics**: Execution time, gas usage, throughput analysis
- 📊 **Statistical Analysis**: Mean, median, percentiles (P95, P99), standard deviation
- 📈 **Visualization**: Automatic chart generation for execution times and gas usage
- 💾 **Data Export**: CSV and JSON export for further analysis
- 🔄 **Batch Testing**: Configurable iterations with warmup runs

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd genlayer-benchmark
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Before running the benchmark, update the configuration in `benchmark.py`:

```python
config = {
    'rpc_url': 'https://genlayer-testnet.rpc.caldera.xyz/http',
    'contract_address': 'YOUR_CONTRACT_ADDRESS',
    'private_key': 'YOUR_PRIVATE_KEY'
}
```

⚠️ **Security Note**: Never commit your private key to the repository. Use environment variables or a `.env` file for production.

## Usage

Run the benchmark suite:

```bash
python benchmark.py
```

### Example Usage

```python
from benchmark import IntelligentContractBenchmark

# Initialize benchmark
benchmark = IntelligentContractBenchmark(
    rpc_url='https://genlayer-testnet.rpc.caldera.xyz/http',
    contract_address='0x...',
    private_key='your_private_key'
)

# Run benchmark test
results = benchmark.run_benchmark(
    method_name='yourMethod',
    params=['param1', 'param2'],
    iterations=100,
    warmup=5
)

# Export results
benchmark.export_results()
benchmark.generate_charts()
```

## Metrics Collected

- **Execution Time**: Min, max, mean, median, standard deviation, P95, P99
- **Gas Usage**: Min, max, mean, median
- **Success Rate**: Percentage of successful executions
- **Throughput**: Transactions per second (TPS)

## Output Files

- `benchmark_results_YYYYMMDD_HHMMSS.csv` - Detailed execution data
- `benchmark_results_YYYYMMDD_HHMMSS.json` - JSON format results
- `benchmark_charts/` - Directory containing visualization charts:
  - `execution_time_distribution.png`
  - `execution_time_trend.png`
  - `gas_usage_distribution.png`

## Requirements

- Python 3.7+
- web3
- requests
- pandas
- matplotlib

## License

This project is provided as-is for research and benchmarking purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

