# Docs!
## Table of contents
1. Introduction
2. Dependencies (libraries)
3. Usage

## Introduction:

### what it does

In the current state of the project, you can:

* Visualize columns of a .csv file:
  * Histograms
  * Plots
  * Scatter Plots
  * Select a filter column and do the same plots as above  

* Clusterize based on numerical featues (K-Means algorith, n supplied b the user)
  
### what it will do

* Description of the .csv file:
  * Give all the basic descriptive summary statistics (count,mean, std,...) in a table

* Data mangling through different methods:
  * standardize and normalize columns
  * binarize labels (apply ML algorithms)
  * OHE on categorical varialbles (to perform some ML algorithms)

* Data Analysis:
  * Train Classification algorithm (start with regression)
  * Traing Regression Models (start with linear regression )
  
## Dependencies:

This project relies on the following libreries:t
*  PyQt4 (v4.8.7)
*  matplotlib (v2.1.0)
*  numpy (v1.13.3)
*  scipy (v1.0.0)
*  sklearn (v1.19.1)

Any aditional information on what aditional packages are beeing used (if so) please send an issue.

## Usage:

start the program from the folder "dirty" and execute python "main.py", if every dependency is installed,
it will launch a window with the following elements:
1. Column 1:
  * A plain text input (inp - lineEditwidget): through this widgets you will load the data (try: iris.csv)
  * Read File button (rdBtn - QpushButton ): when you wrote the name of the file you want to read click-it and the data will apear on the...
  * Dataframes List (dfList - QlistWidget): displays all the dataframes in memory, double click one to se it's columns
  * Plots List (plotsList -QlistWidget): displays all the plots you have made from the currently selected dataframe (last one double clicked on dfList)
  * Analysis button (aBtn - pushButton): click this and it will spawn a child window to perform analysis. More on this latter.

2. Column 2:

  * A canvas and a toolkit: here will be displayed all the plotsyou produce, don't worry if it disapears suddenly, it should all come back when you double click a plot in tthe Plots List (it's not a bug it's a *feature*)
  
3. Column 3:

  * Columns availables list (colList - QlistWidget): shows all the columns in the dataframe you just double clicked. double click one column here and it will pass to the staging area
  * ComboBox of graphs (plotBox - QcomboBox): select the plot you want to generate! you can choose between histograms plots or scatter plots (this last one requires for you to have 2 columns in the staging list) 
  * Selected Columns list (stgList - QlistWidget): shows all the columns in the staging area, this columns will be used to generate plots (histograms, scatter) 
  * nameless ComboBox (filter combobox) (filterBox - QcomboBox): Select a column (preferably a categorical one (try species from the iris.csv file)) this will make your visualizations a lot more atractive plotting each different species in a different color, but in the same figure, just hit the
  * Plot Button (plotBtn - PushButton): press it to generate plots.
  
 this is everything you got to know to use the basics... to do clusterization, keep reading
 
 ### Analysis Window
 
 this windows has few elements:
 
 1. Analysis ComboBox (aBox -QcomboBox): select which kind of analysis you want to perform (just Cluster is implemented)
 2. Input (inp - lineEdit): here you enter some metadata for the algorithm, in the case of clustering, the number of clusters you want to generate (the only thing that for now)
 3. Options List (optList - QlistWidget): shows all the columns of the current dataframe selected (the last you double clicked). Doubleclick a column here to move it to the
 4. Feature List (featList - QlistWidget): shows the columns which the algorith will use to training (*just numeric features for now!*). Double click a column here to remove it from the list.
 5. Fit Button (fitBrn - QpusButton): click this to fit the model, a message will be displayed on the console when the model finish training (prints "Done!")


Well, that's about it, more documentation will be added when necessary.

# Have fun exploring data!
  
  
