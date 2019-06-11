import numpy as np 


no_topics = [5, 10, 20, 25, 50]
no_years = 2016 - 1981

for no in no_topics:
	distribution = np.load("Distributions/" + str(no) + "topics.npy")
	weights = np.zeros((no_years, no))
	start = 0
	for i in range(1981, 2016):
		file = "new_data/" + str(i) + ".npy"
		year = np.load(file)

		year_data = distribution[start:start + len(year), :]

		yearly_sum = np.sum(year_data, axis = 0)/ len(year)
		weights[i - 1981] = yearly_sum
		start = start + len(year)

	np.save("Weights/" + str(no) + ".npy", weights)
