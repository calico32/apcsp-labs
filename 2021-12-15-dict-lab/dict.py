import json
import os
from enum import Enum
from typing import Dict, List

import colorama  # type: ignore
from colorama import Fore, Style

colorama.init()

WORD_TYPES = {
    'n': 'head noun',
    'mod': 'modifier (adjective or adverb)',
    'sep': 'separator',
    'vt': 'verb, transitive (normally used with e)',
    'vi': 'verb, intransitive',
    'interj': 'interjection',
    'prep': 'quasi-preposition',
    'conj': 'conjunction',
    'kama': 'compound verb preceded by kama',
    'cont': 'context word used before la',
    'oth': 'special, other word',
}


class Definition:
    unofficial: bool = False
    definition: str
    word_types: List[str]

    def __init__(self, input: List[str]) -> None:
        self.word_types = []

        word_type, definition = input

        if word_type[-1] == '*':
            word_type = word_type[:-1]
            self.unofficial = True

        types = list(map(lambda x: x.strip(), word_type.split(',')))

        for type in types:
            if type not in WORD_TYPES:
                raise ValueError(f'Unknown word type: {type}')
            self.word_types.append(type)

        self.definition = definition


def add_definition(dictionary: Dict[str, List[Definition]], word: str, definitions: List[List[str]]) -> None:
    for definition in definitions:
        dictionary[word].append(Definition(definition))


def build_dict() -> Dict[str, List[Definition]]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    input: List[Dict] = json.loads(
        open(os.path.join(dir_path, 'dictionary.json'), 'r').read()
    )

    output: Dict[str, List[Definition]] = {}

    for obj in input:
        if type(obj['word']) is list:
            for spelling in obj['word']:
                output[spelling] = []
                add_definition(output, spelling, obj['meanings'])
        else:

            output[obj['word']] = []
            add_definition(output, obj['word'], obj['meanings'])

    return output


dictionary = build_dict()


def _error(message: str):
    print(Fore.RED + message + Style.RESET_ALL)


def _prompt(message: str):
    return input(Fore.GREEN + message + Style.RESET_ALL)


def print_definitions(word: str) -> None:
    if word not in dictionary:
        _error(f'No definition found for {word}')
        return

    print()

    defintion_width = max(map(lambda x: len(x.definition), dictionary[word]))

    print(f'{Fore.BLUE}{Style.BRIGHT}{word}{Style.RESET_ALL}'.center(defintion_width))
    print()

    for index, definition in enumerate(dictionary[word]):
        print(
            f'{Fore.CYAN}{index + 1}. {", ".join([WORD_TYPES[t] for t in definition.word_types])}')
        print(f'{Fore.YELLOW}{definition.definition}{Style.RESET_ALL}')
        print()


print(Fore.YELLOW + '''
Toki Pona Dictionary

Type a word to get its definition(s).
Type "list [page]" (or "l [page]") to list available words.
Type "search <query>" (or "s <query>") to search for words containing <query>.
Type "about" for more information about Toki Pona.
Type "quit" or "q" to exit.
''' + Style.RESET_ALL)

try:
    while True:
        user_input = _prompt('> ')

        if user_input.lower() == 'quit':
            break

        if user_input.strip() == '':
            continue

        if user_input.split(' ')[0] in ['list', 'l']:
            page = 1
            did_print = False
            if len(user_input.split()) > 1:
                page = int(user_input.split()[1])

            for i in range(page * 10 - 10, page * 10):
                if i >= len(dictionary):
                    break

                did_print = True

                print(
                    f'{Fore.BLUE}{i + 1:>3}: {list(dictionary.keys())[i]}{Style.RESET_ALL}')

            if not did_print:
                _error('Page does not exist.')

            continue

        if user_input.split(' ')[0] in ['search', 's']:
            query = ' '.join(user_input.split()[1:])
            found = []

            for user_input in dictionary:
                if query.lower() in user_input.lower() or len(list(filter(lambda x: query.lower() in x.definition.lower(), dictionary[user_input]))) > 0:
                    found.append(user_input)

            if len(found) == 0:
                _error('No words found.')
            elif len(found) == 1:
                print_definitions(found[0])
            else:
                print(f'Found {len(found)} words:')
                for user_input in found:
                    print(f'{Fore.BLUE}{user_input}{Style.RESET_ALL}')
                print()

            continue

        if user_input.lower() == 'about':
            print(Fore.YELLOW + "Toki Pona is a human language invented by Sonja Lang in 2001. Learn more at https://www.tokipona.org/." + Style.RESET_ALL)

        if user_input.lower() not in dictionary:
            _error(f'Word "{user_input}" not found.')
            continue

        print_definitions(user_input.lower())
except KeyboardInterrupt:
    pass
except EOFError:
    pass
