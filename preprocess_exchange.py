import numpy as np  

codes = ["CAD", "GBP", "JPY", "Swiss"]
yearly_exchange_rate = np.zeros((36, 4))
for k in range(0, 4):

	file = open("USD_" + codes[k] + ".txt")

	number = []
	for f in file:
		number.append(float(f[8:]))



	#yearly_exchage_rate = []
	start = 120
	for j in range(1981, 2017):
		tot = 0.0
		for i in range(0, 12):
			tot = tot + number[start + i]

		tot = tot/12
		start = start + 12
		yearly_exchange_rate[j - 1981][k] = tot


np.save("new_data/exchange_rates", yearly_exchange_rate)



