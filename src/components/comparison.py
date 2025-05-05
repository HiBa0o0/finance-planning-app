import pandas as pd

def compare_financing_plans(plan1, plan2):
    """
    Compare two financing plans and return a summary of differences.
    
    Parameters:
    - plan1: DataFrame representing the first financing plan.
    - plan2: DataFrame representing the second financing plan.
    
    Returns:
    - summary: DataFrame summarizing the comparison results.
    """
    summary = pd.DataFrame({
        'Metric': ['Cumulative Balance', 'Annual Costs'],
        'Plan 1': [plan1['Cumulative Balance'].sum(), plan1['Annual Costs'].sum()],
        'Plan 2': [plan2['Cumulative Balance'].sum(), plan2['Annual Costs'].sum()],
        'Difference': [
            plan1['Cumulative Balance'].sum() - plan2['Cumulative Balance'].sum(),
            plan1['Annual Costs'].sum() - plan2['Annual Costs'].sum()
        ]
    })
    
    return summary

def display_comparison(summary):
    """
    Display the comparison summary in a user-friendly format.
    
    Parameters:
    - summary: DataFrame containing the comparison results.
    """
    import streamlit as st
    
    st.title("Financing Plans Comparison")
    st.write(summary)