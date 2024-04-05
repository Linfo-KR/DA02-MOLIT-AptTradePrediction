from data.crawler import *
from data.query import *
from data.preprocessing import *
from analysis.eda import EDA

def main():
    inputData = preprocessing('800000')
    eda = EDA(inputData)
    # eda.boxplot()
    # eda.barplot()
    # eda.histogram()
    # eda.lineplot()
    # eda.barplot()
    eda.correlation()


if __name__ == '__main__':
    main()