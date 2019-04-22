import joblib
import os
import pandas as pd
import sklearn

model_folder = "."
model = joblib.load(os.path.join(model_folder, "model.joblib"))


# Describes how categorical columns are to be one-hot encoded.
# Lists describe the columns to include.
# Dictionaries describe how to group values into columns. (For example, rather than including
# several different columns for countries, they are grouped into three columns for simplicity.
# They weren't grouped arbitrarily but also not based on a proper analysis.)
onehot_columns = {
	"workclass": ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov"],#, "Without-pay", "Never-worked"],
	"marital-status": {"Married": ["Married-civ-spouse", "Married-AF-spouse"], "Divorced":["Divorced"], "Never-married":["Never-married"], "Separated":["Separated"], "Widowed":["Widowed"], "Married-spouse-absent":["Married-spouse-absent"]},
	"occupation": ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"],
	"relationship": ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"],
	"race": ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"],
	"native-country": {
		"USA" : ["United-States"],
		"G7": ["England", "Canada", "Germany", "Japan", "Italy", "France"],
		"Other": ["Cambodia", "Puerto-Rico" "Outlying-US(Guam-USVI-etc)", "India", "Greece", "South", "China", "Cuba", "Iran", "Honduras", "Philippines", "Poland", "Jamaica", "Vietnam", "Mexico", "Portugal", "Ireland", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti", "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia", "El-Salvador", "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands"]
	}
}

def to_predictable(df):
	"""
	Converts a data frame in the raw format to a format that can be used for model selection and predictions
	"""
	
	# Numeric columns require no modifications
	predictable = df[["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]].copy()
	
	# Change sex into a boolean column
	predictable["Male"] = df["sex"] == "Male"
	
	# Do the one-hot encoding as described above
	for c in onehot_columns:
		if isinstance(onehot_columns[c], dict):
			for v in onehot_columns[c]:
				predictable[c + "-" + v] = df[c].isin(onehot_columns[c][v])
		else:
			for v in onehot_columns[c]:
				predictable[c + "-" + v] = df[c] == v

	return predictable


def get_donor_class(age=None,
		workclass=None,
		education_num=None,
		marital_status=None,
		occupation=None,
		relationship=None,
		race=None,
		sex=None,
		capital_gain=None,
		capital_loss=None,
		hours_per_week=None,
		native_country=None):

	example = pd.DataFrame.from_dict({
		"age":[age],
		"workclass":[workclass],
		"education-num":[education_num],
		"marital-status":[marital_status],
		"occupation":[occupation],
		"relationship":[relationship],
		"race":[race],
		"sex":[sex],
		"capital-gain":[capital_gain],
		"capital-loss":[capital_loss],
		"hours-per-week":[hours_per_week],
		"native-country":[native_country],
		"label":"?",
	})
	predictable = to_predictable(example)
	return model.predict(predictable)[0]
