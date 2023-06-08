from nl2ltl import translate
from nl2ltl.engines.rasa.core import RasaEngine
from nl2ltl.filters.simple_filters import BasicFilter
from nl2ltl.engines.utils import pretty
from nl2ltl.engines.utils import _top_result

#RasaEngine.train()

engine = RasaEngine()
filter = BasicFilter()
utterance = "Eventually send me a Slack after receiving a Gmail"

ltlf_formulas = translate(utterance, engine, filter)
_top_result(ltlf_formulas)


