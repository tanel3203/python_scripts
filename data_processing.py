from __future__ import division
import data_import_and_prep_and_display as dataimport
import math

# -------------- VARIABLES

# Define variables
tehinguID = dataimport.getColumnContent(0)
aktsiaNimi = dataimport.getColumnContent(1)
tehinguAasta = dataimport.getColumnContent(2)
tehinguKvartal = dataimport.getColumnContent(3)
investoriGrupp = dataimport.getColumnContent(4)
investoriID = dataimport.getColumnContent(5)
tegevusAktsias = dataimport.getColumnContent(6)

uniqueAktsiaNimi = list(set(aktsiaNimi))


# -------------- INTERFACES

def getBuysInStockQuarter(stock, year, quarter):
    return countBuysAndSalesInStockQuarter(stock, year, quarter)[0]

def getSalesInStockQuarter(stock, year, quarter):
    return countBuysAndSalesInStockQuarter(stock, year, quarter)[1]

def getBuysInQuarter(year, quarter):
    return countBuysAndSalesInStock(year, quarter)[0]

def getSalesInQuarter(year, quarter):
    return countBuysAndSalesInStock(year, quarter)[1]

def getStockQuarterLSV(stock, year, quarter):
    print "--------------------------------"
    print "Stock: ", stock
    print "Year: " , year
    print "Quarter: ", quarter
    return investorGroupStockQuarterLSV(getBuysInStockQuarter(stock, year, quarter), getSalesInStockQuarter(stock, year, quarter), getBuysInQuarter(year, quarter), getSalesInQuarter(year, quarter))

def getYearArrayFromYearQuarterArray(yearQuarterArray):
    return yearFromYearQuarterArray(yearQuarterArray)

def getQuarterArrayFromYearQuarterArray(yearQuarterArray):
    return quarterFromYearQuarterArray(yearQuarterArray)


# -------------- FUNCTIONS

# Count buys and sales for a stock in a given quarter
def countBuysAndSalesInStockQuarter(stock, year, quarter):
    currBuyersQS = 0
    currSellersQS = 0
    
    for item in range(0,len(tehinguID)):
        
        # Get all buyers and sellers in the stock in the quarter
        if ((aktsiaNimi[item] == stock) and (tehinguAasta[item] == str(year)) and (tehinguKvartal[item] == str(quarter))):

            if tegevusAktsias[item] == '-1':
                currSellersQS += 1
            elif tegevusAktsias[item] == '1':
                currBuyersQS += 1
            
    return currBuyersQS, currSellersQS

# Count all buys and sales in the given quarter
def countBuysAndSalesInStock(year, quarter):
    currBuyersQ = 0
    currSellersQ = 0
    
    for item in range(0,len(tehinguID)):
        
        if (tehinguAasta[item] == str(year)) and (tehinguKvartal[item] == str(quarter)):

            # Get all buyers and sellers in the quarter
            if tegevusAktsias[item] == '-1':
                currSellersQ += 1
            elif tegevusAktsias[item] == '1':
                currBuyersQ += 1
                
    return currBuyersQ, currSellersQ
    

# Get the LSV measure for the investor group
#       in a given quarter for the given stock
#       (assumes that some data exists for each quarter in the available years)
#       (otherwise activePropQ takes activeQ=0 to denominator and result is error)
def investorGroupStockQuarterLSV(buyersQS, sellersQS, buyersQ, sellersQ):
    
    # Define variables
    activeQS = buyersQS + sellersQS
    activeQ = buyersQ + sellersQ
    activePropQ = buyersQ/activeQ

    # Calculate initial LSVI
    print "STOCK - This quarter active: ", activeQS, ", and buyers: ", buyersQS
    print "ALL - This quarter active: ", activeQ, ", and buyers: ", buyersQ, ", and proportion: ", activePropQ
    indicatorLSVI = abs((buyersQS/activeQS)-activePropQ)

    # Create variable to calculate binomial distribution
    divisor = 1

    while divisor < activeQS:
        divisor *= 10

    # Adjust variables to calculate binomial distribution
    adjBuyersQS = (buyersQS/divisor)
    adjActiveQS = (activeQS/divisor)
    print "ADJUSTED STOCK - adjBuyersQS: ", adjBuyersQS, ", and adjActiveQS: ", adjActiveQS, ", and divisor: ", divisor
    
    # Calculate adjusted LSVI (same as previous LSVI on adj data)
    adjustedLSVI = abs((adjBuyersQS/adjActiveQS)-activePropQ)
    print "adjustedLSVI: ", adjustedLSVI

    # If wrong value, throw error
    if round(adjustedLSVI,10) != round(indicatorLSVI,10):
        raise ValueError("LSVI on adjusted data is different from initial!")

    # Calculate binomial probability
    binomialProb = ((math.gamma(adjActiveQS+1))*activePropQ*(1-activePropQ))/((math.gamma(adjActiveQS-adjBuyersQS+1))*(math.gamma(adjBuyersQS+1)))
    print "binomialProb: ", binomialProb

    # Calculate Adjustment factor
    adjFactor = binomialProb*adjustedLSVI
    print "adjFactor: ", adjFactor

    # Calculate LSV 
    indicatorLSV = adjustedLSVI - adjFactor
    print "indicatorLSV: ", indicatorLSV
    return indicatorLSV

# Year values array from array of "YYYY-Q" type
def yearFromYearQuarterArray(yearQuarterArray):
    yearArray = []
    
    for i in range(0,len(yearQuarterArray)):
        
        yearArray.append(yearQuarterArray[i][0:4])
        
    return yearArray

# Quarter values array from array of "YYYY-Q" type
def quarterFromYearQuarterArray(yearQuarterArray):
    quarterArray = []
    
    for i in range(0,len(yearQuarterArray)):
        
        quarterArray.append(yearQuarterArray[i][5:6])

    return quarterArray

# Create a string array from year array with quarters
def createYearQuarterArray(yearArray):
    yearsLen = int(len(list(set(yearArray))))
    firstYear = int(yearArray[0])
    years = []
    
    for i in range(firstYear,(firstYear+yearsLen)):
        
        years.append(str(i)+"-"+str(1))
        years.append(str(i)+"-"+str(2))
        years.append(str(i)+"-"+str(3))
        years.append(str(i)+"-"+str(4))
        
    return years

# Create matrix type variable (results in LSV indicators for each stock quarter)
def createMatrix(uniqueStocksArray, yearsQuartersArray):
    a = []
    
    for x in range(0,len(uniqueStocksArray)):
        row = []
        for y in range(0,len(yearsQuartersArray)):
            
            currentYear = getYearArrayFromYearQuarterArray(yearsQuartersArray)[y]
            currentQuarter = getQuarterArrayFromYearQuarterArray(yearsQuartersArray)[y]
            row.append(getStockQuarterLSV(uniqueStocksArray[x],currentYear,currentQuarter))
            
        a.append(row)
        
    return a


# -------------- IMPLEMENTATION

aastaKvartal = createYearQuarterArray(tehinguAasta)
matrixLSV = createMatrix(uniqueAktsiaNimi, aastaKvartal)

print matrixLSV


