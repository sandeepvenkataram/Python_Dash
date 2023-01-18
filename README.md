# Python_Dash

This is a Dashboard written in Python using the Plotly Dash library to visualize data from from Venkataram et al. Nature Ecology and Evolution (2023).

## Features

There are a series of 4 scatterplots and two tables.

The top-left scatterplot is the primary plot. Selecting ploints in this plot will highlight those points in the other plots and update the table of Adaptive Loci.

Hovering over a point in the primary plot will update the top-right table to show mutations identified in that isolate.

Selected genes in the adaptive loci table will further filter hilighted points in the bottom three plots.

Individual axes can be selected for each scatterplot along with whether they are displayed on a log2 or linear scale.

The checkboxes below each plot control additional traces, including OLS regression lines, Y=X line and the presence of errorbars.

## Dependencies

    Dash
    Dash Bootstrap Components
    Plotly
    Numpy
    Pandas
    
## Live Dashboard

A live version of this dashboard can be used at http://svenkataram.pythonanywhere.com/

