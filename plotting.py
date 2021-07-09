from random import randint, choice
from runTest import Letter
from analyze import matches

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


if __name__ == "__main__":
    print(createWordSet2(5, 'allMatches'))