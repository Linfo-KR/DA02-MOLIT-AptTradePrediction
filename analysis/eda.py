import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from data.preprocessing import *
from utils.utils import *

class EDA:
    def __init__(self, data):
        self.data = data
        
    def describe(self):
        summary = self.data.describe(include=['number', 'object'])
        summary.to_csv('./results/eda/summary.csv', encoding='utf-8', na_rep='NULL')
        
        return summary
    
    def _set_plot_style(self):
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (24, 18)
        plt.rcParams['font.size'] = 12
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
    
    def boxplot(self):
        create_folder('./figures/boxplot')
        self._set_plot_style()
        
        # Box Plot
        # x = addr_1 / y = price
        # 1) 서울시 전체 집값 SUMMARY
        plt.boxplot([self.data['price']], notch=True, patch_artist=True, showmeans=True, meanline=True, widths=0.6,
                    meanprops={'color':'red', 'linewidth':'1.5'}, medianprops={'color':'blue'}, boxprops={'color':'lime', 'linewidth':1.5})
        plt.ylim(0, 800000)
        plt.xlabel('Seoul')
        plt.ylabel('Price')
        plt.title('Seoul Apartment Price Summary')
        plt.tight_layout()
        plt.savefig('./figures/boxplot/box_seoul.png')
        plt.cla()
        plt.clf()
        plt.close()
        
        # 2) 각 구별 집값 SUMMARY
        regionList = self.data['district'].drop_duplicates().tolist()
        regionValueDict = {}
        for region in regionList:
            regionValueDict[region] = self.data[self.data['district'] == region]['price']
        
        fig, ax = plt.subplots()
        ax.boxplot(regionValueDict.values(), notch=True, patch_artist=True, showmeans=True, meanline=True, whis=2.5, widths=0.2,
                    meanprops={'color':'red', 'linewidth':'1.5'}, medianprops={'color':'blue'}, boxprops={'color':'lime', 'linewidth':1.5})
        ax.set_xticklabels(regionValueDict.keys(), rotation=45)
        ax.set_ylim(0, 800000)
        ax.set_xlabel('Region')
        ax.set_ylabel('Price')
        
        plt.title('Seoul Apartment Price Summary by District')
        plt.tight_layout()
        plt.savefig('./figures/boxplot/box_seoul_district.png')
        plt.cla()
        plt.clf()
        plt.close()
        
    def lineplot(self):
        create_folder('./figures/lineplot')
        self._set_plot_style()
        
        # Line Plot => 시간흐름에 따른 각 구별 집값 변동 추이
        # x = ym / y = price
        # 1) 서울시 평균 집값 변동 추이
        meanPriceTotal = self.data.groupby('ym')['price'].mean().reset_index()
        plt.plot(meanPriceTotal['ym'], meanPriceTotal['price'], linewidth=3, label='서울_전체')
        plt.xlabel('TimeSeries')
        plt.ylabel('Average Price')
        plt.title('Seoul Apartment Price Changes')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.legend()
        plt.tight_layout()
        plt.savefig('./figures/lineplot/line_seoul.png')
        plt.cla()
        plt.clf()
        plt.close()
        
        # 2) 각 구별 평균 집값 변동 추이
        regionList = self.data['district'].drop_duplicates().tolist()
        regionValueDict = {}

        for region in regionList:
            regionValueDict[region] = self.data[self.data['district'] == region][['ym', 'price']]
            meanPriceRegion = regionValueDict[region].groupby('ym')['price'].mean().reset_index()
            plt.plot(meanPriceTotal['ym'], meanPriceTotal['price'], label='서울_전체', linestyle='dotted', linewidth=2, marker='.')
            plt.plot(meanPriceRegion['ym'], meanPriceRegion['price'], label=region, linestyle='solid', linewidth=2, marker='.')
            plt.ylim(0, 300000)
            plt.xlabel('TimeSeries')
            plt.ylabel('Average Price')
            plt.title('Seoul Apartment Price Changes by District')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'./figures/lineplot/line_seoul_district({region}).png')
            plt.cla()
            plt.clf()
            plt.close()
            
    def barplot(self):
        # Bar Plot
        # input = [ym, district, con_year, area, floor, py]
        create_folder('./figures/barplot')
        self._set_plot_style()
        
        _, axes = plt.subplots(3, 2)
        # 1) 년도별 거래 건수 비교
        axes[0,0].bar(self.data['year'].value_counts().index, self.data['year'].value_counts().values, width=0.4)
        axes[0,0].set_title('Number of Trades by Month')
        axes[0,0].set_xlabel('TimeSeries')
        axes[0,0].set_ylabel('Trade')
        
        # 2) 구별 거래 건수 비교
        axes[0,1].bar(self.data['district'].value_counts().index, self.data['district'].value_counts().values, width=0.2)
        axes[0,1].set_title('Number of Trades by District')
        axes[0,1].set_xlabel('District')
        axes[0,1].set_ylabel('Trade')
    
        # 3) 건축년도별 거래 건수 비교
        constructionBins = [1960, 1970, 1980, 1990, 2000, 2010, 2020, 2023]
        constructionLabel = ['1960-1970', '1970-1980', '1980-1990', '1990-2000', '2000-2010', '2010-2020', '2020-2023']
        self.data['con_class'] = pd.cut(self.data['con_year'], bins=constructionBins, labels=constructionLabel)
        axes[1,0].bar(self.data['con_class'].value_counts().index, self.data['con_class'].value_counts().values, width=0.4)
        axes[1,0].set_title('Number of Trades by Construction Year')
        axes[1,0].set_xlabel('Construction Year')
        axes[1,0].set_ylabel('Trade')
        
        # 4) 전용면적별 거래 건수 비교
        areaBins = [0, 100, 200, 300, 400, 500]
        areaLabel = ['0-100', '100-200', '200-300', '300-400', '400-500']
        self.data['area_class'] = pd.cut(self.data['area'], bins=areaBins, labels=areaLabel)
        axes[1,1].bar(self.data['area_class'].value_counts().index, self.data['area_class'].value_counts().values, width=0.4)
        axes[1,1].set_title('Number of Trades by Area')
        axes[1,1].set_xlabel('Area')
        axes[1,1].set_ylabel('Trade')
        
        # 5) 층별 거래 건수 비교
        floorBins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 80]
        floorLabel = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40', '40~']
        self.data['floor_class'] = pd.cut(self.data['floor'], bins=floorBins, labels=floorLabel)
        axes[2,0].bar(self.data['floor_class'].value_counts().index, self.data['floor_class'].value_counts().values, width=0.4)
        axes[2,0].set_title('Number of Trades by Floor')
        axes[2,0].set_xlabel('Floor')
        axes[2,0].set_ylabel('Trade')
        
        # 6) 평당가격별 거래 건수 비교
        pyBins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 25000, 35000]
        pyLabel = ['0-1000', '1000-2000', '2000-3000', '3000-4000', '4000-5000',
                   '5000-6000', '6000-7000', '7000-8000', '8000-9000', '9000-10000',
                   '10000-15000', '15000-20000', '20000-25000', '25000~']
        self.data['py_class'] = pd.cut(self.data['py'], bins=pyBins, labels=pyLabel)
        axes[2,1].bar(self.data['py_class'].value_counts().index, self.data['py_class'].value_counts().values, width=0.2)
        axes[2,1].set_title('Number of Trades by Py')
        axes[2,1].set_xlabel('Py')
        axes[2,1].set_ylabel('Trade')

        plt.tight_layout()
        plt.savefig('./figures/barplot/bar_seoul_variables.png')
        plt.cla()
        plt.clf()
        plt.close()
        
    def histogram(self):
        # Histogram
        # input = price
        create_folder('./figures/histogram')
        self._set_plot_style()
        
        # 1) 서울시 전체 집값 분포
        plt.hist(self.data['price'], bins=100, color='limegreen', linewidth=2, alpha=0.3, edgecolor='black')
        plt.xlim(0, 500000)
        plt.xlabel('Class')
        plt.ylabel('Freq')
        plt.title('Seoul Apartment Price Distribution')
        plt.tight_layout()
        plt.savefig('./figures/histogram/histogram_seoul.png')
        plt.cla()
        plt.clf()
        plt.close()
        
        # 2) 각 구별 집값 분포
        regionList = self.data['district'].drop_duplicates().tolist()
        for region in regionList:
            regionPrice = self.data[self.data['district'] == region]['price']
            plt.hist(regionPrice, bins=100, color='limegreen', linewidth=2, alpha=0.3, edgecolor='black')
            plt.xlim(0, 500000)
            plt.xlabel('Class')
            plt.ylabel('Freq')
            plt.title('Seoul Apartment Price Distribution by District')
            plt.tight_layout()
            plt.savefig(f'./figures/histogram/histogram_seoul_district({region}).png')
            plt.cla()
            plt.clf()
            plt.close()
    
    def scatterplot(self):
        create_folder('./figures/scatterplot')
        self._set_plot_style()
        # Scatter Plot
        # x = [ym, district, con_year, area(range factor), floor(range factor)] / y = price
        
        _, axes = plt.subplots(3, 2)
        # 1) 거래시점에 따른 집값 산점도
        axes[0,0].scatter(self.data['ym'], self.data['price'])
        axes[0,0].set_title('Month and Price')
        axes[0,0].set_xlabel('TimeSeries')
        axes[0,0].set_ylabel('Price')
        
        # 2) 구에 따른 집값 산점도
        axes[0,1].scatter(self.data['district'], self.data['price'])
        axes[0,1].set_title('District and Price')
        axes[0,1].set_xlabel('District')
        axes[0,1].set_ylabel('Price')
        
        # 3) 건축년도에 따른 집값 산점도
        axes[1,0].scatter(self.data['con_year'], self.data['price'])
        axes[1,0].set_title('Construction Year and Price')
        axes[1,0].set_xlabel('Construction Year')
        axes[1,0].set_ylabel('Price')
        
        # 4) 전용면적에 따른 집값 산점도
        axes[1,1].scatter(self.data['area'], self.data['price'])
        axes[1,1].set_title('Area and Price')
        axes[1,1].set_xlabel('Area')
        axes[1,1].set_ylabel('Price')
        
        # 5) 층수에 따른 집값 산점도
        axes[2,0].scatter(self.data['floor'], self.data['price'])
        axes[2,0].set_title('Floor and Price')
        axes[2,0].set_xlabel('Floor')
        axes[2,0].set_ylabel('Price')
        
        # 6) 구에 따른 평당 집값 산점도
        axes[2,1].scatter(self.data['district'], self.data['py'])
        axes[2,1].set_title('District and Py')
        axes[2,1].set_xlabel('District')
        axes[2,1].set_ylabel('Py')

        plt.tight_layout()
        plt.savefig('./figures/scatterplot/scatter_seoul_variables.png')
        plt.cla()
        plt.clf()
        plt.close()
    
    def correlation(self):
        create_folder('./figures/corr')
        self._set_plot_style()
        # Correlataion
        # Heatmap
    
        # x = year / con_year / area / floor / py
        # y = price
        corrData = self.data[['year', 'con_year', 'area', 'floor', 'py', 'price']]
        corr = corrData.corr(method='pearson')
        corrCols = ['year', 'con_year', 'area', 'floor', 'py', 'price']
        
        sns.set_theme(font_scale=2)
        sns.heatmap(corr.values, cbar=True, annot=True, annot_kws={'size':15}, fmt='.2f', square=True, xticklabels=corrCols, yticklabels=corrCols)
        plt.tight_layout()
        plt.savefig('./figures/corr/heatmap_seoul.png')
        plt.cla()
        plt.clf()
        plt.close()
    
# Code Refactoring => Normalization + Module
# Graph Design Update
# Get Insights