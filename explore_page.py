import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gdown 


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor's degree" in x:
        return "Bachelor's degree"
    if "Master's degree" in x:
        return "Master's degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than a Bachelors"
    
@st.cache ## cache's the code below so we don't have to reload each time the code is refreshed.
def load_data():
	url = https://drive.google.com/file/d/1XMLadcyLhIvax7VPL3I5OiFdTqIFSH1l/view?usp=drive_link
	output = "survey_results_public.csv"
	gdown.download(url, output, quiet=False)

	df = pd.read_csv(output)
	#df = pd.read_csv("survey_results_public.csv")
	df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
	df.rename({"ConvertedComp": "Salary"}, axis=1, inplace=True)
	df = df[df["Salary"].notnull()]
	df.dropna(inplace=True)
	df = df[df["Employment"] == "Employed full-time"]
	df.drop("Employment", axis=1, inplace=True)

	country_map = shorten_categories(df.Country.value_counts(), 400)
	df["Country"] = df["Country"].map(country_map)
	df = df[df["Salary"] <= 250000]
	df = df[df["Salary"] >= 10000]
	df = df[df["Country"] != "Other"]

	df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
	df["EdLevel"] = df["EdLevel"].apply(clean_education)

	return df
df = load_data()

def show_explore_page():
	st.title("Explore Software Engineer Salaries")
	st.write(
	"""
	### Stack Overflow Developer Survey 2020
	""") # writes a heading
	data = df["Country"].value_counts()
	
	fig1, ax1 = plt.subplots()
	ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
	ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

	st.write("""### Number of Data from different countries""")
	st.pyplot(fig1)
	
