import os


# def test_function(filename):
#     file = open(f'static/files/{filename}', 'a')
#     file.write('\ntext added in test_function\n')
#     file.close()
#     #file = os.open(f'static/files/{filename}')


def low_pass(filename):
    print('low pass')
    file = open(f'static/files/{filename}', 'a')
    file.write('\nlow pass\n')
    file.close()


def high_pass(filename):
    print('high pass')
    file = open(f'static/files/{filename}', 'a')
    file.write('\nhigh pass\n')
    file.close()


def cut(filename):
    print('cut')
    file = open(f'static/files/{filename}', 'a')
    file.write('\ncut\n')
    file.close()