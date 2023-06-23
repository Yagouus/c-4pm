import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from nl2ltl.engines.gpt3.core import GPT3Engine
from nl2ltl import translate
from nl2ltl.engines.utils import _top_result
from nl2ltl.filters.simple_filters import BasicFilter


def run(utterance):
    engine = GPT3Engine()
    filter = BasicFilter()

    ltlf_formulas = translate(utterance, engine, filter)
    return _top_result(ltlf_formulas) if ltlf_formulas else None
