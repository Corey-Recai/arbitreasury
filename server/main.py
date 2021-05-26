import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import cbpro
import pandas as pd
import time
import re
from db import insertBTCETHSignal, insertBTCLTCSignal, insertBTCXRPSignal, insertBTCETCSignal


def getData():
    # Read in username and password from environment variables
    def getKey(envParam):
        enVar = os.environ.get(envParam)
        return enVar

    # Set timeout for webdriver page loads
    timeout = 10

    # Delecare the webdriver for Selenium to use
    driver = webdriver.Chrome(
        executable_path="/Users/coreyrecai/Apps/arbitreasury/chrome_driver/chromedriver")
    driver.get("https://pro.coinbase.com/")

    # Check if Login Button is present
    loginElementPresent = EC.presence_of_element_located(
        (By.LINK_TEXT, 'Log In'))
    WebDriverWait(driver, timeout).until(loginElementPresent)
    # Click the Login Button
    driver.find_element_by_link_text('Log In').click()

    # Check if email address field has loaded
    signInBtnPresent = EC.presence_of_element_located(
        (By.XPATH, '//*[@id="signin_button"]'))
    WebDriverWait(driver, timeout).until(signInBtnPresent)
    # Send the email and password keys
    driver.find_element_by_xpath(
        '//*[@id="email"]').send_keys(getKey('COINBASE_USERNAME'))
    driver.find_element_by_xpath(
        '//*[@id="password"]').send_keys(getKey('COINBASE_PASSWORD'))
    # Submit the login form
    driver.find_element_by_xpath('//*[@id="signin_button"]').click()

    # If 2-step Verification then require token
    twoFactorAuth = True if EC.text_to_be_present_in_element(
        (By.XPATH, '//*[text()="2-Step Verification"]'), "2-Step Verification").text == "2-Step Verification" else False
    while True:
        if twoFactorAuth == True:
            try:
                # Declare token field
                authToken = driver.find_element_by_xpath('//*[@id="token"]')
                # Clear input field
                authToken.click()
                authToken.clear()
                # Require token input

                def getToken(message):
                    while True:
                        try:
                            userToken = int(input(message)[:7])
                            return userToken
                        except ValueError:
                            print('You must enter a number')
                            userToken = int(input(message)[:7])
                verificationCode = getToken('Enter 2-step verification code:')
                # Send token
                authToken.send_keys(verificationCode)
                driver.find_element_by_xpath(
                    '//*[@id="step_two_verify"]').click()
            except NoSuchElementException:
                break

    popUpModal = EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/div/div/div[1]/div'))
    popUpModalPresent = WebDriverWait(driver, timeout).until(popUpModal)

    if popUpModalPresent:
        driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div/div/div[2]/div/div/div[1]/div').click()
    else:
        pass

    # Check if Select Market field has loaded
    selectMarketPresent = EC.presence_of_element_located(
        (By.XPATH, '//*[text()="Select Market"]'))
    WebDriverWait(driver, timeout).until(selectMarketPresent)

    # Open Markets Panel
    driver.find_element_by_xpath('//*[text()="Select Market"]').click()

    # Get Crypto Price Data
    starttime = time.time()
    initialInvestment = 10000

    def toFloat(numString):
        numFloat = float(re.sub('\$|,', '', numString))
        return numFloat

    public_client = cbpro.PublicClient()

    def getTradeSize(arbiPair, investmentSize):
        # Get entire Coinbase Order Book
        book = public_client.get_product_order_book(arbiPair, level=3)
        # Loop through ask list and vol list and write data to separate lists
        askList = []
        askVolList = []
        w = -1
        for n in range(0, len(book['asks'])):
            w += 1
            askPrice = book['asks'][w][0]
            vol = book['asks'][w][1]

            askList.append(askPrice)
            askVolList.append(vol)

        # Loop through ask list and vol list and write data to separate lists
        bidList = []
        bidVolList = []
        x = -1
        for n in range(0, len(book['bids'])):
            x += 1
            askPrice = book['bids'][x][0]
            vol = book['bids'][x][1]

            bidList.append(askPrice)
            bidVolList.append(vol)

        # Declare DataFrame for ask price and vol
        askBook = pd.DataFrame()
        askBook['askList'] = askList
        askBook['volList'] = askVolList

        buySizeList = []

        y = -1
        for n in range(0, len(askList)):
            y += 1
            buySize = toFloat(askList[y])*toFloat(askVolList[y])
            buySizeList.append(buySize)

        askBook['buySizeList'] = buySizeList

        # Declare DataFrame for bid price and vol
        bidBook = pd.DataFrame()
        bidBook['bidList'] = bidList
        bidBook['volList'] = bidVolList

        sellSizeList = []

        z = -1
        for n in range(0, len(bidList)):
            z += 1
            sellSize = toFloat(bidList[z])*toFloat(bidVolList[z])
            sellSizeList.append(sellSize)

        bidBook['sellSizeList'] = sellSizeList
        return askBook, bidBook

    def getBTCUSDLastPrice():
        btc_usdLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[1]/div[1]/div[4]/span[1]').text)
        return btc_usdLastPrice

    def getBTCETHParams(btc_usdLastPrice):
        eth_usdLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[1]/div[2]/div[4]/span[1]').text)
        eth_btcLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[3]/div[1]/div[4]/span[1]').text)

        eth_btcImpliedPrice = eth_usdLastPrice/eth_btcLastPrice
        eth_btcProfitMargin = eth_btcImpliedPrice - btc_usdLastPrice
        eth_btcProfitMarginPercent = (eth_btcProfitMargin/btc_usdLastPrice)*100
        btc_ethIsTradable = True if eth_btcProfitMarginPercent > 0.05 else False
        btc_ethProfit = initialInvestment*eth_btcProfitMargin

        tradeSizeRequest = getTradeSize('ETH-BTC', btc_ethProfit)
        askBook = tradeSizeRequest[0]
        ourBuyPosition = {'askList': btc_ethProfit,
                          'volList': btc_ethProfit/eth_btcLastPrice,
                          'buySizeList': btc_ethProfit*(btc_ethProfit/eth_btcLastPrice)
                          }
        askBook = askBook.append(ourBuyPosition, ignore_index=True)
        askBook = askBook.astype(float)
        askBook = askBook.sort_values(by=['askList'], ascending=True)
        askBook = askBook.where(
            askBook['askList'] < ourBuyPosition['askList']).dropna()
        btc_ethIsLiquid = True if btc_ethProfit / \
            eth_btcLastPrice < sum(askBook['volList']) else False

        btc_ethParamList = [btc_usdLastPrice, eth_usdLastPrice, eth_btcLastPrice, eth_btcImpliedPrice, eth_btcProfitMargin,
                            eth_btcProfitMarginPercent, btc_ethIsTradable, btc_ethIsLiquid, initialInvestment, btc_ethProfit]
        return btc_ethParamList

    def getBTCLTCParams(btc_usdLastPrice):
        ltc_usdLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[1]/div[4]/div[4]/span[1]').text)
        ltc_btcLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[3]/div[3]/div[4]/span[1]').text)
        ltc_btcImpliedPrice = ltc_usdLastPrice/ltc_btcLastPrice
        ltc_btcProfitMargin = ltc_btcImpliedPrice - btc_usdLastPrice
        ltc_btcProfitMarginPercent = (ltc_btcProfitMargin/btc_usdLastPrice)*100
        ltc_btcIsTradable = True if ltc_btcProfitMarginPercent > 0.05 else False
        btc_ltcProfit = initialInvestment*ltc_btcProfitMargin
        btc_ltcParamList = [btc_usdLastPrice, ltc_usdLastPrice, ltc_btcLastPrice, ltc_btcImpliedPrice,
                            ltc_btcProfitMargin, ltc_btcProfitMarginPercent, ltc_btcIsTradable, initialInvestment, btc_ltcProfit]
        return btc_ltcParamList

    def getBTCXRPParams(btc_usdLastPrice):
        xrp_usdLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[1]/div[3]/div[4]/span[1]').text)
        xrp_btcLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[3]/div[2]/div[4]/span[1]').text)
        xrp_btcImpliedPrice = xrp_usdLastPrice/xrp_btcLastPrice
        xrp_btcProfitMargin = xrp_btcImpliedPrice - btc_usdLastPrice
        xrp_btcProfitMarginPercent = (xrp_btcProfitMargin/btc_usdLastPrice)*100
        xrp_btcIsTradable = True if xrp_btcProfitMarginPercent > 0.05 else False
        btc_xrpProfit = initialInvestment*xrp_btcProfitMargin
        btc_xrpParamList = [btc_usdLastPrice, xrp_usdLastPrice, xrp_btcLastPrice, xrp_btcImpliedPrice,
                            xrp_btcProfitMargin, xrp_btcProfitMarginPercent, xrp_btcIsTradable, initialInvestment, btc_xrpProfit]
        return btc_xrpParamList

    def getBTCETCParams(btc_usdlastPrice):
        etc_usdLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[1]/div[9]/div[4]/span[1]').text)
        etc_btcLastPrice = toFloat(driver.find_element_by_xpath(
            '//*[@id="page_content"]/div/div/div[2]/div[1]/div[1]/div[3]/div/div[3]/div/div/div/div[3]/div[2]/div[4]/span[1]').text)
        etc_btcImpliedPrice = etc_usdLastPrice/etc_btcLastPrice
        etc_btcProfitMargin = etc_btcImpliedPrice - btc_usdLastPrice
        etc_btcProfitMarginPercent = (etc_btcProfitMargin/btc_usdLastPrice)*100
        etc_btcIsTradable = True if etc_btcProfitMarginPercent > 0.05 else False
        btc_etcProfit = initialInvestment*etc_btcProfitMargin
        btc_etcParamList = [btc_usdLastPrice, etc_usdLastPrice, etc_btcLastPrice, etc_btcImpliedPrice,
                            etc_btcProfitMargin, etc_btcProfitMarginPercent, etc_btcIsTradable, initialInvestment, btc_etcProfit]
        return btc_etcParamList

    while True:
        btc_usdLastPrice = getBTCUSDLastPrice()

        btc_ethParamList = getBTCETHParams(btc_usdLastPrice)

        btc_ltcParamList = getBTCLTCParams(btc_usdLastPrice)

        btc_xrpParamList = getBTCXRPParams(btc_usdLastPrice)

        btc_etcParamList = getBTCETCParams(btc_usdLastPrice)

        insertBTCETHSignal(btc_ethParamList[0], btc_ethParamList[1], btc_ethParamList[2], btc_ethParamList[3],
                           btc_ethParamList[4], btc_ethParamList[5], btc_ethParamList[6], btc_ethParamList[7], btc_ethParamList[8])
        insertBTCLTCSignal(btc_ltcParamList[0], btc_ltcParamList[1], btc_ltcParamList[2], btc_ltcParamList[3],
                           btc_ltcParamList[4], btc_ltcParamList[5], btc_ltcParamList[6], btc_ltcParamList[7], btc_ltcParamList[8])
        insertBTCXRPSignal(btc_xrpParamList[0], btc_xrpParamList[1], btc_xrpParamList[2], btc_xrpParamList[3],
                           btc_xrpParamList[4], btc_xrpParamList[5], btc_xrpParamList[6], btc_xrpParamList[7], btc_xrpParamList[8])
        insertBTCETCSignal(btc_etcParamList[0], btc_etcParamList[1], btc_etcParamList[2], btc_etcParamList[3],
                           btc_etcParamList[4], btc_etcParamList[5], btc_etcParamList[6], btc_etcParamList[7], btc_etcParamList[8])
        time.sleep(0.1 - ((time.time() - starttime) % 0.1))


getData()
