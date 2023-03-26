
echo "$(date +"%Y-%m-%d %H:%M:%S");$(curl https://fr.finance.yahoo.com/quote/%5EIXIC?p=%5EIXIC | grep -o 'data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="[0-9.]*"' | grep -o 'value="[0-9.]*' | grep -o '[0-9.]*')" >> /home/admin/project/prix.csv
