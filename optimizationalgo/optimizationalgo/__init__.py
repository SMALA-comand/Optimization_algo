"""
``optimizationalgo``
=====================

Библиотека, реализующая оптимизационные алгоритмы для задач разного рода.
В данный момент поддерживаются алгоритмы для задачи коммовояжёра.
Для подробной информации по этой задаче пройдите в optimizationalgo.voyage

Доступные субпакеты
---------------------
voyage
    Алгоритмы решения задачи коммивояжёра

"""
from .voyage import simulated_annealing
from .voyage import ants_colony
from .voyage import create_visual

__author__ = 'Марк Козлов, Вячеслав Есаков, Артём Радайкин, Александр Савостьянов, Лев Памбухчян'

__version__ = "0.0.10"

__all__ = ['ants_colony', 'simulated_annealing', 'create_visual']
