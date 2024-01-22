# New England Grid Outage Analysis

## Introduction

Welcome to the New England Grid Outage Analysis repository! This project focuses on data analysis and handling, particularly in the context of analyzing the resilience of the New England grid. As a grid operator, developer, or enthusiast, understanding outage patterns is crucial for decision-making and optimizing grid performance.

## Project Overview

### Data Collection

The project begins with the collection of outage data using a script (`line_outage_data_pull.py`). The data is stored in a CSV file (`api_data.csv`), which serves as the foundation for subsequent analyses.

### Filtering and Cleaning

The collected data is filtered to focus on line outages that have been implemented. Specific lines of interest, such as those with equipment descriptions '315' and '327', are extracted for further analysis. Duplicates are removed, and relevant columns are processed to convert dates and calculate outage durations.

### Yearly Analysis

The project includes a comprehensive yearly analysis of outage data. Outage durations for equipment descriptions '315' and '327' are grouped by year, providing insights into the overall trends and patterns over time.

### Visualization

Visualizations play a key role in conveying complex information. Two types of plots are generated:
1. **Yearly Graph**: A line graph illustrating the total outage hours for equipment descriptions '315' and '327' over the years.
![OccurencesTimeSeries](https://github.com/arturogalofre/NewEnglandGrid_OutageAnalysis/assets/75703907/ab6aa875-f199-483a-bd66-082fcba61eaa)


2. **Pie Distribution**: A pie chart displaying the distribution of outage time between the selected equipment descriptions.
![PieDistribution](https://github.com/arturogalofre/NewEnglandGrid_OutageAnalysis/assets/75703907/3c16c79f-a906-4c71-b32e-964700c23257)



### Time Series Analysis

A time series analysis is performed on a generated range of dates for the year 2022. The analysis includes the creation of a DataFrame (`date_df`) and the addition of columns (`Value315` and `Value327`) based on outage occurrences during specific date ranges.

![OutageOnOff](https://github.com/arturogalofre/NewEnglandGrid_OutageAnalysis/assets/75703907/865c2ce2-8966-4362-ad3b-5c5d708ad3d2)

### Code Organization

The code is organized into logical sections, each serving a specific purpose. Comments are provided throughout to enhance readability and understanding.

### Repository Structure

- **`data`**: Contains the input and output data files (`api_data.csv`, `line_data_df.csv`, `save_df.csv`).
- **`plots`**: Stores the generated plots (`OccurencesTimeSeries.png`, `PieDistribution.png`, `OutageOnOff.png`).
- **`scripts`**: Includes the main data analysis script (`loine_outage_data_pull.py`) and the code used for time series analysis.

## Conclusion

This repository not only demonstrates my proficiency in data analysis but also showcases my ability to derive meaningful insights from real-world datasets. The structured and well-documented code, coupled with insightful visualizations, reflects my commitment to delivering high-quality data analysis projects.

Feel free to explore the code, data, and visualizations to gain a deeper understanding of the New England grid outage analysis process. If you have any questions or would like to discuss specific aspects of the project, please don't hesitate to reach out.

Thank you for visiting this repository, and I look forward to your feedback and potential collaboration opportunities.

**Author: ArturoGalofre**
