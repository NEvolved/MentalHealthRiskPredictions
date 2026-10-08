def cleanWerkomgeving(X):
    X = X.copy()
    X["employment_status"] = X["employment_status"].replace({
        'Un-employed': 'Unemployed'
    })
    return X
def cleanDecimals(X):
    X = X.copy()
    X["productivity_score"] = (X["productivity_score"].astype(str).str.replace(r"\.\.", ".", regex=True))
    return X

def dropNAData(X):
    X = X.copy()
    return X.dropna()

def dropNonBinaryData(X):
    X = X.copy()
    X = X[X["gender"].isin(["Male", "Female"])]
    return X

def convertMentalHealthRisk(X):
    X = X.copy()
    risk_map = {'Low': 0, 'Medium': 1, 'High': 2}
    X['mental_health_risk'] = X['mental_health_risk'].map(risk_map)
    return X

def convertWordToNumericalColumns(X):
    X = X.copy()
    binary_map = {'No': 0, 'Yes': 1}
    X['seeks_treatment'] = X['seeks_treatment'].map(binary_map)
    X['mental_health_history'] = X['mental_health_history'].map(binary_map)
    return X
