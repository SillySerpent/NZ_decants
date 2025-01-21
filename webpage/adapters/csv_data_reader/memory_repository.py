from bisect import insort_left
from typing import List, Iterable

import abc


class MemoryRepository(abc.ABC):

  def __init__(self):
      self.memory = []



