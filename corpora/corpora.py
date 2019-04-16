import xml.etree.ElementTree
import re


class AncoraCorpus:
    def __init__(self, source_mode=None):
        self._devel_source = 'corpora/training/es.devel.txt'
        self._devel_sentences = 1419
        self._train_source = 'corpora/training/es.train.txt'
        self._train_sentences = 9022
        self._test_source = 'corpora/test/es.test.txt'
        self._test_sentences = 1705

        if source_mode == 'development':
            self.sources = [self._devel_source]
            self.total_sentences = self._devel_sentences
        elif source_mode == 'train':
            self.sources = [self._train_source]
            self.total_sentences = self._train_sentences
        elif source_mode == 'test':
            self.sources = [self._test_source]
            self.total_sentences = self._test_sentences
        else:
            self.sources = [
                self._devel_source,
                self._train_source,
                self._test_source
            ]
            self.total_sentences = (
                self._devel_sentences + self._train_sentences +
                self._test_sentences)

    def _process_sentence(self, sentence):
        return " ".join(
            [token.split("\t")[1] for token in sentence])

    def __iter__(self):
        for source in self.sources:
            with open(source, "r") as f:
                sentence_tokens = []
                for line in f:
                    if not line.startswith("#begin"):
                        if line is "\n" or line.startswith("#end"):
                            yield (self._process_sentence(sentence_tokens),
                                   source)
                            sentence_tokens = []
                        else:
                            sentence_tokens.append(line)
