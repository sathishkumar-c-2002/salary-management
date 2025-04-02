import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def generate_salary_report(data):
    # Create DataFrame
    df = pd.DataFrame([data])
    
    # Calculations
    df['total_income'] = df['basic_salary'] + df['incentives']
    df['total_expenses'] = df['spends'] + df['recharge'] + df['grocery']
    df['net_savings'] = df['total_income'] - df['total_expenses']
    df['savings_percentage'] = (df['net_savings'] / df['total_income']) * 100
    
    try:
        # Generate plot
        plt.figure(figsize=(10, 6))
        categories = ['Income', 'Expenses', 'Savings']
        values = [df['total_income'].values[0], 
                 df['total_expenses'].values[0], 
                 df['net_savings'].values[0]]
        
        plt.bar(categories, values, color=['green', 'red', 'blue'])
        plt.title('Salary Breakdown')
        plt.ylabel('Amount ($)')
        
        # Save plot to bytes
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', bbox_inches='tight')
        img_bytes.seek(0)
        plot_url = base64.b64encode(img_bytes.getvalue()).decode()
        
        # Close the figure to free memory
        plt.close()
        
        return {
            'calculations': df.to_dict('records')[0],
            'plot': plot_url
        }
        
    except Exception as e:
        print(f"Error generating plot: {str(e)}")
        return {
            'calculations': df.to_dict('records')[0],
            'plot': None,
            'error': str(e)
        }