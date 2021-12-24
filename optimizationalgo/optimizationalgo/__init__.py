"""
``optimizationalgo``
=====================

Библиотека, реализующая оптимизационные алгоритмы для задач разного рода.
В данный момент поддерживаются алгоритмы для задачи коммовояжёра.
Для подробной информации пройдите в optimizationalgo.voyage

"""
from .voyage import simulated_annealing
from .voyage import ants_colony

__author__ = 'Mark Kozlov'

__version__ = "0.0.7"
