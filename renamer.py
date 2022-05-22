import os
from pathlib import Path
RESOURCE_PATH = Path(os.path.dirname(__file__)).joinpath("res")
def rename():
    for dir in os.listdir(RESOURCE_PATH):
        chapter_path = RESOURCE_PATH.joinpath(str(dir.title()))
        index = 1
        print('==============================')
        print('Chapter {0}'.format(dir.title()))
        print('==============================')
        files = [int(item[:-4]) for item in os.listdir(chapter_path)]
        files.sort()
        os.chdir(chapter_path)
        for item in files:
            renamedFileName = str(item) + '.png'
            indexFileName = '{0}.png'.format(str(index))

            if (renamedFileName != indexFileName):
                print('Renaming {0} to {1}'.format(renamedFileName, indexFileName))
                os.rename(renamedFileName, indexFileName)
            index += 1
        os.chdir('..')

if __name__ == '__main__':
    rename()