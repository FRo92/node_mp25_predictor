# MP2.5 Model predictor 🔮

This repository includes the implementation of a base model based by LightGBM along with the construction of features relevant to the problem.
To run this models you must to have MP2.5 measures and meteorological variables such as temperature, humidity and pressure.

## Features 🧩
Mainly there are two types of features, continuous and categorical variables.

### Continuos Variables 
Is recommended that these variables are measured along the MP2.5 Node sensor.

| Variable    | type |  unit |
| -------- | ------- |------|
| Temperature  | float   | celcius |
| Relative Humidity | float    | percent |
| Pressure    | float    | hPa |

### Categorical Features
Categorical features are built from timestamp of measures and traffic conditions near de node sensor. Mainly are calendar variables.
Here are examples of features:

| Variable    | description |  values |
| -------- | ------- | ------|
| Traffic  | evaluates from 1 to 7 the level of traffic near node   | 1 to 7 |
| common holidays  | mark with a 1 the common holidays    | 0 or 1 |
| previous days to holidays    | mark with a 1 the previous day to holiday    | 0 or 1 |
|Christmast      | mark with a 1 Xmast day  |  0 or 1    |
|  National Holidays   | mark with a 1 the days during Nationals Holidays     | 0 or 1 |
|  season  | 4 if winter, 3 if autum, 2 if spring, 1 if summer    | 0 or 1 |

## How to run the model 🪄
First you need to build the feature dataframe.
Run in your terminal
```python 
python events.py
```
Once built the features you are ready to run de predict model:
```
make predict
```

## Contact 📬
If you have troubles, questions or improvements please contact francis.rojas@uc.cl
