#!/usr/bin/env python3
"""
Data Structures & Algorithms Implementation
SMS Transactions Search Algorithms Comparison

This module implements and compares different search algorithms:
1. Linear Search - O(n) time complexity
2. Dictionary Lookup - O(1) average time complexity
3. Binary Search - O(log n) time complexity (for sorted data)
"""

import time
import json
from typing import List, Dict, Optional, Tuple


class SearchAlgorithms:
    """Implementation of various search algorithms for SMS transactions"""
    
    def __init__(self, transactions_data: List[Dict]):
        """
        Initialize with transaction data
        
        Args:
            transactions_data: List of transaction dictionaries
        """
        self.transactions = transactions_data
        self.transactions_dict = {}
        self.sorted_transactions = []
        
        # Prepare data structures
        self._prepare_data_structures()
    
    def _prepare_data_structures(self):
        """Prepare different data structures for various search algorithms"""
        # Add IDs to transactions if not present
        for i, transaction in enumerate(self.transactions):
            if 'id' not in transaction:
                transaction['id'] = i + 1
        
        # Create dictionary for O(1) lookup
        self.transactions_dict = {t['id']: t for t in self.transactions}
        
        # Create sorted list for binary search (sorted by ID)
        self.sorted_transactions = sorted(self.transactions, key=lambda x: x['id'])
    
    def linear_search(self, transaction_id: int) -> Tuple[Optional[Dict], float]:
        """
        Linear Search Implementation - O(n) time complexity
        
        Args:
            transaction_id: ID of transaction to find
            
        Returns:
            Tuple of (transaction_dict, execution_time_seconds)
        """
        start_time = time.time()
        
        for transaction in self.transactions:
            if transaction.get('id') == transaction_id:
                end_time = time.time()
                return transaction, end_time - start_time
        
        end_time = time.time()
        return None, end_time - start_time
    
    def dictionary_lookup(self, transaction_id: int) -> Tuple[Optional[Dict], float]:
        """
        Dictionary Lookup Implementation - O(1) average time complexity
        
        Args:
            transaction_id: ID of transaction to find
            
        Returns:
            Tuple of (transaction_dict, execution_time_seconds)
        """
        start_time = time.time()
        result = self.transactions_dict.get(transaction_id)
        end_time = time.time()
        return result, end_time - start_time
    
    def binary_search(self, transaction_id: int) -> Tuple[Optional[Dict], float]:
        """
        Binary Search Implementation - O(log n) time complexity
        
        Args:
            transaction_id: ID of transaction to find
            
        Returns:
            Tuple of (transaction_dict, execution_time_seconds)
        """
        start_time = time.time()
        
        left, right = 0, len(self.sorted_transactions) - 1
        
        while left <= right:
            mid = (left + right) // 2
            mid_id = self.sorted_transactions[mid]['id']
            
            if mid_id == transaction_id:
                end_time = time.time()
                return self.sorted_transactions[mid], end_time - start_time
            elif mid_id < transaction_id:
                left = mid + 1
            else:
                right = mid - 1
        
        end_time = time.time()
        return None, end_time - start_time
    
    def compare_algorithms(self, transaction_id: int) -> Dict:
        """
        Compare all search algorithms for a given transaction ID
        
        Args:
            transaction_id: ID of transaction to search for
            
        Returns:
            Dictionary with results and performance metrics
        """
        results = {
            'transaction_id': transaction_id,
            'algorithms': {},
            'performance_analysis': {}
        }
        
        # Test Linear Search
        linear_result, linear_time = self.linear_search(transaction_id)
        results['algorithms']['linear_search'] = {
            'found': linear_result is not None,
            'execution_time': linear_time,
            'time_complexity': 'O(n)',
            'space_complexity': 'O(1)',
            'result': linear_result
        }
        
        # Test Dictionary Lookup
        dict_result, dict_time = self.dictionary_lookup(transaction_id)
        results['algorithms']['dictionary_lookup'] = {
            'found': dict_result is not None,
            'execution_time': dict_time,
            'time_complexity': 'O(1)',
            'space_complexity': 'O(n)',
            'result': dict_result
        }
        
        # Test Binary Search
        binary_result, binary_time = self.binary_search(transaction_id)
        results['algorithms']['binary_search'] = {
            'found': binary_result is not None,
            'execution_time': binary_time,
            'time_complexity': 'O(log n)',
            'space_complexity': 'O(1)',
            'result': binary_result
        }
        
        # Performance Analysis
        times = [linear_time, dict_time, binary_time]
        fastest_time = min(times)
        slowest_time = max(times)
        
        results['performance_analysis'] = {
            'fastest_algorithm': 'dictionary_lookup' if dict_time == fastest_time else 
                               'binary_search' if binary_time == fastest_time else 'linear_search',
            'slowest_algorithm': 'linear_search' if linear_time == slowest_time else 
                               'binary_search' if binary_time == slowest_time else 'dictionary_lookup',
            'speed_improvement': {
                'dictionary_vs_linear': f"{linear_time / dict_time:.2f}x faster" if dict_time > 0 else "N/A",
                'binary_vs_linear': f"{linear_time / binary_time:.2f}x faster" if binary_time > 0 else "N/A",
                'dictionary_vs_binary': f"{binary_time / dict_time:.2f}x faster" if dict_time > 0 else "N/A"
            },
            'dataset_size': len(self.transactions)
        }
        
        return results
    
    def benchmark_algorithms(self, test_ids: List[int]) -> Dict:
        """
        Benchmark all algorithms with multiple test cases
        
        Args:
            test_ids: List of transaction IDs to test
            
        Returns:
            Dictionary with comprehensive benchmark results
        """
        benchmark_results = {
            'test_cases': len(test_ids),
            'dataset_size': len(self.transactions),
            'algorithms': {
                'linear_search': {'total_time': 0, 'avg_time': 0, 'success_rate': 0},
                'dictionary_lookup': {'total_time': 0, 'avg_time': 0, 'success_rate': 0},
                'binary_search': {'total_time': 0, 'avg_time': 0, 'success_rate': 0}
            },
            'detailed_results': []
        }
        
        for test_id in test_ids:
            comparison = self.compare_algorithms(test_id)
            benchmark_results['detailed_results'].append(comparison)
            
            # Aggregate statistics
            for algo_name, algo_data in comparison['algorithms'].items():
                benchmark_results['algorithms'][algo_name]['total_time'] += algo_data['execution_time']
                if algo_data['found']:
                    benchmark_results['algorithms'][algo_name]['success_rate'] += 1
        
        # Calculate averages
        for algo_name in benchmark_results['algorithms']:
            algo_stats = benchmark_results['algorithms'][algo_name]
            algo_stats['avg_time'] = algo_stats['total_time'] / len(test_ids)
            algo_stats['success_rate'] = (algo_stats['success_rate'] / len(test_ids)) * 100
        
        return benchmark_results


def load_transactions_from_file(filename: str) -> List[Dict]:
    """
    Load transactions from JSON file
    
    Args:
        filename: Path to JSON file
        
    Returns:
        List of transaction dictionaries
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found. Using sample data.")
        return []
    except json.JSONDecodeError:
        print(f"Invalid JSON in {filename}. Using sample data.")
        return []


def create_sample_data() -> List[Dict]:
    """Create sample transaction data for testing"""
    return [
        {
            "id": 1,
            "address": "M-Money",
            "body": "You have received 2000 RWF from Jane Smith",
            "date": "1715351458724",
            "type": "1",
            "service_center": "+250788110381"
        },
        {
            "id": 2,
            "address": "M-Money", 
            "body": "Your payment of 1,000 RWF has been completed",
            "date": "1715351506754",
            "type": "1",
            "service_center": "+250788110381"
        },
        {
            "id": 3,
            "address": "Bank-Alert",
            "body": "Account balance: 50,000 RWF",
            "date": "1715369560245",
            "type": "1",
            "service_center": "+250788110381"
        }
    ]


def main():
    """Demonstrate the search algorithms"""
    print("🔍 SMS Transactions Search Algorithms Demo")
    print("=" * 50)
    
    # Load data
    transactions = load_transactions_from_file('sms_transactions.json')
    if not transactions:
        print("Using sample data for demonstration...")
        transactions = create_sample_data()
    
    # Initialize search algorithms
    searcher = SearchAlgorithms(transactions)
    
    print(f"Dataset size: {len(transactions)} transactions")
    print()
    
    # Test individual search
    test_id = 1
    print(f"🔍 Testing search for transaction ID: {test_id}")
    print("-" * 30)
    
    comparison = searcher.compare_algorithms(test_id)
    
    for algo_name, algo_data in comparison['algorithms'].items():
        status = "✅ Found" if algo_data['found'] else "❌ Not Found"
        print(f"{algo_name.replace('_', ' ').title()}:")
        print(f"  Status: {status}")
        print(f"  Time: {algo_data['execution_time']:.6f} seconds")
        print(f"  Complexity: {algo_data['time_complexity']}")
        print()
    
    # Performance analysis
    perf = comparison['performance_analysis']
    print("📊 Performance Analysis:")
    print(f"  Fastest: {perf['fastest_algorithm'].replace('_', ' ').title()}")
    print(f"  Dataset size: {perf['dataset_size']}")
    print("  Speed improvements:")
    for improvement, ratio in perf['speed_improvement'].items():
        print(f"    {improvement.replace('_', ' ').title()}: {ratio}")
    print()
    
    # Benchmark with multiple test cases
    print("🏃‍♂️ Running benchmark with multiple test cases...")
    test_ids = [1, 2, 3, 10, 50, 100] if len(transactions) >= 100 else [1, 2, 3]
    benchmark = searcher.benchmark_algorithms(test_ids)
    
    print(f"Benchmark results ({benchmark['test_cases']} test cases):")
    print("-" * 40)
    
    for algo_name, stats in benchmark['algorithms'].items():
        print(f"{algo_name.replace('_', ' ').title()}:")
        print(f"  Average time: {stats['avg_time']:.6f} seconds")
        print(f"  Success rate: {stats['success_rate']:.1f}%")
        print()
    
    # Algorithm recommendations
    print("💡 Algorithm Recommendations:")
    print("-" * 30)
    print("• Dictionary Lookup: Best for frequent individual lookups")
    print("• Binary Search: Good for sorted data with occasional lookups")
    print("• Linear Search: Simple but slow for large datasets")
    print()
    print("🎯 For this SMS API: Dictionary lookup is optimal!")


if __name__ == "__main__":
    main()
