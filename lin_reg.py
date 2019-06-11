from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt



#old_y = np.load("new_data/exchange_rates.npy")



PPP = pd.read_excel("../PPP_Country.xlsx")
PPP = np.array(PPP)
PPP = PPP[:, 1:]
temp = PPP[:, 1]
PPP[:, 1] = PPP[:, 0]
PPP[:, 0] = temp

GDP = pd.read_excel("../GDP_Country.xlsx")
GDP= np.array(GDP)
GDP = GDP[:, 1:]
temp = GDP[:, 1]
GDP[:, 1] = GDP[:, 0]
GDP[:, 0] = temp

ex = pd.read_excel("../Country_Exrate.xlsx")
ex = np.array(ex)
old_y = ex[:, 1:]
y = old_y[1:]

country = ["CHN", "INR", "GBP", "CAD", "JPY", "SWISS"]
regressor = ["Linear", "Ridge", "Support Vector","Random Forest"]

#distros = [5, 10, 20, 25, 50]
distros = [5]
count = 0

all_error = np.empty((5, 6, 4), dtype=object)
for distro in distros:
    weights = np.load("Weights/" + str(distro) + ".npy")
    weights = weights*100
    #weights = weights[:, :4]
    #weights = np.append(weights[:, :4], weights[:, 1:], 1)

    #weights = weights[2:]
    print(old_y[:len(old_y) - 1, 1].reshape(-1, 1).shape)
    print(weights.shape)
    #weights = np.append(weights, old_y[:len(old_y) - 1 , 1].reshape(-1, 1), 1)
    #print(weights)
    total_error = 0.0
    for rate in range(0, 6):
        new_weights = np.append(weights, old_y[:len(old_y) - 3, rate].reshape(-1, 1), 1)
        #new_weights = old_y[:len(old_y) - 3, rate].reshape(-1, 1)
        new_weights = np.append(new_weights, GDP[:len(GDP) - 3, rate].reshape(-1, 1), 1)
        #new_weights = PPP[:len(PPP) - 3, rate].reshape(-1, 1)
        #new_weights = np.append(weights,  PPP[:len(PPP) - 3, rate].reshape(-1, 1), 1)
        new_weights = np.append(new_weights, PPP[:len(PPP) - 3, rate].reshape(-1, 1), 1)
        #new_weights = np.append(new_weights, ex[:len(ex) - 3, rate].reshape(-1, 1), 1)
        for network in range(0, 4):

            errors = []
            for i in range(2000, 2015):
            	#reg = SVR(gamma='auto', kernel='rbf')
                reg = None
                if network == 0:
                    reg = LinearRegression()
                if network == 1:
                    reg = Ridge(alpha=0.01)
                if network == 2:
                    reg = SVR(gamma='auto', kernel='rbf')
                if network == 3:
                    reg = RandomForestRegressor(n_estimators = 100)

                reg.fit(new_weights[0:(i - 1981), :], y[0:(i - 1981), rate])
                prediction = reg.predict(new_weights[i - 1981, :].reshape(1, -1))
                error = np.abs((prediction - y[i - 1981, rate])/y[i - 1981, rate])
            	#print("Prediction" + str(prediction))
            	#print("Actual is " + str(y[i - 1971, rate]))
            	#print(weights[i - 1971, :])
            	#print(reg.predict(weights[i - 1971, :].reshape(1, -1)))
            	#if i == 2015:
            	    #print(reg.coef_)
                if network == 3 and i == 2014:
                    features = ["Cluster 1", "Cluster 2", "Cluster 3", "Cluster 4", "Cluster 5", "Previous Exchange Rate", "GDP", "PPP"]
                    importances = reg.feature_importances_
                    indices = np.argsort(importances)
                    new_features = np.empty((8), dtype='object')
                    for tt in range(0, 8):
                        new_features[tt] = features[indices[tt]]
                    fig, ax = plt.subplots()
                    plt.title('Feature Importances for Country ' + country[rate])
                    plt.barh(range(len(indices)), importances[indices], color='#8f63f4', align='center')
                    plt.xlabel('Relative Importance')
                    ax.set_yticks(np.arange(len(indices)))
                    ax.set_yticklabels(new_features)
                    
                    plt.savefig(country[rate] + "_remove_prev.png")
                total_error = total_error + error
                errors.append(error)
            print("The average error for " + str(country[rate]) + " with a " + str(regressor[network]) + " regressor with " + str(distro) + " number of clusters is " + str(total_error/16))
            total_error = 0.0

            all_error[count][rate][network] = errors

    count = count + 1

for i in range(0, 1):
    for j in range(0, 4):
        CHN_mean = np.mean(all_error[i][0][j])
        CHN_std = np.std(all_error[i][0][j])
        INR_mean = np.mean(all_error[i][1][j])
        INR_std = np.std(all_error[i][1][j])
        GBP_mean = np.mean(all_error[i][2][j])
        GBP_std = np.std(all_error[i][2][j])
        CAD_mean = np.mean(all_error[i][3][j])
        CAD_std = np.std(all_error[i][3][j])
        JPY_mean = np.mean(all_error[i][4][j])
        JPY_std = np.std(all_error[i][4][j])
        SWS_mean = np.mean(all_error[i][5][j])
        SWS_std = np.std(all_error[i][5][j])

        if j == 3:
            print(CHN_mean)
            print(INR_mean)
            print(GBP_mean)
            print(CAD_mean)
            print(JPY_mean)
            print(SWS_mean)

        currency = ["CHN", "INR", "GBP", "CAD", "JPY", "SWS"]
        x_pos = np.arange(len(currency))
        CTEs = [CHN_mean, INR_mean, GBP_mean, CAD_mean, JPY_mean, SWS_mean]
        error = [CHN_std, INR_std, GBP_std, CAD_std, JPY_std, SWS_std]

        fig, ax = plt.subplots()
        ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Average Error')
        ax.set_xlabel("Currency Exchange")
        ax.set_xticks(x_pos)
        ax.set_xticklabels(currency)
        ax.set_title('Average Error of ' + str(regressor[j]) + " Regressor with " + str(distros[i]) + " Clusters")
        ax.yaxis.grid(True)

        # Save the figure and show
        plt.tight_layout()
        plt.ylim((0, 0.6))
        plt.savefig(str(regressor[j]) + str(distros[i]) + ".png")
        #plt.show()


np.save("all_error", all_error)



