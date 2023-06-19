from abc import ABC

from logaut import ltl2dfa

from src.Declare4Py.ProcessModels.AbstractModel import ProcessModel
from pylogics.parsers import parse_ltl
from src.Declare4Py.Utils.utils import Utils
from typing import List


class LTLModel(ProcessModel, ABC):

    def __init__(self, backend: str = "lydia"):
        super().__init__()
        self.formula: str = ""
        self.parsed_formula = None
        self.parameters = []
        self.backend = backend

    def get_backend(self) -> str:
        return self.backend

    def to_lydia_backend(self) -> None:
        self.backend = "lydia"

    def to_ltlf2dfa_backend(self) -> None:
        self.backend = "ltlf2dfa"

    def add_conjunction(self, new_formula: str) -> None:
        new_formula = Utils.normalize_formula(new_formula)
        self.formula = f"({self.formula}) && ({new_formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_disjunction(self, new_formula: str) -> None:
        new_formula = Utils.normalize_formula(new_formula)
        self.formula = f"({self.formula}) || ({new_formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_implication(self, new_formula: str) -> None:
        new_formula = Utils.normalize_formula(new_formula)
        self.formula = f"({self.formula}) -> ({new_formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_equivalence(self, new_formula: str) -> None:
        new_formula = Utils.normalize_formula(new_formula)
        self.formula = f"({self.formula}) <-> ({new_formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_negation(self) -> None:
        self.formula = f"!({self.formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_next(self) -> None:
        self.formula = f"X({self.formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_eventually(self) -> None:
        self.formula = f"F({self.formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_always(self) -> None:
        self.formula = f"G({self.formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def add_until(self, new_formula: str) -> None:
        new_formula = Utils.normalize_formula(new_formula)
        self.formula = f"({self.formula}) U ({new_formula})"
        self.parsed_formula = parse_ltl(self.formula)

    def check_satisfiability(self) -> bool:
        if self.parsed_formula is None:
            raise RuntimeError("You must load the LTL model before checking the model.")
        if self.backend not in ["lydia", "ltlf2dfa"]:
            raise RuntimeError("Only lydia and ltlf2dfa are supported backends.")
        dfa = ltl2dfa(self.parsed_formula, backend=self.backend)
        dfa = dfa.minimize()
        if len(dfa.accepting_states) > 0:
            return True
        else:
            return False

    def parse_from_string(self, formula: str, new_line_ctrl: str = "\n") -> None:
        """
        This function expects an LTL formula as a string.
        The pylogics library is used, reference to it in case of doubt.
        Refer to http://ltlf2dfa.diag.uniroma1.it/ltlf_syntax
        for allowed LTL symbols.
        We allow unary operators only if followed by parenthesis, e.g.: G(a), X(a), etc..


        Args:
            formula: string containing the LTL formula to be passed
            new_line_ctrl:

        Returns:
            Void

        """
        if type(formula) is not str:
            raise RuntimeError("You must specify a string as input formula.")

        formula = Utils.normalize_formula(formula)

        try:
            self.parsed_formula = parse_ltl(formula)
        except RuntimeError:
            raise RuntimeError(f"The inserted string: \"{formula}\" is not a valid LTL formula")

        self.formula = formula


class LTLTemplate:
    """
    Class that allows the user to create a template. User can choose between various standard formulae.
    Makes use of the class LTLModel.
    Insert a string representing one of the seven available template functions
    """

    def __init__(self, template_str: str):
        self.template_str: str = template_str
        self.parameters: [str] = []
        self.ltl_templates = {'eventually_activity_a': self.eventually_activity_a,
                              'existence_two_activity_a': self.existence_two_activity_a,
                              'not_eventually_activity_a': self.not_eventually_activity_a,
                              'eventually_a_then_b': self.eventually_a_then_b,
                              'eventually_a_or_b': self.eventually_a_or_b,
                              'eventually_a_next_b': self.eventually_a_next_b,
                              'eventually_a_then_b_then_c': self.eventually_a_then_b_then_c,
                              'eventually_a_next_b_next_c': self.eventually_a_next_b_next_c,
                              'next_a': self.next_a}

        self.tb_declare_templates = {'responded_existence': self.responded_existence,
                                     'response': self.response,
                                     'alternate_response': self.alternate_response,
                                     'chain_response': self.chain_response,
                                     'precedence': self.precedence,
                                     'alternate_precedence': self.alternate_precedence,
                                     'chain_precedence': self.chain_precedence,
                                     'not_responded_existence': self.not_responded_existence,
                                     'not_response': self.not_response,
                                     'not_precedence': self.not_precedence,
                                     'not_chain_response': self.not_chain_response,
                                     'not_chain_precedence': self.not_chain_precedence}

        self.templates = {**self.ltl_templates, **self.tb_declare_templates}

        if template_str in self.templates:
            self.template_str = template_str
        else:
            raise RuntimeError(f"{template_str} is a not a valid template. Check the tutorial here "
                               f"https://declare4py.readthedocs.io/en/latest/tutorials/2.Conformance_checking_LTL.html "
                               f"for a list of the valid templates")

    def get_ltl_templates(self) -> List[str]:
        return [template for template in self.ltl_templates]

    def get_tb_declare_templates(self) -> List[str]:
        return [template for template in self.tb_declare_templates]

    @staticmethod
    def eventually_activity_a(activity: List[str]) -> str:
        formula_str = "F(" + activity[0] + ")"
        return formula_str

    # Eventually(And(self.argument, Next(Eventually(self.argument))))
    @staticmethod
    def existence_two_activity_a(activity: List[str]) -> str:
        formula_str = "F(" + activity[0] + " && F(" + activity[0] + "))"
        return formula_str

    @staticmethod
    def not_eventually_activity_a(activity: List[str]) -> str:
        formula_str = "!F(" + activity[0] + ")"
        return formula_str


    @staticmethod
    def eventually_a_then_b(activity: List[str]) -> str:
        formula_str = "F(" + activity[0] + " && F(" + activity[1] + "))"
        return formula_str

    @staticmethod
    def eventually_a_or_b(activity: List[str]) -> str:
        formula_str = "F(" + activity[0] + ") || F(" + activity[1] + ")"
        return formula_str

    @staticmethod
    def eventually_a_next_b(activity: List[str]) -> str:
        formula_str = "F(" + activity[0] + " && X(" + activity[1] + "))"
        return formula_str

    @staticmethod
    def eventually_a_then_b_then_c(activity: List[str]) -> str:
        formula_str = "F(" + activity[0] + " && F(" + activity[1] + " && F(" + activity[2] + ")))"
        return formula_str

    @staticmethod
    def eventually_a_next_b_next_c(activity: List[str]) -> str:
        formula_str = "F(" + activity[0] + " && X(" + activity[1] + " && X(" + activity[2] + ")))"
        return formula_str

    @staticmethod
    def next_a(act: [str]) -> str:
        formula_str = "X(" + act[0] + ")"
        return formula_str

    # Branched Declare Models
    @staticmethod
    def responded_existence(source: List[str], target: List[str]) -> str:
        formula = "F(" + source[0]
        for i in range(1, len(source)):
            formula += " || " + source[i]
        formula += ") -> F(" + target[0]
        for i in range(1, len(target)):
            formula += " || " + target[i]
        formula += ")"
        return formula

    @staticmethod
    def response(source: [str], target: List[str]) -> str:
        formula = "G(" + source[0]
        for i in range(1, len(source)):
            formula += " || " + source[i]
        formula += " -> F(" + target[0]
        for i in range(1, len(target)):
            formula += " || " + target[i]
        formula += "))"
        return formula

    @staticmethod
    def alternate_response(source: List[str], target: List[str]) -> str:
        formula = "G(" + source[0]
        for i in range(1, len(source)):
            formula += " || " + source[i]
        formula += " -> X((!(" + source[0] + ")"
        for i in range(1, len(source)):
            formula += " || !(" + source[i] + ")"
        formula += ")U( " + target[0]
        for i in range(1, len(target)):
            formula += " || " + target[i]
        formula += ")))"
        return formula

    @staticmethod
    def chain_response(source: List[str], target: List[str]) -> str:
        formula = "G(" + source[0]
        for i in range(1, len(source)):
            formula += "  || " + source[i]
        formula += " -> X(" + target[0]
        for i in range(1, len(target)):
            formula += " || " + target[i]
        formula += "))"
        return formula

    @staticmethod
    def precedence(source: List[str], target: List[str]) -> str:
        formula = "((!(" + target[0] + ")"
        for i in range(1, len(target)):
            formula += "|| !(" + target[i] + ")"
        formula += ")U(" + source[0]

        for i in range(1, len(source)):
            formula += "|| " + source[i]

        formula += ")) || G((!(" + target[1] + ")"
        for i in range(1, len(target)):
            formula += "||!(" + target[i] + ")"

        formula += "))"
        return formula

    @staticmethod
    def alternate_precedence(source: List[str], target: List[str]) -> str:
        formula = "("
        for i in range(1, len(target)-1):
            formula += "!(" + target[i] + ")||"
        formula += "!(" + target[len(target)-1] + ")U(" + source[0]
        for i in range(1, len(source)):
            formula += "|| " + source[i]
        formula += ")) && G(" + target[0]
        for i in range(1, len(target)):
            formula += "||" + target[i]
        formula += " -> X(("
        for i in range(1, len(target)-1):
            formula += "!(" + target[i] + ")||"
        formula += "!(" + target[len(target)-1] + ")U(" + source[0]
        for i in range(1, len(source)):
            formula += "|| " + source[i]
        formula += ")) && G( !(" + target[0] + ")"
        for i in range(1, len(target)):
            formula += "||!(" + target[i] + ")"
        formula += ")))"
        return formula

    @staticmethod
    def chain_precedence(source: List[str], target: List[str]) -> str:
        formula = "G(X(" + target[0]
        for i in range(1, len(target)):
            formula += "||" + target[i]
        formula += ") -> " + "(" + source[0]
        for i in range(1, len(source)):
            formula += "||" + source[i]
        formula += "))"
        return formula

    @staticmethod
    def not_responded_existence(source: List[str], target: List[str]) -> str:
        formula = "F(" + source[0]
        for i in range(1, len(source)):
            formula += "||" + source[i]
        formula += ") -> !(F(" + target[0] + ")"
        for i in range(1, len(target)):
            formula += "|| F(" + target[i] + ")"
        formula += ")"
        return formula

    @staticmethod
    def not_response(source: List[str], target: List[str]) -> str:
        formula = "G(" + source[0]
        for i in range(1, len(source)):
            formula += "|| " + source[i]
        formula += " -> !(F(" + target[0] + "))"
        for i in range(1, len(target)):
            formula += "||!(F(" + target[i] + "))"
        formula += ")"
        return formula

    @staticmethod
    def not_precedence(source: List[str], target: List[str]) -> str:
        formula = "G(F(" + target[0] + ")"
        for i in range(1, len(target)):
            formula += "|| F(" + target[i] + ")"
        formula += "->!(" + source[0]
        for i in range(1, len(source)):
            formula += "||" + source[i]
        formula += "))"
        return formula

    @staticmethod
    def not_chain_response(source: List[str], target: List[str]) -> str:
        formula = "G(" + source[0]
        for i in range(1, len(source)):
            formula += "|| " + source[i]
        formula += " -> X(!(" + target[0] + ")"
        for i in range(1, len(target)):
            formula += "||!(" + target[i] + ")"
        formula += "))"
        return formula

    @staticmethod
    def not_chain_precedence(source: List[str], target: List[str]) -> str:
        formula = "G( X(" + target[0]
        for i in range(1, len(target)):
            formula += " || " + target[i]
        formula += ") -> !(" + source[0] + ")"
        for i in range(1, len(source)):
            formula += " || !("+source[i]+")"
        formula += ")"
        return formula

    def fill_template(self, *activities: List[str]) -> LTLModel:
        """
        Function used to retrieve the selected template and returns an LTLModel object containing such template

        Args:
            *activities: List of parameters to pass to the selected template function

        Returns:
            Model of the template formula

        """
        if self.template_str is None:
            raise RuntimeError("Please first load a valid template")
        func = self.templates.get(self.template_str)
        filled_model = LTLModel()
        try:
            formula = func(*activities)
            for act in activities:
                act = [item.lower() for item in act]
                act = [Utils.parse_activity(item) for item in act]
                self.parameters += act
            filled_model.parse_from_string(formula)
            filled_model.parameters = self.parameters
        except (TypeError, RuntimeError):
            raise TypeError("Mismatched number of parameters or type")
        return filled_model
