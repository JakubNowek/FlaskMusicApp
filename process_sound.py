import os

# def test_function(filename):
#     file = open(f'static/files/{filename}', 'a')
#     file.write('\ntext added in test_function\n')
#     file.close()
#     #file = os.open(f'static/files/{filename}')


def func(function, *argv):
    function(argv[0])

def low_pass(filename):
    print('low pass')
    print(filename)
    file = open(f'static/files/{filename}', 'a')
    file.write('low pass\n')
    print(filename)
    file.close()


def high_pass(filename):
    print('high pass')
    file = open(f'static/files/{filename}', 'a')
    file.write('high pass\n')
    file.close()


def cut(filename):
    print('cut')
    file = open(f'static/files/{filename}', 'a')
    file.write('cut\n')
    file.close()
