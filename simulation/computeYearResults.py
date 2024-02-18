def computeYearResults(tradeIndex,trade,profitsMonthOneYear,profitsMonth,profitsYear,yearsTradePositionTf,precedent,wallet):
    currentMonth = str(trade['month'].item())
    currentYear = str(trade['year'].item())
    currentWallet = trade['year'].item()

    currentWallet = trade['usdt size wallet'].item()
    if currentMonth != precedent['Month'] :

        if currentYear != precedent['Year'] :
            # for order book history and display
            yearTradePosition = (trade['year'].item(),tradeIndex)
            yearsTradePositionTf.append(yearTradePosition)
            
            if precedent['Year'] != '' :
                profitsMonthOneYear = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0, 6 : 0, 7 : 0, 8 : 0, 9 : 0, 10 : 0, 11 : 0, 12 : 0}
                year = trade['year'].item()
                profitsYear[year] = (currentWallet - wallet['precedentYear']) / wallet['precedentYear'] * 100
                profitsMonth[year] = profitsMonthOneYear
            precedent['Year'] = currentYear
            wallet['precedentYear'] = currentWallet

        if precedent['Month'] != '' :
            month = trade['month'].item()
            year = trade['year'].item()
            profitsMonthOneYear[month] = (currentWallet - wallet['precedentMonth']) / wallet['precedentMonth'] * 100
        precedent['Month'] = currentMonth
        wallet['precedentMonth'] = currentWallet

    return yearsTradePositionTf,profitsYear,profitsMonthOneYear,profitsMonth,precedent,wallet
