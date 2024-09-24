import math
from sklearn.utils import murmurhash3_32
import bitarray
import random

# Hash functions
def hash_factory(m):
    """
    Implement a simple hash function factory. 
    Given an argument m, the desired hash table size,
    the factory should return a hash function that maps integers into a table of that length.
    (Or use murmurhash from sklearn.utils import murmurhash3_32 )

    input:
    m: int, the desired hash table size

    output:
    hash_function: a hash function that maps integers into a table of length m
    """
    def hash_function(key, seed):
        """
        input:
        key: int, the integer to be hashed
        seed: int, the seed for the hash function

        output:
        int, a hash value
        """
        return murmurhash3_32(key, seed=seed) % m
    return hash_function

# Bloom Filter
class BloomFilter:
    def __init__(self, n, fp_rate):
        """
        Implement a simple BloomFilter class.

        input:
        n: int, the number of elements to be inserted
        fp_rate: float, the desired false positive rate

        output:
        None
        """
        # Calculate the size of the bit array R using the formula: R = -N * ln(fp_rate) / (ln(2)^2)
        self.R = 1 << math.ceil(math.log2(-n * math.log(fp_rate) / (math.log(2) ** 2)))

        # N elements to be inserted
        self.N = n

        # fp_rate is the desired false positive rate
        self.fp_rate = fp_rate

        # Calculate the number of hash functions (k) using the formula: k = (m / n) * ln(2)
        self.k = math.ceil((self.R / self.N) * math.log(2))

        # create a bit array of size R
        self.table = bitarray.bitarray(self.R)
        self.table.setall(0)

        # Create k hash functions
        self.hash_functions = [hash_factory(self.R) for _ in range(self.k)]

    def insert(self, key):
        """
        Insert a key into the Bloom filter.

        input:
        key: int, the integer to be inserted

        output:
        None
        """
        for i in range(self.k):
            self.table[self.hash_functions[i](key, i)] = 1

    def test(self, key):
        """
        Test if a key is in the Bloom filter.

        input:
        key: int, the integer to be tested

        output:
        bool, whether the key is in the Bloom filter
        """
        for i in range(self.k):
            if not self.table[self.hash_functions[i](key, i)]:
                return False
        return True


def generate_membership_test_set():
    """
    Generate a set of 10,000 random integers between 10,000 and 100,000.
    Generate another set of 2000 unique integers,
    1000 of which from membership set and another 1000 not in membership set.

    input:
    None
    
    output:
    membership_set: set, a set of 10,000 random integers between 10,000 and 100,000
    """
    membership_list = random.sample(range(10000, 100000), 10000)
    
    membership_set = set(membership_list)
    
    test_set1 = set(random.sample(membership_list, 1000))

    available_set = set(range(10000, 100000)) - membership_set

    available_list = list(available_set)
    
    test_set2 = set(random.sample(available_list, 1000))
    
    test_set_all = test_set1.union(test_set2)
    
    return membership_set, test_set_all


def demonstrate_bloom_filter():
    false_positive_rates = [0.01, 0.001, 0.0001]
    membership_set, test_set = generate_membership_test_set()
    result = ""

    for fp_rate in false_positive_rates:
        bloom_filter = BloomFilter(len(membership_set), fp_rate)
            
        # Insert all items in the membership set into the Bloom filter
        for item in membership_set:
            bloom_filter.insert(item)
            
        # Test all items in the test set and compute the false positive rate
        false_positives = 0
        for item in test_set:
            if item not in membership_set and bloom_filter.test(item):
                false_positives += 1
            
        actual_fp_rate = false_positives / len(test_set)
        print(f"Desired FP rate: {fp_rate}, Actual FP rate: {actual_fp_rate}")

        result += f"Desired FP rate: {fp_rate}, Actual FP rate: {actual_fp_rate}\n"
    
    with open("Results.txt", "w") as f:
        f.write(result)

if __name__ == "__main__":
    # Run the demonstration
    demonstrate_bloom_filter()