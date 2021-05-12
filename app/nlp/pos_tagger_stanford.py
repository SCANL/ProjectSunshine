import os

import wexpect

from app.common import util
from app.common.Singleton import Singleton

class POSTaggerStanford(metaclass=Singleton):

    def __init__(self):
        path_to_model = util.get_config_setting('stanford', 'path_to_model')
        path_to_jar = util.get_config_setting('stanford', 'path_to_jar')
        path_to_java = util.get_config_setting('general', 'path_to_java')
        os.environ['JAVAHOME'] = path_to_java
        # self.tagger = StanfordPOSTagger(path_to_model, path_to_jar)
        spawn_string = "java -mx1g -cp %s edu.stanford.nlp.tagger.maxent.MaxentTagger -model %s" %(path_to_jar,path_to_model)
        self.tagger = wexpect.spawn(spawn_string)
        self.tagger.expect('(For EOF, use Return, Ctrl-D on Unix; Enter, Ctrl-Z, Enter on Windows.)')

    def get_pos(self, term):
        self.tagger.sendline(term)
        self.tagger.expect(term+'_[A-Z]+')
        pos = self.tagger.after.split('_')[1]
        return pos
        # return self.tagger.tag(term)

    def terminate(self):
        self.tagger.terminate()
