#!/usr/bin/env python3

from bip44 import Wallet
from bip44.utils import get_eth_addr
from mnemonic import Mnemonic

import string

###############################################################################
# Globals
###############################################################################

mnemo = Mnemonic("english")

###############################################################################
# Helper Functions
###############################################################################

def write_to_disk(addr, words):
  with open(addr, "w") as f:
    f.write(words)

def stripped(addr):
  return addr[2:]

def num_repeating_ends(addr):
    def count(addr):
      first_char = addr[0]
      for index, char in enumerate(addr):
        if char != first_char:
          return index if index > 1 else 0
    return count(stripped(addr)) + count(list(reversed(stripped(addr))))

def all_numbers(addr):
    return stripped(addr).isdigit()

def all_letters(addr):
    return all([a in string.ascii_letters for a in stripped(addr)])

###############################################################################
# Main Logic
###############################################################################

def generate_addr():
  words = mnemo.generate(strength=256)
  w = Wallet(words)
  sk, pk = w.derive_account("eth", account=0)
  addr = get_eth_addr(pk)

  #
  # If the addr has 8 or more repeating chars at the ends.
  #
  if 8 <= num_repeating_ends(addr):
    print(num_repeating_ends(addr), addr)
    write_to_disk(addr, words)

  #
  # The addr has only numbers:
  #
  if all_numbers(addr):
    print("all numbers", addr)
    write_to_disk(addr, words)

  #
  # The addr has only letters:
  #
  if all_letters(addr):
    print("all letters", addr)
    write_to_disk(addr, words)

  #
  # The addr starts with a specific string:
  #
  if stripped(addr).lower().startswith("dead"):
    if addr.lower().endswith("beef"):
      print("specific", addr)
      write_to_disk(addr, words)

if __name__ == "__main__":
  while True:
    generate_addr()
