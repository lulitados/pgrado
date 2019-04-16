import shlex
import numpy as np

from sklearn.externals import joblib
from sklearn.preprocessing import CategoricalEncoder

from clauses import clauses_processor
from evaluator.evaluator import evaluate_clause


class bcolors:
    """
    Colores para destacar el output.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class PGrado:
    """
    Clase que implementa las utilidades necesarias para clasificar textos.

    Resume el proceso desarrollado durante el proyecto para la division de
    textos en clausulas y su clasificacion con respecto al sujeto del verbo
    principal.
    """
    AVAILABLE_CLASSIFIERS = [
        'LinearSVC',
        'VotingClassifier',
        'LogisticRegression',
        'RandomForestClassifier',
        'SGDClassifier',
        'SVC'
    ]
    SELECTED_CLASSIFIER = 'LinearSVC'

    def __init__(self):
        training_values_file = np.memmap(
            '../ancora_training_values.memmap',
            dtype='U50',
            mode='r')

        training_data_file = np.memmap(
            '../ancora_training_data.memmap',
            dtype='U50',
            mode='r',
            shape=(training_values_file.shape[0], 322))

        self.ENCODER = joblib.load('categorical_encoder.pkl')
        # self.ENCODER = CategoricalEncoder(handle_unknown='ignore')
        # self.ENCODER.fit(training_data_file[:, :22])
        # joblib.dump(self.ENCODER, 'categorical_encoder.pkl')

    def introduction(self):
        print(
            ("{0}Bienvenido al interactivo del Proyecto de Grado"
                ", edicion 2018. Autores: Lucia Gonzalez, Veronica Martinez{1}\n").format(
                    bcolors.HEADER, bcolors.ENDC))

    def how_to_get_help(self):
        print("Para obtener ayuda utilice el comando '{0}help{1}'.".format(
            bcolors.WARNING, bcolors.ENDC))

    def help_me(self):
        self.how_to_get_help()
        self.how_to_exit()
        print()
        self.show_available_classifiers()

    def how_to_exit(self):
        print("Para salir utilice el comando '{0}exit{1}'.".format(
            bcolors.WARNING, bcolors.ENDC))

    def show_available_classifiers(self):
        print("Clasificador actual: {}{}{}{}\n".format(
            bcolors.BOLD,
            bcolors.OKGREEN,
            self.SELECTED_CLASSIFIER,
            bcolors.ENDC))
        print(
            "Seleccione un clasificador utilizando el comando '{2}clasificador <nom_clasificador>{1}'"
            "\nClasificadores disponibles\n{0}- "
            "{3}{1}".format(
                bcolors.OKBLUE, bcolors.ENDC, bcolors.WARNING, '\n- '.join(
                    self.AVAILABLE_CLASSIFIERS)))

    def select_classifier(self, clasificador):
        if clasificador in self.AVAILABLE_CLASSIFIERS:
            self.SELECTED_CLASSIFIER = clasificador
            print("{}Clasificador {}{}'{}'{} seleccionado con exito.{}".format(
                bcolors.OKBLUE,
                bcolors.BOLD,
                bcolors.OKGREEN,
                clasificador,
                bcolors.OKBLUE,
                bcolors.ENDC))
        else:
            print("{}Clasificador desconocido{}".format(
                bcolors.FAIL, bcolors.ENDC))

    def classify_text(self, text):
        """
        Metodo principal para clasificar.

        Ejecutara los siguientes pasos:
        1. Procesar el texto para obtener las clausulas con su respectivo
           verbo principa.
        2. Evaluar cada clausula para obtener sus features.
        3. Clasificar cada clausula con el clasificador seleccionado.
        """
        classifier = joblib.load('{}.pkl'.format(self.SELECTED_CLASSIFIER))
        clauses = clauses_processor.get_clauses(text)
        clauses.reverse()
        print("{}{}Resultados ({}):{}".format(
            bcolors.HEADER, bcolors.BOLD, self.SELECTED_CLASSIFIER, bcolors.ENDC))
        for clause in clauses:
            clause_features = np.array(evaluate_clause(*clause))
            encoded_features = self.ENCODER.transform([clause_features[:22]]).toarray()

            predicted = classifier.predict([
                list(map(float, np.append(encoded_features, clause_features[22:])))
            ])
            print('{blue}Clausula: {bold}{green}{clause}{end}'.format(
                blue=bcolors.OKBLUE,
                bold=bcolors.BOLD,
                green=bcolors.OKGREEN,
                end=bcolors.ENDC,
                clause=clause[0]))
            print('{blue}Verb info: {bold}{green}{verb}{end}'.format(
                blue=bcolors.OKBLUE,
                bold=bcolors.BOLD,
                green=bcolors.OKGREEN,
                end=bcolors.ENDC,
                verb=clause[1]))
            print('{blue}Prediccion: {bold}{green}{predicted}{end}'.format(
                blue=bcolors.OKBLUE,
                bold=bcolors.BOLD,
                green=bcolors.OKGREEN,
                end=bcolors.ENDC,
                predicted=predicted))
            print()

    def interact(self):
        self.introduction()
        self.help_me()
        """
        Loop principal
        """
        while True:
            try:
                cmd, *args = shlex.split(input("{0}>{1} ".format(
                    bcolors.BOLD, bcolors.ENDC)))
            except (KeyboardInterrupt, EOFError):
                cmd = 'exit'
            except ValueError:
                continue

            if cmd == 'exit':
                print("Hasta luego!")
                break

            elif cmd == 'help':
                self.help_me()

            elif cmd == 'clasificador':
                self.select_classifier(args[0])
            elif cmd == 'clasificar':
                if self.SELECTED_CLASSIFIER == None:
                     print("{0}{2}Debe seleccionar un clasificador para comenzar a clasificar.{1}".format(
                            bcolors.FAIL, bcolors.ENDC, bcolors.BOLD))
                     self.show_available_classifiers()
                     continue
                print(("{0}Ingrese el texto a clasificar. "
                       "Para concluir escriba el caracter {2}#{1}{0} "
                       "en una nueva linea.{1}").format(
                    bcolors.BOLD, bcolors.ENDC, bcolors.OKGREEN))
                sentinel = '#' # Termina de aceptar texto al encontrar este string
                self.classify_text(' '.join(iter(input, sentinel)))
            else:
                print("{0}Comando desconocido '{2}'.{1}".format(
                    bcolors.BOLD, bcolors.ENDC, cmd))
                self.how_to_get_help()
                self.how_to_exit()


pgrado = PGrado()
pgrado.interact()
