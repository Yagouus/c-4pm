import asyncio
import glob
import os
import pprint as pretty_print
import typing
from pathlib import Path
from typing import Any, Dict, Optional, Text

from rasa.shared.exceptions import RasaException
from rasa.shared.utils.cli import print_success
import rasa.core.agent
import rasa.utils.common

if typing.TYPE_CHECKING:
    from rasa.core.agent import Agent


def pprint(obj: Any) -> None:
    """Prints JSONs with indent."""
    pretty_print.pprint(obj, indent=2)


def chat(
        model_path: Optional[Text] = None,
        endpoints: Optional[Text] = None,
        agent: Optional["Agent"] = None,
) -> None:
    """Chat to the bot within a Jupyter notebook.

    Args:
        model_path: Path to a combined Rasa model.
        endpoints: Path to a yaml with the action server is custom actions are defined.
        agent: Rasa Core agent (used if no Rasa model given).
    """

    from rasa.core.utils import AvailableEndpoints
    _endpoints = AvailableEndpoints.read_endpoints(endpoints)

    if model_path:
        agent = asyncio.run(
            rasa.core.agent.load_agent(model_path=model_path, endpoints=_endpoints)
        )

    if agent is None:
        raise RasaException(
            "Either the provided model path could not load the agent "
            "or no core agent was provided."
        )

    print("Your bot is ready to talk! Type your messages here or send '/stop'.")
    while True:
        message = input("Ask something to DECLAREBOT: ")
        if message == "/stop":
            break

        responses = asyncio.run(agent.handle_text(message))
        for response in responses:
            print("Bot says: ", _display_bot_response(response))


def launch_bot(model_path: Optional[Text] = None,
               endpoints: Optional[Text] = None,
               agent: Optional["Agent"] = None,
               ):
    """Chat to the bot within a Jupyter notebook.

    Args:
        model_path: Path to a combined Rasa model.
        endpoints: Path to a yaml with the action server is custom actions are defined.
        agent: Rasa Core agent (used if no Rasa model given).
    """

    from rasa.core.utils import AvailableEndpoints
    _endpoints = AvailableEndpoints.read_endpoints(endpoints)

    if model_path:
        agent = asyncio.run(
            rasa.core.agent.load_agent(model_path=model_path, endpoints=_endpoints)
        )

    if agent is None:
        raise RasaException(
            "Either the provided model path could not load the agent "
            "or no core agent was provided."
        )

    print("Your bot is ready to talk! Type your messages here or send '/stop'.")

    return agent


def talk(agent, message):

    if message == "/stop":
        return agent, "Thanks, goodbye!"

    responses = asyncio.run(agent.handle_text(message))
    for response in responses:
        _display_bot_response(response)

    return responses


def _display_bot_response(response: Dict) -> None:

    from IPython.display import Image, display

    for response_type, value in response.items():
        if response_type == "text":
            print_success(value)

        if response_type == "image":
            image = Image(url=value)
            display(image)


def get_latest_model(path: Path = Path("models")) -> Optional[str]:
    """Get the Rasa latest model."""
    model_files = glob.glob(f"{path}/*.tar.gz")

    if not model_files:
        return None

    return max(model_files, key=os.path.getctime)

