from fst import FST
import string, sys
from fsmutils import composechars, trace

vowels = ['a', 'e', 'i', 'o', 'u', 'w', 'y']
grp1 = ['b', 'f', 'p', 'v']
grp2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']
grp3 = ['d', 't']
grp4 = ['l']
grp5 = ['m', 'n']
grp6 = ['r']

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Indicate that '1' is the initial state
    f1.add_state('start')
    f1.add_state('next')
    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('next')

    # Add the rest of the arcs
    for letter in string.ascii_lowercase:
        # f1.add_arc('start', 'next', (letter), (letter))
        # f1.add_arc('next', 'next', (letter), ('0'))
        f1.add_arc('start', 'next', (letter), (letter))
        if letter in vowels:
            f1.add_arc('next', 'next', (letter), ())
        elif letter in grp1:
            f1.add_arc('next', 'next', (letter), ('1'))
        elif letter in grp2:
            f1.add_arc('next', 'next', (letter), ('2'))
        elif letter in grp3:
            f1.add_arc('next', 'next', (letter), ('3'))
        elif letter in grp4:
            f1.add_arc('next', 'next', (letter), ('4'))
        elif letter in grp5:
            f1.add_arc('next', 'next', (letter), ('5'))
        elif letter in grp6:
            f1.add_arc('next', 'next', (letter), ('6'))
        else:
            continue
            #wtf
    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.initial_state = '1'
    f2.set_final('1')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('1', '1', (letter), (letter))

    for n in range(10):
        f2.add_arc('1', '1', (str(n)), (str(n)))

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('1a')
    f3.add_state('1b')
    f3.add_state('2')
    
    f3.initial_state = '1'
    f3.set_final('2')

    for letter in string.letters:
        f3.add_arc('1', '1', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('1', '1', (str(number)), (str(number)))
    
    f3.add_arc('1', '1a', (), ('0'))
    f3.add_arc('1a', '1b', (), ('0'))
    f3.add_arc('1b', '2', (), ('0'))
    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    # user_input = raw_input().strip()
    f1 = letters_to_numbers()
    # f2 = truncate_to_three_digits()
    # f3 = add_zero_padding()

    print f1.transduce(x for x in "washington")
    # if user_input:
    #     print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
