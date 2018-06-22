import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime

def getContentHTML(valURL):
    r = None
    try:
        r = requests.get(valURL)
        if(r.status_code == requests.codes.ok):
            return(r)
        else:
            print("ERROR: Status Code = "+str(r.status_code)+' for URL = '+str(valURL))
    except:
        print("ERROR: URL = "+str(valURL))
        
def getContentSoup(valRequest):
    rtnVal = None
    if(valRequest):
        if(valRequest.text is not None):
            rtnVal = BeautifulSoup(valRequest.text,'lxml')
    return(rtnVal)

def getHomeDetails(valSoupContent):
    tmpSoup = BeautifulSoup(valSoupContent,'lxml')
    valStrAddrStreet = tmpSoup.find('div',attrs={'class':'property-address'}).text.strip()
    valStrAddrCity = tmpSoup.find('div',attrs={'class':'property-city'}).text.strip()
    valNumPrice = tmpSoup.find('a',attrs={'class':'listing-price'}).text.strip()
    try:
        valNumSqFt = tmpSoup.find('div',attrs={'class':'property-sqft'}).text.strip()
    except:
        valNumSqFt = ''
    valNumBathsFull = tmpSoup.find('div',attrs={'class':'property-baths'}).text.strip()
    try:
        valNumBathsHalf = tmpSoup.find('div',attrs={'class':'property-half-baths'}).text.strip()
    except:
        valNumBathsHalf = ''
    valNumBedrooms = tmpSoup.find('div',attrs={'class':'property-beds'}).text.strip()
    return([valStrAddrStreet,valStrAddrCity,valNumPrice,valNumBathsFull,valNumBathsHalf,valNumBedrooms,valNumSqFt])

def getHomeDF(valRow):
    rtnVal = pd.DataFrame()
    valSoupContent = valRow['ResponseSoup']
    valSchoolID = valRow['ID']
    if(isinstance(valSoupContent,BeautifulSoup)):
        valSoupDivs = valSoupContent.find_all('div',attrs={'class':'property-card-primary-info'})
        vecHomeDetails = [getHomeDetails(str(x)) for x in valSoupDivs]
        dfHomeDetails = pd.DataFrame(vecHomeDetails,columns=['AddrStreet','AddrCity','Price','NumBathsFull','NumBathsHalf','NumBeds','NumSqFt'])
        #print(dfHomeDetails.shape)
        dfHomeDetails['ElementaryID'] = valSchoolID
        dfHomeDetails['DateRetrieved'] = datetime.datetime.now()
        dfHomeDetails['NumBathsFull'] = dfHomeDetails['NumBathsFull'].str.extract('([0-9]+)',expand=False)
        dfHomeDetails['NumBathsHalf'] = dfHomeDetails['NumBathsHalf'].str.extract('([0-9]+)',expand=False)
        dfHomeDetails['NumBeds'] = dfHomeDetails['NumBeds'].str.extract('([0-9]+)',expand=False)
        dfHomeDetails['NumSqFt'] = dfHomeDetails['NumSqFt'].str.extract('([0-9]+)',expand=False)
        #dfHomeDetails['Price'] = dfHomeDetails['Price'].str.extract('([0-9\,?]+)',expand=False)
        dfHomeDetails['Price'] = dfHomeDetails['Price'].astype(str)
        dfHomeDetails['Price'] = dfHomeDetails['Price'].str.replace(',','')
        dfHomeDetails['Price'] = dfHomeDetails['Price'].str.replace('$','')

        dfHomeDetails['NumBathsFull'] = pd.to_numeric(dfHomeDetails['NumBathsFull'])
        dfHomeDetails['NumBathsHalf'] = pd.to_numeric(dfHomeDetails['NumBathsHalf'])
        dfHomeDetails['NumBeds'] = pd.to_numeric(dfHomeDetails['NumBeds'])
        dfHomeDetails['NumSqFt'] = pd.to_numeric(dfHomeDetails['NumSqFt'])
        dfHomeDetails['Price'] = pd.to_numeric(dfHomeDetails['Price'])
        rtnVal = dfHomeDetails
    return(rtnVal)