import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import data_cleansing  # Assuming data_cleansing.py contains your data preprocessing functions
import data_analysis  # Assuming data_analysis.py contains your data analysis functions
import statsmodels.api as sm  # Import statsmodels

# Function to load and preprocess the data
def load_and_preprocess_data():
    df = data_cleansing.get_pd()
    return df

# Function to train a linear regression model
def train_linear_regression(X, Y):
    # Split data into training and testing sets (80% training, 20% testing)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Build the MLR model
    model = LinearRegression()

    # Fit the model to the training data
    model.fit(X_train, Y_train)

    # Get the coefficients (slopes) and intercept
    coefficients = model.coef_
    intercept = model.intercept_

    # Add a constant term (intercept) to the independent variables for statsmodels
    X_train_sm = sm.add_constant(X_train)

    # Fit the OLS (Ordinary Least Squares) model using statsmodels
    model_sm = sm.OLS(Y_train, X_train_sm).fit()

    return model, X_test, Y_test, coefficients, intercept, model_sm

# Function to evaluate the model
def evaluate_model(model, X_test, Y_test):
    # Predict the target variable for the test set
    y_pred = model.predict(X_test)

    # Evaluate the model (you can use different metrics like Mean Absolute Error, R-squared, etc.)
    mae = mean_absolute_error(Y_test, y_pred)
    r2 = r2_score(Y_test, y_pred)

    return mae, r2

def get_result(X, Y):
    # Train the linear regression model
    model, X_test, Y_test, coefficients, intercept, model_sm = train_linear_regression(X, Y)

    # Store coefficients, intercept, and p-values in a DataFrame
    results_df = pd.DataFrame({
        'Coefficient Names': X.columns.tolist() + ['Intercept'],
        'Coefficients': coefficients.tolist() + [intercept]
    })

    # Print p-values for the coefficients using statsmodels
    print("P-values for coefficients:")
    p_values = model_sm.pvalues.tolist()
    print(p_values)

    # Add p-values to the results DataFrame
    results_df['P-values'] = p_values

    # Evaluate the model
    mae, r2 = evaluate_model(model, X_test, Y_test)

    # Create DataFrames for Mean Absolute Error and R-squared
    mae_df = pd.DataFrame({'Coefficient Names': 'Mean Absolute Error', 'Coefficients': mae}, index=[0])
    r2_df = pd.DataFrame({'Coefficient Names': 'R-squared', 'Coefficients': r2}, index=[0])

    # Concatenate DataFrames to results_df
    results_df = pd.concat([results_df, mae_df, r2_df], ignore_index=True)

    print(f'Mean Absolute Error: {mae}')
    print(f'R-squared: {r2}')

    print('\n', results_df)
 
    # Save the results DataFrame to a CSV file
    results_df.to_csv('linear_regression_results.csv', index=False)

def main():
    # Load and preprocess the data
    df = load_and_preprocess_data()

    # print(df.info()) 
    print(df.head(5))
    
    print(df.describe())

    print("\n===================== Data Processing =====================\n")

    Sale_X = df[['Price', 'resoloution', 'weight', 'ppi', 'cpu core', 'cpu freq', 'internal mem', 'ram', 'RearCam', 'Front_Cam', 'battery', 'thickness']]
    Sale_Y = df['Sale']

    get_result(Sale_X, Sale_Y)
    print()
    # analysis_df = data_analysis.show_signi()

    Price_X = df[['resoloution', 'weight', 'ppi', 'cpu core', 'cpu freq', 'internal mem', 'ram', 'RearCam', 'Front_Cam', 'battery', 'thickness']]
    Price_Y = df['Price']
    get_result(Price_X, Price_Y)

    print("\n===================== Data Analysis =====================\n")

    # df = data_analysis.get_processedData()

    analysis_df = data_analysis.show_signi()

if __name__ == "__main__":
    main()

