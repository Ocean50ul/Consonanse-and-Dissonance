import h5py as h5
import matplotlib.pyplot as plt
import numpy as np

def matches(lst):
    '''Checks weither 3-element-list contains sequenced or non-sequenced duplicates.

    Args:
        lst: list

    Returns:
        string that describe matches in a list

          >>> matches([1, 2, 3])
          noMatches
        
          >>> matches([1, 1, 3])
          2seq

          >>> matches([1, 2, 1])
          2noSeq

          >>> matches([1, 1, 1])
          allMatches

    Raise:
        ValueError if list contains more or less than 3 elements:

          >>> matches([1, 2])
          'Invalid list length, should be exactly 3, but 2 is given'         
    '''
    if len(lst) != 3:
        raise ValueError(f'Invalid list length, should be exactly 3, but {len(lst)} is given')

    if len(set(lst)) == 1:
        return 'allMatches'

    if len(set(lst)) == len(lst):
        return 'noMatches'
    else:
        if lst[1] == lst[0] or lst[1] == lst[2]:
            return '2seq'
        else:
            return '2noSeq'

def getGenerationValues(fileName):
    '''Get place of articulation values for all words of a given test aswell as pronunciation difficulty.
    
    Args:
        filename: name of a .hdf5 file, which represents data from one test.
        
    Retruns:
        dictionary, where key is a tuple that contains word itself and pronunciation difficulty, and value is a list that
        contains place of articulation for three consonant character in order they appear in word.

          >>> getGenerationValues('foo')
          {
            ('ушжхэ', 'средне'): ['передне-язычный', 'передне-язычный', 'задне-язычный']
          }
    '''

    if not fileName.endswith('.hdf5'):
        fileName = fileName + '.hdf5'

    result = {}
    with h5.File(fileName, 'r') as f:
        for j in range(1, len(list(f.keys())) + 1):
            data = []
            for key, value in f[f'Group_{j}'].attrs.items():
                if key == 'difficulty':
                    difficulty = value
                if key == 'word':
                    word = value
            for i in range(0, 3):
                d = f[f'Group_{j}/dataSet_{i}']
                data.append(d[1])
            result[(word, difficulty)] = data
    
    return result

if __name__ == "__main__":
    easy = {}
    easy_plus = {}
    for key, value in getGenerationValues('each_withoutEnding_2020-03-11_23-23').items():
        if key[1] == 'сложно':
            easy[matches(value)] = easy.get(matches(value), 0) + 1
        if key[1] == 'сложно+':
            easy_plus[matches(value)] = easy_plus.get(matches(value), 0) + 1

    print('Statistics for hard+:')
    for key, value in easy_plus.items():
        print(key, value)
    print('====================')
    print('Statistics for hard:')
    for key, value in easy.items():
        print(key, value)
    # if matches(value) == '2noSeq':
    #     D[key[1]] = D.get(key[1], 0) + 1

    
    # desired_order_list = ['легко+', 'легко', 'средне', 'сложно']
    # reordered_dict = {k: D[k] for k in desired_order_list}

    # plt.bar(range(len(reordered_dict)), list(reordered_dict.values()), align='center')
    # plt.xticks(range(len(reordered_dict)), list(reordered_dict.keys()))
    # plt.show()
    
                