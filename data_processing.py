from __future__ import division

import data_import_and_prep_and_display as dataimport
import math


# print "Let's get data for a column in a seven column array: "
# var = raw_input("Enter column (1-7): ")
# prepared_var = int(var)-1
# print "Header:"
# print dataimport.getColumnHeader(prepared_var)
# print "Content:"
# print dataimport.getColumnContent(prepared_var)

# Define variables
tehinguID = dataimport.getColumnContent(0)
aktsiaNimi = dataimport.getColumnContent(1)
tehinguAasta = dataimport.getColumnContent(2)
tehinguKvartal = dataimport.getColumnContent(3)
investoriGrupp = dataimport.getColumnContent(4)
investoriID = dataimport.getColumnContent(5)
tegevusAktsias = dataimport.getColumnContent(6)

# Get the LSV measure for the investor group
#       in a given quarter for the given stock
def investorGroupStockQuarterLSV(buyersQS, sellersQS, buyersQ, sellersQ):
    
    # Define variables
    activeQS = buyersQS + sellersQS
    activeQ = buyersQ + sellersQ
    activePropQ = buyersQ/activeQ

    # Calculate initial LSVI
    indicatorLSVI = abs((buyersQS/activeQS)-activePropQ)

    # Create variable to calculate binomial distribution
    divisor = 1

    while divisor < activeQS:
        divisor *= 10

    # Adjust variables to calculate binomial distribution
    adjBuyersQS = (buyersQS/divisor)
    adjActiveQS = (activeQS/divisor)
    
    # Calculate adjusted LSVI (same as previous LSVI on adj data)
    #print adjBuyersQS
    #print adjActiveQS
    #print activePropQ
    adjustedLSVI = abs((adjBuyersQS/adjActiveQS)-activePropQ)

    # If wrong value, throw error
    if round(adjustedLSVI,10) != round(indicatorLSVI,10):
        raise ValueError("LSVI on adjusted data is different from initial!")

    # Calculate binomial probability
    binomialProb = ((math.gamma(adjActiveQS+1))*activePropQ*(1-activePropQ))/((math.gamma(adjActiveQS-adjBuyersQS+1))*(math.gamma(adjBuyersQS+1)))

    # Calculate Adjustment factor
    adjFactor = binomialProb*adjustedLSVI

    # Calculate LSV 
    indicatorLSV = adjustedLSVI - adjFactor

    return indicatorLSV

# rows - stocks (here 3)
# columns - quarters (here 4)
# data content - LSV for the given stock in the given quarter, indicatorLSVqs should be a 
def createMatrix(indicatorLSVqs, noOfRows, noOfColumns):
    return [[indicatorLSVqs[columnItem] for columnItem in range(noOfColumns)] for rowItem in range(noOfRows)]

# investorGroupStockQuarterLSV(tegevusAktsias.count('1'), tegevusAktsias.count('-1'), 204, 54)
print createMatrix(5,3,4)
