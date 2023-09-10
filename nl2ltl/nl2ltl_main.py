from nl2ltl import translate
from nl2ltl.engines.gpt.core import GPTEngine
from nl2ltl.filters.simple_filters import BasicFilter
from nl2ltl.engines.utils import _top_result

engine = GPTEngine()
filter = BasicFilter()
utterance = "Give me all cases in which activity ERTriage occurs immediately after activity AdmissionNC is performed"

ltlf_formulas = translate(utterance, engine, filter)
_top_result(ltlf_formulas)