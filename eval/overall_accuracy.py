import os
import subprocess
import csv
import time
import logging
import statistics
from datetime import datetime
import json

# Disable OpenAI token caching for inference benchmarking
os.environ["OPENAI_API_CACHE"] = "false"
os.environ["OPENAI_CACHE"] = "false"

import logging
import shutil

# Suppress WARNING logs from DSPy
logging.getLogger().setLevel(logging.ERROR)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('benchmark_execution.log'),
        logging.StreamHandler()
    ]
)

def get_folder_names(directory_path):
    folder_names = []
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isdir(item_path):
            folder_names.append(item)
    return folder_names

def run_file_and_capture_output(file_path, implementation):
    """Run a file and capture its output"""
    try:
        start_time = time.time()
        
        # Determine command based on implementation
        if implementation == 'lmql':
            cmd = ['python', file_path]
        elif implementation == 'mtllm':
            cmd = ['jac', 'run', file_path]
        else:  # dspy
            # Remove __pycache__ directories before running
            folder = os.path.dirname(file_path)
            for root, dirs, files in os.walk(folder):
                for d in dirs:
                    if d == '__pycache__':
                        pycache_path = os.path.join(root, d)
                        try:
                            shutil.rmtree(pycache_path)
                        except Exception as e:
                            logging.warning(f"Failed to remove {pycache_path}: {e}")
            cmd = ['python', file_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip(),
            'execution_time': execution_time,
            'return_code': result.returncode,
            'command': ' '.join(cmd)
        }
    
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Execution timeout (300 seconds)',
            'execution_time': 300,
            'return_code': -1,
            'command': ' '.join(cmd) if 'cmd' in locals() else 'Unknown'
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'execution_time': 0,
            'return_code': -1,
            'command': 'Error before execution'
        }

def run_multiple_times(file_path, implementation, num_runs, benchmark):
    """Run a file multiple times and collect statistics"""
    results = []
    execution_times = []
    success_count = 0

    logging.info(f"Running {file_path} {num_runs} times...")
    data_file_path = os.path.join(os.path.dirname(file_path), f"tests_{benchmark}.json")
    if os.path.exists(data_file_path):
        with open(data_file_path) as data_file:
            data = json.load(data_file)["data"]

    for run_num_loop in range(1, num_runs + 1):
        run_num = run_num_loop
        logging.info(f"  Run {run_num_loop}/{num_runs}")

        if 0 == run_num_loop % 20:
            run_num_loop = 20
        else:
            run_num_loop = run_num_loop % 20
        if os.path.exists(data_file_path):
            with open("/tmp/IN.json", 'w') as input_file:
                json.dump(data[run_num_loop-1], input_file)

        result = run_file_and_capture_output(file_path, implementation)
        # Delete /tmp/IN.json after each run
        try:
            os.remove("/tmp/IN.json")
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.warning(f"Failed to delete /tmp/IN.json: {e}")
        
        # Store individual result
        result['run_number'] = run_num
        results.append(result)
        
        if result['success']:
            success_count += 1
            execution_times.append(result['execution_time'])
        
        # Small delay between runs to avoid overwhelming the system
        time.sleep(0.1)
    
    # Calculate statistics
    stats = {
        'total_runs': num_runs,
        'successful_runs': success_count,
        'success_rate': (success_count / num_runs) * 100,
        'failed_runs': num_runs - success_count
    }
    
    if execution_times:
        stats.update({
            'avg_execution_time': statistics.mean(execution_times),
            'min_execution_time': min(execution_times),
            'max_execution_time': max(execution_times),
            'median_execution_time': statistics.median(execution_times),
            'std_execution_time': statistics.stdev(execution_times) if len(execution_times) > 1 else 0
        })
    else:
        stats.update({
            'avg_execution_time': 0,
            'min_execution_time': 0,
            'max_execution_time': 0,
            'median_execution_time': 0,
            'std_execution_time': 0
        })
    
    return results, stats

def main():
    benchmarks = get_folder_names('../benchmarks')
    implementations = ['lmql', 'dspy', 'mtllm']
    num_runs = 100
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    detailed_csv = f'benchmark_detailed_results_{timestamp}.csv'
    summary_csv = f'benchmark_summary_results_{timestamp}.csv'
    
    logging.info(f"Starting benchmark execution with {num_runs} runs per file")
    logging.info(f"Detailed results: {detailed_csv}")
    logging.info(f"Summary results: {summary_csv}")
    
    # Detailed results CSV (individual runs)
    with open(detailed_csv, 'w', newline='', encoding='utf-8') as detailed_file:
        detailed_fieldnames = ['benchmark', 'implementation', 'file_path', 'run_number', 
                              'file_exists', 'success', 'execution_time', 'return_code', 
                              'command', 'stdout', 'stderr', 'timestamp']
        detailed_writer = csv.DictWriter(detailed_file, fieldnames=detailed_fieldnames)
        detailed_writer.writeheader()
        
        # Summary results CSV (aggregated statistics)
        with open(summary_csv, 'w', newline='', encoding='utf-8') as summary_file:
            summary_fieldnames = ['benchmark', 'implementation', 'file_path', 'file_exists',
                                 'total_runs', 'successful_runs', 'failed_runs', 'success_rate',
                                 'avg_execution_time', 'min_execution_time', 'max_execution_time',
                                 'median_execution_time', 'std_execution_time', 'timestamp']
            summary_writer = csv.DictWriter(summary_file, fieldnames=summary_fieldnames)
            summary_writer.writeheader()
            
            total_files = 0
            processed_files = 0
            
            for benchmark in benchmarks:
                # if benchmark not in ["expert_answer"]:
                #     continue
                for implementation in implementations:
                    total_files += 1
                    folder_path = f'../benchmarks/{benchmark}/{benchmark}_{implementation}'
                    file_path = f'{folder_path}.jac' if implementation == 'mtllm' else f'{folder_path}.py'
                    
                    logging.info(f"Processing {total_files}: {benchmark} - {implementation}")
                    
                    if not os.path.exists(file_path):
                        logging.warning(f"File not found: {file_path}")
                        
                        # Write to both CSV files for missing files
                        missing_file_row = {
                            'benchmark': benchmark,
                            'implementation': implementation,
                            'file_path': file_path,
                            'file_exists': False,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        # Detailed CSV entry for missing file
                        detailed_row = missing_file_row.copy()
                        detailed_row.update({
                            'run_number': 1,
                            'success': False,
                            'execution_time': 0,
                            'return_code': -1,
                            'command': 'N/A',
                            'stdout': '',
                            'stderr': 'File not found'
                        })
                        detailed_writer.writerow(detailed_row)
                        
                        # Summary CSV entry for missing file
                        summary_row = missing_file_row.copy()
                        summary_row.update({
                            'total_runs': 0,
                            'successful_runs': 0,
                            'failed_runs': 0,
                            'success_rate': 0,
                            'avg_execution_time': 0,
                            'min_execution_time': 0,
                            'max_execution_time': 0,
                            'median_execution_time': 0,
                            'std_execution_time': 0
                        })
                        summary_writer.writerow(summary_row)
                        continue
                    
                    processed_files += 1
                    
                    # Run the file multiple times
                    results, stats = run_multiple_times(file_path, implementation, num_runs, benchmark)
                    
                    # Write detailed results
                    for result in results:
                        detailed_writer.writerow({
                            'benchmark': benchmark,
                            'implementation': implementation,
                            'file_path': file_path,
                            'run_number': result['run_number'],
                            'file_exists': True,
                            'success': result['success'],
                            'execution_time': result['execution_time'],
                            'return_code': result['return_code'],
                            'command': result['command'],
                            'stdout': result['stdout'],
                            'stderr': result['stderr'],
                            'timestamp': datetime.now().isoformat()
                        })
                    
                    # Write summary results
                    summary_writer.writerow({
                        'benchmark': benchmark,
                        'implementation': implementation,
                        'file_path': file_path,
                        'file_exists': True,
                        'total_runs': stats['total_runs'],
                        'successful_runs': stats['successful_runs'],
                        'failed_runs': stats['failed_runs'],
                        'success_rate': stats['success_rate'],
                        'avg_execution_time': stats['avg_execution_time'],
                        'min_execution_time': stats['min_execution_time'],
                        'max_execution_time': stats['max_execution_time'],
                        'median_execution_time': stats['median_execution_time'],
                        'std_execution_time': stats['std_execution_time'],
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    logging.info(f"Completed {benchmark}-{implementation}: "
                              f"{stats['successful_runs']}/{stats['total_runs']} successful "
                              f"(Success rate: {stats['success_rate']:.1f}%)")
                    
                    if stats['successful_runs'] > 0:
                        logging.info(f"  Avg time: {stats['avg_execution_time']:.2f}s, "
                                  f"Min: {stats['min_execution_time']:.2f}s, "
                                  f"Max: {stats['max_execution_time']:.2f}s")
    
    logging.info(f"Execution complete. Processed {processed_files}/{total_files} files.")
    logging.info(f"Detailed results saved to: {detailed_csv}")
    logging.info(f"Summary statistics saved to: {summary_csv}")

if __name__ == "__main__":
    main()

