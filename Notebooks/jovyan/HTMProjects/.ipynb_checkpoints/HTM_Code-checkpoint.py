import numpy as np
import sympy as sp
from IPython.display import HTML
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import sys


#################### SDR FUNCTIONS ########################################################
def create_randomised_sdr(sdr_size, number_of_active_bits):
    sdr = set()
    while len(sdr) < number_of_active_bits:
        sdr.add(np.random.randint(low=1, high=sdr_size))

    return(list(sdr))


def randomly_flip_percentage_of_bits(sdr, sdr_size, percentage_to_flip):
    rd.shuffle(sdr)
    count_of_bits_to_be_flipped = int(percentage_to_flip * len(sdr))
    new_sdr = sdr[count_of_bits_to_be_flipped:]  
    noise = create_randomised_sdr(sdr_size, count_of_bits_to_be_flipped)
    sdr_with_noise = noise + new_sdr
    return(sdr_with_noise)





############## METRICS FUNCTIONS ###################################################
def compute_union_and_overlap(SDR1_on_bits, SDR2_on_bits):
    union = list(set(SDR1_on_bits).union(SDR2_on_bits))
    overlap = list(set(SDR1_on_bits).intersection(SDR2_on_bits))
    
    return({"union": union, "overlap": overlap})

def compute_match(SDR1_active_bits, SDR2_active_bits, sdr_size, match_threshold):
    match = {}
    match['overlap'] = len(compute_union_and_overlap(s1, s2)['overlap'])
    match['overlap_as_percentage_of_sdr_size'] = (match['overlap'] / sdr_size) * 100
    match['is_match'] = match_threshold < (match['overlap_as_percentage_of_sdr_size'])
    
    return(match)


def compute_overlap_set_cardinality(n, w0, w1, b, provide_summary = True):
    on_bit_space = sp.binomial(w0, b)
    off_bit_space = sp.binomial(n - w0, w1 - b)
    overlap_set = on_bit_space * off_bit_space
    if provide_summary:
        print("Given a capcity of", str(w0), "bits in the on-bit space, the number of ways to arrange ", str(b), "on-bits: ", on_bit_space)
        print("Given a capacity", str(n - w0), "bits in the off-bit space, the number of ways to arrange", str(w1 - b), "off-bits: ", off_bit_space)
        print("Number of SDRs that will match w0: ", overlap_set)
    return(overlap_set)


def create_and_compare_sdrs_over_multiple_iterations(iterations, sdr_size, population):
    sdr_unions_for_comparison = []
    sdr_overlaps_for_comparison = []
    for x in range(iterations):
        SDR1 = create_randomised_sdr(sdr_size, population)
        SDR2 =create_randomised_sdr(sdr_size, population)
        sdr_comparison = compute_union_and_overlap(SDR1, SDR2)
        sdr_unions_for_comparison.append(len(sdr_comparison['union']))
        sdr_overlaps_for_comparison.append(len(sdr_comparison['overlap']))
    print("Average union: ", str(sum(sdr_unions_for_comparison) / len(sdr_unions_for_comparison)))
    print("Average overlap: ", str(sum(sdr_overlaps_for_comparison) / len(sdr_overlaps_for_comparison)))
    return({"union_comparison": sdr_unions_for_comparison, "overlap_comparison": sdr_overlaps_for_comparison})


################### SCALAR ENCODER ###################################################
class CreateScalarEncoder:
    def __init__(self, bit_space_size = None,
                number_of_bits_per_value = None,
                min_val = None,
                max_val = None):
        self.bit_space_size = bit_space_size
        self.number_of_bits_per_value = number_of_bits_per_value
        self.unique_bits_per_encoded_value = 1
        self.min_value_to_encode = min_val
        self.max_value_to_encode = max_val
        self.buckets = self.compute_bucket_capacity(self.bit_space_size, self.number_of_bits_per_value)
        self.max_bucket_starting_indice = self.buckets - 1
        self.offset = 1
        self.current_encoded_value = None
        self.bit_locations_for_current_encoded_value = 1
        self.previously_encoded_values = np.array([])
        self.bit_locations_for_previously_encoded_values = []
        self.current_and_previous_encoded_values_comparison = None
        self.is_periodic = False
        
    def get_summary(self):
        print("----------------- SUMMARY -------------------------")
        print("Bit Space Size: ", self.bit_space_size)
        print("Number of bits used to encode each value:", self.number_of_bits_per_value)
        print("Range of values to be encoded: From ", self.min_value_to_encode, ' to ', self.max_value_to_encode)
        print("Number of unique bits per encoded value: ", self.unique_bits_per_encoded_value)
        print("Number of buckets available in bit space:", self.buckets)
        print("Max bucket starting indice:", self.max_bucket_starting_indice)
        print("Current encoded value: ", self.current_encoded_value)
        print("Previously encoded values: ", self.previously_encoded_values)
        print("Bit locations for current encoded value: ", self.bit_locations_for_current_encoded_value)
        print("Bit locations for previously encoded values: ", self.bit_locations_for_previously_encoded_values)
        print("Current and previous encoded values comparison: ", self.current_and_previous_encoded_values_comparison)
        print("Encode periodically: ", self.is_periodic)
    
    def compute_bucket_capacity(self, n, w):
        return(n - w + 1)

    def compare_current_and_previously_encoded_value(self):
        self.current_and_previous_encoded_values_comparison = np.abs(self.current_encoded_value / self.bit_space_size - self.previously_encoded_values[0] / self.bit_space_size)
    
    def encode_value_in_bit_space(self, value_choice):
        
        # check if value is outside range
        if (value_choice < self.min_value_to_encode) or (value_choice > self.max_value_to_encode):
            print('Not a valid value to encode as is outside specified range')
            return()
        
        if self.current_encoded_value is not None:
            self.previously_encoded_values = np.append(self.previously_encoded_values, self.current_encoded_value)
            self.bit_locations_for_previously_encoded_values.append(self.bit_locations_for_current_encoded_value)
            self.compare_current_and_previously_encoded_value()
        self.current_encoded_value = value_choice
        
        if (value_choice > self.max_bucket_starting_indice):
            value_to_encode = self.max_bucket_starting_indice
        else:
            value_to_encode = value_choice
            
        window = [value_to_encode, value_to_encode + self.number_of_bits_per_value - self.offset]
        all_values = np.arange(window[0], window[1] + self.offset)
        self.bit_locations_for_current_encoded_value = all_values
    


    
######################## VISUALISATION FUNCTIONS ############################################

def create_axis_for_sdr(ax, x_limit, y_limit, population, label, create_label = True):
    
    if create_label:
        label_add = np.round((population / (x_limit * y_limit)) * 100, 2)
        label = label + ' (Sparsity: {}%)'.format(label_add)
        ax.set_xlabel(label)
        
    ax.set_xticks(range(int(x_limit)))
    ax.set_yticks(range(int(y_limit)))
    [ax.xaxis.get_major_ticks()[i].tick1line.set_color("white") for i in range(int(x_limit))]
    [ax.yaxis.get_major_ticks()[i].tick1line.set_color("white") for i in range(int(y_limit))]
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='k', linestyle='-', linewidth=.5)
    
    return(ax)


def convert_sdr_to_tuple_for_visualisation(sdr, sdr_size):    
    counting_offset = 1
    # create array of complete sdrs

    m = np.zeros(sdr_size)
    for i in sdr:
        m[i] = m[i] + 1
    
    # find dimensions of visualisation
    n = sp.symbols('n')
    e = sp.Eq(2**n, sdr_size)
    s = sp.solve(e, n)
    middle_index = np.floor(float(s[0] / 2))
    
    if s[0] % 2 == 0:
        dimensions = [2**middle_index, 2**middle_index]
    else:
        dimensions = [2**middle_index, 2**(middle_index + 1)]
    
    d = np.reshape(m, [int(v) for v in dimensions])
    v = np.where(d == 1)

    
    coords = [(v[1][i], (dimensions[1] - counting_offset) - v[0][i]) for i in range(len(v[1]))]
    
    return(coords)

