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


class SDR:
    def __init__(self, input_space_size, number_of_active_bits, label):
        self.input_space_size = input_space_size
        self.number_of_active_bits= number_of_active_bits
        self.active_bits = create_randomised_sdr(self.input_space_size, self.number_of_active_bits)
        self.label = label
    def get_summary(self):
        print("----------------- SUMMARY -------------------------")
        print("|L1| Label:", self.label)
        print("|L1| Input space size of SDR:", self.input_space_size)
        print("|L2| Number of active bits in SDR:", self.number_of_active_bits)
        print("|L3| Percentage of active bits:", (self.number_of_active_bits / self.input_space_size) * 100, "%")
        print("|L3| Active bits:", self.active_bits)



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


################### ENCODER ###################################################
class Encoder:
    def __init__(self, bit_space_size = None,
                number_of_bits_used_to_encode_value = None,
                min_val = None,
                max_val = None,
                resolution = None,
                is_randomly_distributed = None,
                clip_values_outside_range = None,
                is_periodic = None):

        self.bit_space_size = bit_space_size
        self.number_of_bits_used_to_encode_value = number_of_bits_used_to_encode_value
        self.clip_values_outside_range = clip_values_outside_range
        self.is_periodic = is_periodic
        self.is_randomly_distributed = is_randomly_distributed

        self.resolution = resolution
        self.uniqueness = 1
        self.permittedSimiliarityBetweenEncodings = .90 
        self.similiarityIsPercentage = True
        self.min_value_to_encode = min_val
        self.max_value_to_encode = max_val
        self.max_bit_space_value = bit_space_size
        self.min_bit_space_value = 0
        self.buckets = []
        self.encoded_values_bit_locations = []
        self.offset_for_array_indice = 1
        self.encodedValues = {}
        
        self.bucket_capacity = self.computeBucketCapacity()
        
        if self.is_randomly_distributed:
            self.initial_encoding = np.array(hc.create_randomised_sdr(self.bit_space_size, self.number_of_bits_used_to_encode_value))

            self.encoded_values_and_bit_locations = {str(self.min_value_to_encode):self.initial_encoding}
            self.buckets.append(self.min_value_to_encode)
            self.encoded_values_bit_locations.append(np.array(self.initial_encoding))
        
    def get_summary(self):
        print("----------------- SUMMARY -------------------------")
        print("|L3| Bit Space Size: ", self.bit_space_size)
        print("|L4| Number of bits to be used when encoding each value:", self.number_of_bits_used_to_encode_value)
        
        print("|L5| Range of values that can be encoded: From ", self.min_value_to_encode, ' to ', self.max_value_to_encode)
        if self.is_periodic:
            print("|L6| Number of buckets available in bit space: Unlimited (is periodic)")
        else:
            print("|L6| Number of buckets available in bit space:", float(self.bucket_capacity))
        print("|L1| Encode periodically: ", self.is_periodic)
        print("|L1| Values are encoded as are randomly distributed arrays: ", self.is_randomly_distributed)
        print("|L1| Resolution: ", self.resolution)
        print("|L1| Similiarity between encodings: ", self.uniqueness)
        print("|L2| Values outside range will to be clipped: ",self.clip_values_outside_range)
        print("|L7| Encoded values bit locations:\n ", self.encoded_values_bit_locations)
        #print("|L8| Number of buckets created so far:", len(set(self.buckets)))
        print("----------------------------------------------------")

        
    def computeBucketCapacity(self):
        """The purpose of this function is compute bucket capacity. Bucket capacity"""
        if self.is_randomly_distributed:
            return(np.floor(sp.binomial(self.bit_space_size, self.number_of_bits_used_to_encode_value) / self.resolution))
        else:
            return(np.floor((self.bit_space_size - self.number_of_bits_used_to_encode_value + 1)/ self.resolution))

    def makeRandomMove(self):
        
        newBitLocationsMayHaveClashWithExistingBitLocations = True
        
        while(newBitLocationsMayHaveClashWithExistingBitLocations):
            random_bit_index_to_move = np.random.randint(0, self.number_of_bits_used_to_encode_value, 1)[0]
            random_direction_to_move = np.random.randint(0, 2, 1)

            next_sdr = self.encoded_values_bit_locations[-1].copy()
            value = next_sdr[random_bit_index_to_move]

            if random_direction_to_move == 1:
                value = next_sdr[random_bit_index_to_move] + 1
            else: 
                value = next_sdr[random_bit_index_to_move] - 1

            if value > self.max_bit_space_value:
                if self.is_periodic:
                    value = self.min_bit_space_value
                else:
                    value = value - 2
            elif value < self.min_bit_space_value:
                if self.is_periodic:
                    value = self.max_bit_space_value
                else:
                    value = value + 2

            next_sdr[random_bit_index_to_move] = value
            newBitLocationsMayHaveClashWithExistingBitLocations = np.any(np.all(next_sdr == self.encoded_values_bit_locations, axis=1))
            
        return(next_sdr)
    
    def createBucketsForRandomlyEncodedValues(self, iterations_needed):
        for i in range(0, iterations_needed):
            next_sdr = self.makeRandomMove()
            self.encoded_values_bit_locations.append(next_sdr.copy())
            self.buckets.append(np.array(self.buckets[-1] + 1))
            self.encoded_values_and_bit_locations[str(self.buckets[-1])] = next_sdr.copy()

    
    def checkWhichBucket(self, valueChoice):
        bucket = np.floor(valueChoice / self.resolution)
        return(int(bucket))
        
    def updateEncodedValuesDictionary(self):
        for i in range(len(self.buckets)):

            self.encodedValues[str(self.buckets[i])] = {"bitLocations": self.encoded_values_bit_locations[i],
                                                        "encodedValues": np.arange(start=(self.buckets[i] * self.resolution), 
                                                         stop=(self.buckets[i] * self.resolution) + self.resolution, step=1)}
                    
        print(self.encodedValues)
    
    def encode_value_in_bit_space(self, value_choice):

        bucket = self.checkWhichBucket(value_choice)
        
        value_choice = bucket
        
        print("\nEncoding the value ->", value_choice)
        
        if (value_choice < self.min_value_to_encode or value_choice > self.max_value_to_encode): 
            if self.clip_values_outside_range:
                valuePriorToClipping = value_choice
                if value_choice < self.min_value_to_encode:
                    value_choice = self.min_value_to_encode
                else:
                    value_choice = self.max_value_to_encode
                print("The value of: ", valuePriorToClipping, "has been clipped to ->", value_choice)
            else:
                print("Not a valid choice (clipValuesOutsideRange has been set to False)")
                return


        if self.is_randomly_distributed:
            if (value_choice < self.buckets[-1]):
                print("There is a bucket already created for the value", value_choice, "-> ", 
                      self.encoded_values_and_bit_locations[str(value_choice)])
                return
            
            buckets_needed_to_encode_value = value_choice - self.buckets[-1]
            print("Current number of encoded values: " , len(self.buckets))
  
            print("Value encoded in first bucket: ", self.min_value_to_encode)
            print("Number of additional buckets required to accomodate the value choice of", value_choice, ": ", buckets_needed_to_encode_value)
            self.createBucketsForRandomlyEncodedValues(buckets_needed_to_encode_value)
        
        else:
            window = [value_choice, value_choice + self.number_of_bits_used_to_encode_value]

            if self.is_periodic:

                inputValues = np.arange(0,self.bit_space_size)
                all_values =  []

                for eachValue in range(window[0], window[1]):
                    all_values.append(inputValues[eachValue % self.bit_space_size])
    
                self.encoded_values_bit_locations.append(all_values)
                self.buckets.append(value_choice)

            else:
 
                all_values = np.arange(window[0], window[1])
                self.encoded_values_bit_locations.append(all_values)
                self.buckets.append(value_choice)
   
           


    
######################## VISUALISATION FUNCTIONS ############################################

def create_axis_for_sdr(ax, x_limit, y_limit, population, label, create_label = True):
    
    if create_label:
        label_add = np.round((population / (x_limit * y_limit)) * 100, 2)
        #label = label + ' (Sparsity: {}%)'.format(label_add)
        ax.set_xlabel(label)
        
    ax.set_xticks(range(int(x_limit)))
    ax.set_yticks(range(int(y_limit)))
    [ax.xaxis.get_major_ticks()[i].tick1line.set_color("white") for i in range(int(x_limit))]
    [ax.yaxis.get_major_ticks()[i].tick1line.set_color("white") for i in range(int(y_limit))]
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.grid(color='k', linestyle='-', linewidth=.5)
    ax.tick_params(axis = "both", which = "both", bottom = False, top = False)

    
    return(ax)



def compute_multiples(n):
    result = set()
    for i in range(1, int(n ** 0.5) + 1):
        div, mod = divmod(n, i)
        if mod == 0:
            result |= {i, div}
    result_as_list = list(result)
    result_as_list.sort()
    return(result_as_list)

def compute_middle_factors(n): 
    if n < 20:
        print("The chosen SDR size is too small and does not make sense to visualize in this way")
        return
    result = compute_multiples(n)
    
    is_prime = len(result) == 2
    if is_prime:
        print("Prime number SDR sizes not supported")
        return
    if len(result) < 5:
        print("There are only" , len(result), "factors of", n, " so the dimensions grid will be unbalanced. Better to choose a different sdr_size")
    if sp.ntheory.primetest.is_square(n):
        dim_one = result[sp.floor(len(result) / 2)]
        dim_two = dim_one
    else:
        dim_one = result[sp.floor(len(result) / 2) - 1]
        dim_two = result[sp.floor(len(result) / 2)]


    return [dim_one, dim_two]



def convert_sdr_to_tuple_for_visualisation(sdr, sdr_size): 
    counting_offset = 1
    m = np.zeros(sdr_size)
    for i in sdr:
        m[i] = m[i] + 1
    
    dimensions = compute_middle_factors(sdr_size)

    if dimensions == None:
        return
    d = np.reshape(m, [int(v) for v in dimensions])
    v = np.where(d == 1)
    
    
    coords = [(v[1][i], (dimensions[1] - counting_offset) - v[0][i]) for i in range(len(v[1]))]

    
    return(coords)

def compute_color(c, min_in_range, max_in_range):
    ival = np.interp(c,[min_in_range,max_in_range],[0,1])
    rgb = colorsys.hsv_to_rgb(0, ival,  1)
    return(rgb)

def offset_coords_for_visualisation(c, offset_amount):
    coords = np.array(c)
    coords = coords + offset_amount
    return(tuple(coords))