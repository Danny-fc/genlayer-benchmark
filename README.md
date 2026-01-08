# Gen Layer Intelligent Contract Performance Benchmark Suite

A comprehensive benchmarking tool for measuring and analyzing the performance of Intelligent Contracts on the Gen Layer testnet. This tool is fully integrated with the GenLayer Python SDK (`genlayer-py`) and provides detailed performance metrics, statistical analysis, and visualization capabilities.

## Features

- ⚡ **Performance Metrics**: Execution time, gas usage, throughput analysis
- 📊 **Statistical Analysis**: Mean, median, percentiles (P95, P99), standard deviation
- 📈 **Visualization**: Automatic chart generation for execution times and gas usage
- 💾 **Data Export**: CSV and JSON export for further analysis
- 🔄 **Batch Testing**: Configurable iterations with warmup runs
- 🔗 **GenLayer SDK Integration**: Native support for GenLayer Asimov Testnet
- 📖 **Read & Write Operations**: Support for both read-only and write contract calls

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Danny-fc/genlayer-benchmark.git
cd genlayer-benchmark
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The requirements include:
- `genlayer-py` - GenLayer Python SDK
- `web3` - Ethereum Web3 library
- `requests` - HTTP library
- `pandas` - Data analysis
- `matplotlib` - Visualization

## Configuration

Before running the benchmark, update the configuration in `benchmark.py`:

```python
config = {
    'contract_address': 'YOUR_CONTRACT_ADDRESS',  # Your deployed contract address
    'private_key': 'YOUR_PRIVATE_KEY'  # Optional, required only for write operations
}
```

**Network Configuration:**
- **Default Network**: GenLayer Asimov Testnet
- **Chain ID**: 4221
- **RPC URL**: http://34.32.169.58:9151

The benchmark suite automatically uses the GenLayer Asimov Testnet configuration. No manual RPC URL setup is required.

⚠️ **Security Note**: Never commit your private key to the repository. Use environment variables or a `.env` file for production.

## Usage

### Basic Usage

Run the benchmark suite:

```bash
python benchmark.py
```

### Programmatic Usage

```python
from benchmark import IntelligentContractBenchmark

# Initialize benchmark (read-only operations don't require private key)
benchmark = IntelligentContractBenchmark(
    contract_address='0x...',  # Your contract address
    private_key='your_private_key'  # Optional, required for write operations
)

# Run benchmark test on a contract method
results = benchmark.run_benchmark(
    method_name='yourMethod',
    params=['param1', 'param2'],  # Method parameters
    iterations=100,  # Number of test executions
    warmup=5  # Warmup runs (not counted in results)
)

# Export results
benchmark.export_results()
benchmark.generate_charts()
```

### Read vs Write Operations

The benchmark supports both read-only and write operations:

```python
# Read-only operation (no transaction, no gas)
result = benchmark.execute_contract(
    method_name='getData',
    params=[],
    is_read=True
)

# Write operation (creates transaction, requires private key)
result = benchmark.execute_contract(
    method_name='setData',
    params=['new_value'],
    is_read=False
)
```

## Metrics Collected

The benchmark suite collects comprehensive performance metrics:

### Execution Time
- **Min/Max**: Fastest and slowest execution times
- **Mean/Median**: Average and median execution times
- **Standard Deviation**: Variability in execution times
- **Percentiles**: P95 and P99 for understanding tail latencies

### Gas Usage
- **Min/Max**: Lowest and highest gas consumption
- **Mean/Median**: Average and median gas usage

### Success Metrics
- **Success Rate**: Percentage of successful executions
- **Total/Failed Executions**: Count of successful and failed runs

### Throughput
- **Transactions Per Second (TPS)**: Calculated from mean execution time

## Output Files

The benchmark generates several output files:

### Data Files
- `benchmark_results_YYYYMMDD_HHMMSS.csv` - Detailed execution data in CSV format
- `benchmark_results_YYYYMMDD_HHMMSS.json` - Same data in JSON format

### Visualization Charts
The `benchmark_charts/` directory contains:
- `execution_time_distribution.png` - Histogram of execution times
- `execution_time_trend.png` - Execution time over test duration
- `gas_usage_distribution.png` - Histogram of gas usage

## Requirements

- **Python**: 3.7 or higher
- **GenLayer SDK**: genlayer-py >= 0.9.0
- **Web3**: web3 >= 6.0.0
- **Data Processing**: pandas >= 1.5.0
- **Visualization**: matplotlib >= 3.6.0
- **HTTP**: requests >= 2.28.0

## GenLayer Network Information

This benchmark suite is configured for the **GenLayer Asimov Testnet**:

- **Network Name**: Genlayer Asimov Testnet
- **Chain ID**: 4221
- **RPC Endpoint**: http://34.32.169.58:9151
- **Block Explorer**: https://explorer-asimov.genlayer.com/
- **Native Currency**: GEN Token

## Example Workflow

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Testnet Tokens**
   - Visit the GenLayer faucet to get testnet tokens
   - Fund your account for write operations

3. **Deploy or Use Existing Contract**
   - Deploy your Intelligent Contract to GenLayer testnet
   - Note the contract address

4. **Configure Benchmark**
   - Update `contract_address` in `benchmark.py`
   - Add `private_key` if testing write operations

5. **Run Benchmarks**
   ```bash
   python benchmark.py
   ```

6. **Analyze Results**
   - Review CSV/JSON files for detailed data
   - Check charts in `benchmark_charts/` directory
   - Analyze performance metrics

## Project Structure

```
genlayer-benchmark/
├── benchmark.py          # Main benchmark suite
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## Key Features of GenLayer SDK Integration

- **Automatic Chain Configuration**: Uses GenLayer Asimov Testnet by default
- **Native Transaction Handling**: Properly handles GenLayer's consensus mechanism
- **Account Management**: Simplified account creation and management
- **Contract Interaction**: Direct contract read/write operations
- **Transaction Tracking**: Built-in transaction status monitoring

## Troubleshooting

### Common Issues

1. **"No account provided" error**
   - Solution: Add `private_key` to configuration for write operations

2. **"Contract schema not supported"**
   - This is normal for some networks. The benchmark will still work.

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

4. **Connection issues**
   - Verify you're connected to the internet
   - Check if GenLayer testnet is accessible

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for research and benchmarking purposes.

## Acknowledgments

- Built with [GenLayer Python SDK](https://pypi.org/project/genlayer-py/)
- Designed for GenLayer Asimov Testnet
- Performance testing and analysis tool for Intelligent Contracts

## Links

- **Repository**: https://github.com/Danny-fc/genlayer-benchmark
- **GenLayer Documentation**: https://docs.genlayer.com/
- **GenLayer Studio**: https://studio.genlayer.com/
