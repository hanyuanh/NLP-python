#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation
import string

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)


consonants = ["B", "CH", "D", "DH", "F", "G", "HH", "JH", "K", "L", "M", "N", "NG", "P", "R", "S", "SH", "T", "TH", "V",
              "W", "Z", "ZH"]

class LimerickDetector:
    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()

    def count_syllables(self):
        return 1
    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        # TODO: provide an implementation!
        if word not in self._pronunciations:
            return 1
        prons = self._pronunciations[word]
        count = 0
        result = 99999
        for pron in prons:
            count_consonant = 0
            for ph in pron:
                if ph in consonants:
                    count_consonant += 1
            count_vowel = len(pron) - count_consonant
            if result > count_vowel:
                result = count_vowel
        return result

    def normalize(self, pron):
        count = 0
        for elem in pron:
            if elem in consonants:
                count += 1
            else:
                return pron[count:]
    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        # TODO: provide an implementation!
        '''
        fetch prons(a)
        fetch prons(b)
        for prona in prons
            
        '''
        prondict = nltk.corpus.cmudict.dict()
        prons_a = []
        prons_b = []
        if a in prondict:
            prons_a = prondict[a]
        if b in prondict:
            prons_b = prondict[b]
        for pron_a in prons_a:
            for pron_b in prons_b:
                norm_pron_a = self.normalize(pron_a)
                norm_pron_b = self.normalize(pron_b)
                if len(norm_pron_a) > len(norm_pron_b):
                    # shorter one should be a suffix of the longer one
                    if norm_pron_a[-len(norm_pron_b):] == norm_pron_b:
                        return True
                    else:
                        continue
                elif len(norm_pron_b) > len(norm_pron_a):
                    # shorter one should be a suffix of the longer one
                    if norm_pron_b[-len(norm_pron_a):] == norm_pron_a:
                        return True
                    else:
                        continue
                else:
                    if norm_pron_a == norm_pron_b:
                        return True
                    else:
                        continue

        return False

    def is_fulfilled(self, list):
        if abs(list[0] - list[1]) <= 2 and abs(list[1] - list[4])<=2 and abs(list[0] - list[4])<=2 and \
        abs(list[2] - list[3]) <= 2 and \
        max([list[2], list[3]]) < min([list[0], list[1], list[4]]):
            for elem in list:
                if elem < 4:
                    return False
            return True
        return False
    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!
        sentences = []
        for s in text.splitlines():
            if len(re.findall(r'[\w]+', s)) != 0:
                sentences.append(s)
        # sentences = [s.strip("\n\n") for s in text.splitlines() if s != "" and re.match(r'[ ]+', s) == None]
        sentences_tokenized = []
        sent_num_syllables = []
        sent_lastword = []
        if len(sentences) != 5:
            return False
        # tokenize each sentence
        for sent in sentences:
            list_w = word_tokenize(sent)
            sentences_tokenized.append(list_w)
        # get rid of punctuation at the end
        i = 0
        for sent in sentences_tokenized:
            temp = []
            for word in sent:
                if word not in string.punctuation:
                    temp.append(word)
            sentences_tokenized[i] = temp
            # revlist = sent[::-1]
            # while len(revlist) > 0:
            #     if revlist[0] in string.punctuation:
            #         revlist.pop(0)
            #     else:
            #         break
            # sentences_tokenized[i] = revlist[::-1]
            sent_lastword.append(sentences_tokenized[i][-1])
            i += 1
        # count syllables for each sent
        for sent in sentences_tokenized:
            count = 0
            for word in sent:
                count += self.num_syllables(word)
            sent_num_syllables.append(count)
        #1. fulfill the rhyme requirement
        if not self.rhymes(sent_lastword[0], sent_lastword[1]) and self.rhymes(sent_lastword[1], sent_lastword[4]) and self.rhymes(sent_lastword[2], sent_lastword[3]):
            return False
        #2. additive requirements
        if not self.is_fulfilled(sent_num_syllables):
            return False
        return True


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
    a = """
    a woman whose friends called a prude
    on a lark when bathing all nude
    saw a man come along
    and unless we are wrong
    you expected this line to be lewd
            """
    g = """There was a young lady one fall
Who wore a newspaper dress to a ball.
The dress caught fire
And burned her entire
Front page, sporting section and all."""
    b = """while it's true all i've done is delay
    in defense of myself i must say
    today's payoff is great
    while the workers all wait
    """
    e = """An exceedingly fat friend of mine,
    When asked at what hour he'd dine,
    Replied, "At eleven,     
    At three, five, and seven,
    And eight and a quarter past nine"""
    instance = LimerickDetector()
    # print instance.num_syllables("asdf")
    # print instance.rhymes("dog", "bog")
    print instance.is_limerick(e)
    main()
