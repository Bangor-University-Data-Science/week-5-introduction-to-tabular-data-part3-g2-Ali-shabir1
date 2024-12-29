#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

def import_data(filename: 'Customer_Behavior.xlsx') -> pd.DataFrame:
    """
    Import the dataset from an Excel or CSV file into a DataFrame.

    Args:
        filename: The name of the dataset file (string).

    Returns:
        A Pandas DataFrame with the dataset.
    """
    try:
        if filename.endswith('.xlsx'):
            return pd.read_excel(filename, engine='openpyxl')
        elif filename.endswith('.csv'):
            return pd.read_csv(filename)
        else:
            raise ValueError("Unsupported file format. Please provide an Excel (.xlsx) or CSV (.csv) file.")
    except Exception as e:
        raise ValueError(f"Error loading file {filename}: {e}")

def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the data by removing rows with any missing CustomerID and excluding rows with negative values in either Quantity or UnitPrice.

    Args:
        df: The raw DataFrame.

    Returns:
        A filtered DataFrame with complete and positive records only.
    """
    df = df.dropna(subset=['CustomerID'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    return df

def loyalty_customers(df: pd.DataFrame, min_purchases: int) -> pd.DataFrame:
    """
    Identify loyal customers based on a minimum purchase threshold.

    Args:
        df: The cleaned DataFrame.
        min_purchases: Minimum number of purchases required to qualify as a loyal customer.

    Returns:
        A DataFrame listing customers who have made at least min_purchases transactions, including the count of their purchases.
    """
    customer_purchases = df.groupby('CustomerID').size()
    loyal_customers = customer_purchases[customer_purchases >= min_purchases].reset_index(name='Purchase Count')
    return loyal_customers

def quarterly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the total revenue per quarter.

    Args:
        df: The cleaned DataFrame.

    Returns:
        A DataFrame with two columns: quarter and total_revenue.
    """
    df['Total'] = df['Quantity'] * df['UnitPrice']
    df['Quarter'] = pd.to_datetime(df['InvoiceDate']).dt.to_period('Q')
    revenue = df.groupby('Quarter')['Total'].sum().reset_index(name='Total Revenue')
    return revenue

def high_demand_products(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    """
    Identify the top_n products with the highest total quantity sold across all transactions.

    Args:
        df: The cleaned DataFrame.
        top_n: Number of top products to return.

    Returns:
        A DataFrame listing the top_n most demanded products based on total quantity sold.
    """
    product_demand = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False)
    return product_demand.head(top_n).reset_index(name='Total Quantity Sold')

def purchase_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary showing the average quantity and average unit price for each product.

    Args:
        df: The cleaned DataFrame.

    Returns:
        A DataFrame with three columns: product, avg_quantity, and avg_unit_price.
    """
    patterns = df.groupby('Description').agg(
        avg_quantity=('Quantity', 'mean'),
        avg_unit_price=('UnitPrice', 'mean')
    ).reset_index()
    return patterns

def answer_conceptual_questions() -> dict:
    """
    Returns answers to conceptual multiple-choice questions as a dictionary.

    Returns:
        A dictionary where each key is a question number (e.g., "Q1", "Q2")
        and each value is a set of answer choices (e.g., {"A"}, {"A", "C"}).
    """
    return {
        "Q1": {"A", "D"},
        "Q2": {"B"},
        "Q3": {"A", "C"},
        "Q4": {"A", "B"},
        "Q5": {"A"}
    }

if __name__ == "__main__":
    # Example usage of the functions
    filename = "Online Retail.xlsx"

    # Import data
    print("Importing data...")
    df = import_data(filename)

    # Filter data
    print("Filtering data...")
    cleaned_df = filter_data(df)

    # Identify loyal customers
    print("Identifying loyal customers...")
    loyal_customers_df = loyalty_customers(cleaned_df, min_purchases=10)
    print(loyal_customers_df)

    # Calculate quarterly revenue
    print("Calculating quarterly revenue...")
    quarterly_revenue_df = quarterly_revenue(cleaned_df)
    print(quarterly_revenue_df)

    # Find high-demand products
    print("Finding high-demand products...")
    high_demand_df = high_demand_products(cleaned_df, top_n=5)
    print(high_demand_df)

    # Analyze purchase patterns
    print("Analyzing purchase patterns...")
    patterns_df = purchase_patterns(cleaned_df)
    print(patterns_df.head())

    # Answer conceptual questions
    print("Answering conceptual questions...")
    mcq_answers = answer_conceptual_questions()
    print(mcq_answers)


# In[ ]:




