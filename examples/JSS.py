# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 10:23:42 2022

@author: Siamak Khatami
@Email: siamak.khatami@ntnu.no
@License: https://creativecommons.org/licenses/by-nc-sa/4.0/
@Source: https://github.com/copatrec
@Document: https://github.com/copatrec
@WebApp: copatrec.org
@Cite:
"""
# Importing packages
import pandas as pd
import numpy as np
import pickle
import sys
try:
    from copatrec import Copatrec  # If package is installed
except ImportError:
    sys.path.append('../src/')
    from copatrec import Copatrec  # If package files cloned

# Setting up matplotlib plot text size
import matplotlib.pyplot as plt
plt.rc('axes', titlesize='18')
plt.rc('axes', labelsize='14')

# Read the data
data = pd.read_pickle("../data/GRIN.pkl")
# Fixing data types to proper ones (optional)
data = data.astype({'gdppc': float,
                    'Government Integrity': float,
                    'year': int,
                    'countryname': str})

# Initiating copatrec object
time_Col = 'year'
category_column = 'countryname'
Dep_Var = 'gdppc'

# report = true is not related to the report function of copatrec.
# it only sets weather a log of current progress should be generated or not.
# report_to_file=True will produce no log output in the terminal.
# To see the progress in the terminal first set
# report = true
# report_to_file=True

SM = Copatrec(data=data,
              dependent_var=Dep_Var,
              category_col=category_column,
              time_col=time_Col,
              report=True,
              report_to_file=False)

# Reproducing Figure 4 in the paper
# Running panel_outliers function
# Figure 4 (a) => First plot
# Figure 4 (b) => Third plot
intervals, outliers = SM.panel_outliers(method='beta',
                                        plot_pairs=True,
                                        plot_hists=True,
                                        plot_outliers_name=True)


# Reproducing Figure 5 Results in the paper
# Panel analysis

# Figure 5 (a)
# drop_outliers=True,
Opt_Forms_Dict1, All_Forms_Dict1, Error_Terms1 = SM.panel(max_epochs=8000,
                                                          alpha=0.05,
                                                          standardization=True,
                                                          plot=False,
                                                          show_time_label=False,
                                                          show_category_label=False,
                                                          drop_outliers=True,
                                                          show_outliers=True,
                                                          plot_predicted_outliers=True,
                                                          outlier_method='beta')

All_Forms_Dict1['Government Integrity']['logistic'].plot(show_outliers=True,
                                                         plot_predicted_outliers=True)

# Figure 5 (b)
# drop_outliers=False,
# This may add additional lines to the JSS.log file.
Opt_Forms_Dict2, All_Forms_Dict2, Error_Terms2 = SM.panel(max_epochs=8000,
                                                          alpha=0.05,
                                                          standardization=True,
                                                          plot=False,
                                                          show_time_label=False,
                                                          show_category_label=False,
                                                          drop_outliers=False,
                                                          show_outliers=True,
                                                          plot_predicted_outliers=True,
                                                          outlier_method='beta')

All_Forms_Dict2['Government Integrity']['logistic'].plot(show_outliers=True,
                                                         plot_predicted_outliers=True)

# Appendix B
# By running the above code, a file "JSS.log" will be created in the same repository of current file
# which holds the log output similar to the "Appendix B. Sample of log file content" in the paper.

# Appendix B
# In line 40 and considering:
# report=True,
# report_to_file=True

# By running the above code, a file "JSS.log" will be created in the same repository of current file
# which holds the log output similar to the "Appendix B. Sample of log file content" in the paper.

# Appendix C
All_Forms_Dict1['Government Integrity']['oscillating_growth'].report()

#                   EXTRA commands                   #
exit() # To run the below commands, please remove this line

Opt_Forms_Dict1['Government Integrity'].save("test")
# loading a result object (model)
file = open('test.pickle', 'rb')
res = pickle.load(file)
res.report()  # printing report