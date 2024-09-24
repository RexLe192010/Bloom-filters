import csv
import pandas as pd
import random
import string
import sys
from BF import BloomFilter, hash_factory
import matplotlib.pyplot as plt


def initialize():
    data  = pd.read_csv('../user-ct-test-collection-01.txt', sep='\t')
    urllist = data.ClickURL.dropna().unique()

    # Initialize variables
    N = 377871
    R_values = range(1000, 10001, 1000)
    false_positive_rates = []
    memory_usages = []
    # Initialize Bloom filter
    bloom_filter = BloomFilter(n=N, fp_rate=0.01)
    # Add URLs to Bloom filter
    for url in urllist:
        bloom_filter.insert(url)
    return urllist, N, R_values, false_positive_rates, memory_usages, bloom_filter


def sample_1000_urls(urllist):
    """
    Sample 1000 URLs from the URL list and generate 1000 false URLs.

    input:
    urllist: list, a list of URLs

    output:
    test_urls: list, a list of 1000 URLs sampled from the URL list
    false_urls: list, a list of 1000 false URLs
    """
    test_urls = random.sample(list(urllist), 1000)
    false_urls = [''.join(random.choices(string.ascii_letters + string.digits, k=10)) for _ in range(1000)]
    return test_urls, false_urls


# Function to calculate false positive rate
def calculate_false_positive_rate(bloom_filter : BloomFilter, false_urls):
    false_positives = sum(1 for url in false_urls if bloom_filter.test(url))
    return false_positives / len(false_urls)


def main():
    urllist, N, R_values, false_positive_rates, memory_usages, bloom_filter = initialize()
    test_urls, false_urls = sample_1000_urls(urllist)
    for R in R_values:
        k = int(0.7 * R / N)
        fpr = calculate_false_positive_rate(bloom_filter, false_urls)
        false_positive_rates.append(fpr)
        memory_usage = sys.getsizeof(bloom_filter)
        memory_usages.append(memory_usage)
        print(f"R: {R}, k: {k}, False Positive Rate: {fpr}, Memory Usage: {memory_usage} bytes")
    plt.plot(memory_usages, false_positive_rates, marker='o')
    plt.xlabel('Memory Usage (bytes)')
    plt.ylabel('False Positive Rate')
    plt.title('False Positive Rate vs Memory Usage')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()