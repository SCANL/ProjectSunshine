import os
import signal
import sys
import pexpect

from src.common import util
from src.common.Singleton import Singleton


class POSTaggerStanford(metaclass=Singleton):
    """
        Singleton class for interacting with the Stanford Part-of-Speech Tagger.

        This class provides methods for initializing the tagger, getting part-of-speech tags for terms,
        and terminating the tagger process.

        Attributes:
            tagger: A PopenSpawn or spawn instance for running the Stanford Part-of-Speech Tagger.
    """

    def __init__(self) -> None:
        """
            Initializes the Stanford Part-of-Speech Tagger.

            It sets up the tagger with the required Java environment variables and starts the tagger process.
        """
        path_to_model = util.get_config_setting('stanford', 'path_to_model')
        path_to_jar = util.get_config_setting('stanford', 'path_to_jar')
        path_to_java = util.get_config_setting('general', 'path_to_java')
        os.environ['JAVAHOME'] = path_to_java
        spawn_string = f"java -mx1g -cp {path_to_jar} edu.stanford.nlp.tagger.maxent.MaxentTagger -model {path_to_model}"

        if sys.platform.startswith("win"):

            """
                Ignoring the following type issue because
                it is working on Windows.
            """
            self.tagger = pexpect.popen_spawn.PopenSpawn(  # type: ignore
                spawn_string)
        else:
            self.tagger = pexpect.spawn(spawn_string)
        # Aspetta che vengano stampate le righe desiderate
        self.tagger.expect(r'Loading default properties from tagger .+')
        self.tagger.expect(r'Loading POS tagger from .+')
        self.tagger.expect(
            r'Type some text to tag, then EOF.\s+\(For EOF, use Return, Ctrl-D on Unix; Enter, Ctrl-Z, Enter on Windows.\)\s+')

    def get_pos(self, term: str) -> str:
        """
            Get the part-of-speech (POS) tag for a given term.

            Args:
                term (str): The input term for which the POS tag is to be obtained.

            Returns:
                str: The POS tag for the input term.

            Note:
                This method sends the input term to the Stanford Part-of-Speech Tagger and extracts the POS tag from the response.

            Raises:
                IndexError: If the POS tag cannot be extracted from the tagger's response.
            """

        self.tagger.sendline(term)
        self.tagger.expect(r'.+\s+.+\s+')
        try:
            pos = self.tagger.after.decode('utf-8').strip().split('_')[1]
        except IndexError:
            self.tagger.sendline(term)
            self.tagger.expect('.+')
            pos = self.tagger.after.decode('utf-8').strip().split('_')[1]
        return pos

    def terminate(self) -> None:
        """
            Terminate the Stanford Part-of-Speech Tagger process.
        """
        if sys.platform.startswith("win"):
            self.tagger.kill(sig=signal.CTRL_C_EVENT)  # type: ignore
            self.tagger.kill(sig=signal.CTRL_BREAK_EVENT)  # type: ignore
        else:
            self.tagger.kill(sig=signal.SIGINT)
            self.tagger.kill(sig=signal.SIGTERM)
