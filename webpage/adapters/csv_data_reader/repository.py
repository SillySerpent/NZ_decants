import abc
from typing import List, Iterable

from webpage.domain_model.domain_model import Cologne

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_cologne(self, cologne: Cologne):
        """ Adds a podcast to the repository list of colognes"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_colognes(self):
        """ Returns list of colognes objects"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_colognes(self):
        """ Returns the number of colognes that exist in the repository"""
        raise NotImplementedError
