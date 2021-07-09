 # -*- coding: utf8 -*-
from random import choice, shuffle
import os.path
import os
import h5py as h5
import numpy as np
import datetime

class Letter():

    def __init__(self, value):
        self.value = value

        sConsons = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'л', 'м', 'н', 'р', 'к', 'п', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
        deafCons = ['к', 'п', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
        alwaysHardCons = ['ж' , 'ш' , 'ц']
        alwaysSoftCons = ['й', 'ч', 'щ']
        firstMate = ['б', 'в', 'г', 'д', 'ж', 'з',]
        secondMate = ['п', 'ф', 'к', 'т', 'ш', 'с']
        gubnye = ['п', 'б', 'м']
        gubnoZybnye = ['в', 'ф']
        peredneYazichnye = ['т', 'д', 'с', 'з', 'н', 'л', 'ц', 'ч', 'ш', 'щ', 'ж', 'р']
        sredneYazichnye = ['й']
        zadneYazichnye = ['к', 'г', 'х']
        sonor = ['р', 'л', 'м', 'н', 'й']

        sVowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']
        emolliatingVowels = ['я', 'ю', 'ё', 'и', 'е']

        if value in sVowels:
            self.generalType = 'vowel'
        elif value in sConsons:
            self.generalType = 'consonant'
        else:
            raise ValueError('Wrong language!')

        if self.generalType == 'vowel':
            
            if value in emolliatingVowels:
                self.vowSoftiness = 'смягчает'
            else:
                self.vowSoftiness = 'не смягчает'
        

        if self.generalType == 'consonant':

            if value in sonor:
                self.acousticType = 'сонорная'
            else:
                self.acousticType = 'шумная'

            if value in deafCons:
                self.deafness = 'глухая'
            else:
                self.deafness = 'звонкая'

            if value in firstMate:
                self.hasPair = 'True'
                self.mate = secondMate[firstMate.index(value)]
            elif value in secondMate:
                self.hasPair = 'True'
                self.mate = firstMate[secondMate.index(value)]
            else:
                self.hasPair = 'False'
                self.mate = 'нет'

            if value in gubnye:
                self.areaOfGeneration = 'губно-губной'
            elif value in gubnoZybnye:
                self.areaOfGeneration = 'губно-зубной'
            elif value in peredneYazichnye:
                self.areaOfGeneration = 'передне-язычный'
            elif value in zadneYazichnye:
                self.areaOfGeneration = 'задне-язычный'
            elif value in sredneYazichnye:
                self.areaOfGeneration = 'средне-язычный'
            else:
                raise ValueError('Напортачил в областях образования')

            if value in alwaysHardCons:
                self.conSoftness = 'твердая'
            elif value in alwaysSoftCons:
                self.conSoftness = 'мягкая'
            else:
                self.conSoftness = 'амбивалентна'

    def getInfo(self):
        '''Returns list with all available information about Letter'''
        if self.generalType == 'consonant':
            return [self.value, self.areaOfGeneration, self.deafness, self.conSoftness, self.acousticType, self.hasPair, self.mate]
        if self.generalType == 'vowel':
            return [self.value, self.vowSoftiness]

def createConSequense():
    '''Creates random sequence of three consonants.

    Returns: three character string
    '''

    consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'л', 'м', 'н', 'р', 'к', 'п', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']

    firstLetter = choice(consonants)
    secondLetter = choice([letter for letter in consonants if letter != firstLetter])
    thirdLetter = choice([letter for letter in consonants if  letter != secondLetter])
    
    return firstLetter + secondLetter + thirdLetter

def createWordSet(howMany, type_=('random', 'vowelAndCon')):
    vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']
    consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'л', 'м', 'н', 'р', 'к', 'п', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    result = []

    if type_ == ('random', 'oneVowel'):
        for _ in range(0, howMany):
            word = createConSequense() + choice(vowels)
            if word not in result:
                result.append(word)
            else:
                howMany += 1

    if type_ == ('set', 'oneVowel'):
        vowel = choice(vowels)
        for _ in range(0, howMany):
            word = createConSequense() + vowel
            if word not in result:
                result.append(word)
            else:
                howMany += 1

    if type_ == ('random', 'vowelAndCon'):
        for _ in range(0, howMany):
            word = createConSequense() + choice(vowels) + choice(consonants)
            if word not in result:
                result.append(word)
            else:
                howMany += 1

    if type_ == ('set', 'vowelAndCon'):
        ending = choice(vowels) + choice(consonants)
        for _ in range(0, howMany):
            word = createConSequense() + ending
            if word not in result:
                result.append(word)
            else:
                howMany += 1

    return result


def createDataSet(generatedWord):
    '''Gather information about every consonant letter in a given word.

    Args:
        generatedWord: a string, which contain three back-to-back consonant letters.
    
    Return: 2D list with all available data for each consonant.
    '''
    vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']

    if any([True for vowel in vowels if generatedWord.startswith(vowel)]):
        relevant = generatedWord[1:4]
    else:
        relevant = generatedWord[0:3]

    result = []
    for item in relevant:
        result.append(Letter(item).getInfo())
    return result


def modifySet(array, type_='random'):
    vowels = ['а', 'у', 'о', 'и', 'э', 'я', 'ю', 'ё', 'е']
    
    if type_ == 'set':
        start = choice(vowels)

        for index, item in enumerate(array):
            array[index] = start + item
    
    if type_ == 'random':
        
        for index, item in enumerate(array):
            start = choice(vowels)
            array[index] = start + item
    
    return array

def fileName(randomType, endingType):
    '''Creates unique name for a test report file.'''
    date = '_'.join(str(datetime.datetime.today().strftime("%Y-%d-%m_%H-%M")).split(' '))
    name = f'{randomType}_{endingType}_{date}'
    return name

def conSequence(seqType):
    '''Creates random sequence of consonants with a certain ruleset.

    Args:
        seqType: specifes ruleset for consonants sequence. There is 4 different rulesets for this function:

            [noMatches]: creates sequence where place of articulation of every letter is different;
            [2seq]: creates sequence where is TWO back to back letters with the same place of articulation;
            [2noSeq]: creates sequence where is TWO letters (first and last) with the same place of articulation;
            [allMatches]: creates sequence where every letter has exacly the same place of articulation.
            
    Returns: three character string.
    '''
    consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'л', 'м', 'н', 'р', 'к', 'п', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
    first = Letter(choice(consonants))

    if seqType == 'noMatches':

        while True:
            second = Letter(choice(consonants))
            third = Letter(choice(consonants))
            
            if len([first.areaOfGeneration, second.areaOfGeneration, third.areaOfGeneration]) == len(set([first.areaOfGeneration, second.areaOfGeneration, third.areaOfGeneration])):
                break

    if seqType == '2seq':

        if choice([0, 1]) == 0:

            while True:
                
                second = Letter(choice(consonants))
                third = Letter(choice(consonants))

                if second.areaOfGeneration == first.areaOfGeneration and third.areaOfGeneration != second.areaOfGeneration:
                    break

        else:

            while True:

                second = Letter(choice(consonants))
                third = Letter(choice(consonants))

                if second.areaOfGeneration != first.areaOfGeneration and third.areaOfGeneration == second.areaOfGeneration:
                    break

    if seqType == '2noSeq':
        
        while True:

            second = Letter(choice(consonants))
            third = Letter(choice(consonants))

            if second.areaOfGeneration != first.areaOfGeneration and third.areaOfGeneration == first.areaOfGeneration:
                break

    if seqType == 'allMatches':
        
        while True:

            second = Letter(choice(consonants))
            third = Letter(choice(consonants))

            if second.areaOfGeneration == first.areaOfGeneration and third.areaOfGeneration == first.areaOfGeneration:
                break
        
    if len([first.value, second.value, third.value]) == len(set([first.value, second.value, third.value])):
        return first.value + second.value + third.value
    else:
        return conSequence(seqType=seqType)

def createWordSet2(number, seqType):
    '''Creates list of a certain length of random generated five character 'words'. Scheme: VCCCV.
    
    Args:
        
        number: list length;
        seqType: ruleset for a consonants sequence in the middle of a word.
        
    Returns: list of a certain length.
    '''
    vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']

    first = choice(vowels)
    second = choice([vowel for vowel in vowels if vowel != first])
    sequenceTypes = ['noMatches', 'allMatches', '2seq', '2noSeq']
    result = []

    if seqType == 'each':

        for seq in sequenceTypes:

            for _ in range(number):

                sequence = conSequence(seq)
                word = first + sequence + second

                if word not in result:
                    result.append(word)
                else:
                    number += 1

    else:

        for _ in range(number):

            sequence = conSequence(seqType)
            word = first + sequence + second

            if word not in result:
                result.append(word)
            else:
                number += 1

    return result

def runTest():

    os.system('color') #to enable colors
    os.system('cls')

    while True:
        testType = input('\nТип теста? [старый] или [новый]\n')

        if testType == 'старый' or testType == 'новый':
            break
        else:
            print('\033[31m' + 'Неверный тип!' + '\033[0m')

    while True:
        howManyCases = input('\nСколько нужно слов?\n')
        try:
            howManyCases = int(howManyCases)
            break
        except ValueError:
            print('\033[31m' + 'Нужно ввести число!' + '\033[0m', end='\n')

    if testType == 'старый':

        while True:
            mutations = input('\nНужен ли дополнительный список слов с гласной в начале слова? [да] или [нет]\n')

            if mutations == 'да' or mutations == 'нет':
                break
            else:
                print('\033[31m' + 'Введите ДА или НЕТ' + '\033[0m')
    
        while True:
            randomType = input('\nВведите тип гласных:\n\n- [random] для случайных гласных после последовательности из трех согласных\n- [set] для фиксированной гласной\n\n')

            if randomType == 'random' or randomType == 'set':
                break
            else:
                print('\033[31m' + 'Неверный тип! Введите либо random, либо set!' + '\033[0m')

        while True:
            endingType = input('\nВведите тип концовки:\n\n- [oneVowel] для последовательности из трех согласных и ОДНОЙ гласной\n- [vowelAndCon] - для последовательности из трех согласных, гласной и согласной\n\n')

            if endingType == 'oneVowel' or endingType == 'vowelAndCon':
                break
            else:
                print('\033[31m' + '\nНеверный тип! Введите либо oneVowel, либо vowelAndCon' + '\033[0m')
    
    elif testType == 'новый':
        
        while True:

            sequenceType = input('\nКакой тип последовательности согласных?\n\n[noMatches] - для последовательности, в которой область образования всех согласных - разная;\n[2seq] - для последовательности, в которой есть два согласных с одинаковой областью образования, стоящих рядом;\n[2noSeq] - для последовательности, в которой есть два согласных с одинаковой областью образования, но стоящих порознь;\n[allMatches] - для последовательности, в которой все согласные имеют одинаковую область образования;\n[each] - для каждой из последовательностей.\n')

            if sequenceType in ['noMatches', '2seq', '2noSeq', 'allMatches', 'each']:
                break
            else:
                print('\033[31m' + 'Неверный тип!' + '\033[0m')

    if testType == 'старый':

        words = createWordSet(howManyCases, type_=(randomType, endingType))
        name = fileName(randomType, endingType)
        os.system('cls') #to clear cmd
        counter = 1

    else:

        words = createWordSet2(howManyCases, sequenceType)
        name = fileName(sequenceType, 'withoutEnding')
        os.system('cls') #to clear cmd
        counter = 1

    with h5.File(f'{name}.hdf5', 'w') as f:
        for word in words:
            while True:
                dificulty = input(f'Насколько сложно было произнести \033[92m\033[1m{word}\033[0m: ')
                apropriate_input = ['легко+', 'легко', 'средне', 'сложно', 'сложно+']
                if dificulty in apropriate_input:
                    break
                if dificulty not in apropriate_input:
                    print('\033[31m' + 'Неверное описание! Возможен только один из следующих вариантов:\nлегко+, легко, средне, сложно, сложно+' + '\033[0m')
            dataSet = createDataSet(word)
            grpName = f'Group_{counter}'
            
            group = f.create_group(grpName)
            group.attrs['word'] = word
            group.attrs['difficulty'] = dificulty

            for index, array in enumerate(dataSet):
                dt = h5.special_dtype(vlen=str)
                group.create_dataset(f'dataSet_{index}', data=np.array(array, dtype=dt))
            
            counter += 1

        if testType == 'старый':

            if mutations == 'да':

                modifySet(words, 'set')
                shuffle(words)
                os.system('cls')

                for word in words:
                    while True:
                        dificulty = input(f'Насколько сложно было произнести \033[92m\033[1m{word}\033[0m: ')
                        apropriate_input = ['легко+', 'легко', 'средне', 'сложно', 'сложно+']
                        if dificulty in apropriate_input:
                            break
                        if dificulty not in apropriate_input:
                            print('\033[31m' + 'Неверное описание! Возможен только один из следующих вариантов:\nлегко+, легко, средне, сложно, сложно+' + '\033[0m')
                    dataSet = createDataSet(word)
                    grpName = f'Group_{counter}'

                    group = f.create_group(grpName)
                    group.attrs['word'] = word
                    group.attrs['difficulty'] = dificulty

                    for index, array in enumerate(dataSet):
                        dt = h5.special_dtype(vlen=str)
                        group.create_dataset(f'dataSet_{index}', data=np.array(array, dtype=dt))
                    
                    counter += 1

    os.system('cls')

if __name__ == "__main__":
    runTest()