from nl2ltl import translate
from nl2ltl.engines.rasa.core import RasaEngine
from nl2ltl.engines.gpt3.core import GPT3Engine
from nl2ltl.filters.simple_filters import BasicFilter
from nl2ltl.engines.utils import pretty
from nl2ltl.engines.utils import _top_result

#RasaEngine.train()

engine = GPT3Engine()
filter = BasicFilter()
utterance = "Tell me in which cases IVLiquid happens"

ltlf_formulas = translate(utterance, engine, filter)
_top_result(ltlf_formulas)


