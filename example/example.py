# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 10:23:42 2021

@author: Siamak Khatami
@Email: siamak.khatami@ntnu.no
@License: https://creativecommons.org/licenses/by-nc-sa/4.0/
@Source: https://github.com/copatrec
@document: https://github.com/copatrec
@Cite:
"""
import pandas as pd
import numpy as np
import pickle
import sys
try:
    from copatrec import Copatrec  # If package is installed
except ImportError:
    sys.path.append('../src/')
    from copatrec import Copatrec  # If package files cloned

import matplotlib.pyplot as plt
plt.rc('axes', titlesize='18')
plt.rc('axes', labelsize='14')
data = pd.read_pickle("../data/Data.pkl")
data = data[['countryname', 'year', 'gdppc', 'Government Integrity']]
time_Col = 'year'
category_column = 'countryname'
Dep_Var = 'gdppc'

data = data.astype({'gdppc': float,
                    'Government Integrity': float,
                    'year': int,
                    'countryname': str})

SM = Copatrec(data=data,
              dependent_var=Dep_Var,
              category_col=category_column,
              time_col=time_Col,
              report=True,
              report_to_file=True)

intervals, outliers = SM.panel_outliers(method='beta', 
                                        plot_pairs = True, 
                                        plot_hists = True, 
                                        plot_outliers_name=True)

Opt_Forms_Dict, All_Forms_Dict, Error_Terms = SM.panel(max_epochs=8000,
                                                       alpha=0.05,
                                                       standardization=True,
                                                       plot=True,
                                                       show_time_label=False,
                                                       show_category_label=False,
                                                       drop_outliers=False,
                                                       show_outliers=True,
                                                       plot_predicted_outliers=True,
                                                       outlier_method='beta')


Opt_Form = Opt_Forms_Dict['Government Integrity']
print(Error_Terms['Government Integrity'])
print(Opt_Forms_Dict['Government Integrity'].Equation_String)
# independent variable values should be standardized if the model has been standardized
print(Opt_Forms_Dict['Government Integrity'].predict(np.array([0.5,0.30,0.24])))
print(Opt_Forms_Dict['Government Integrity'].Time_col_name)
Opt_Form.report()
sys.exit()
# Funcitons with different setups
Opt_Form.save("test") # Saving summary object (model)
All_Forms_Dict['Government Integrity']['logistic'].summary_items() # Print items in model object
All_Forms_Dict['Government Integrity']['logistic'].Data # print dataset
All_Forms_Dict['Government Integrity']['logistic'].Independent_Var # independent variable name
All_Forms_Dict['Government Integrity']['logistic'].report() # print a report
All_Forms_Dict['Government Integrity']['logistic'].help() # print a general help

# loading a summary object (model)
file = open('test.pickle', 'rb')
summ = pickle.load(file)
summ.report() # printing report



