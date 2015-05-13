__author__ = 'rodolfo'

from random import randint


# Esse programa divide o arquivo original em dois novos arquivos

def divideArquivo():
    arquivoOriginal = open("data/treino.csv", "r")
    arquivoMenor = open("arquivoTest.csv", "w")
    arquivoMaior = open("arquivoTreino.csv", "w")

    oldsession = -1
    nRandom = -1
    for line in arquivoOriginal:
        session = line.split(",")[0]
        if (oldsession == session):
            if (nRandom == 10):
                arquivoMenor.write(line)
            else:
                arquivoMaior.write(line)
        else:
            nRandom = randint(1,10)
            if (nRandom == 10):
                arquivoMenor.write(line)
            else:
                arquivoMaior.write(line)
        oldsession = session

# Main
def main():
    divideArquivo()
    pass


if __name__ == '__main__':
    main()
