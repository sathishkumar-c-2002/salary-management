import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def generate_salary_report(data):
    df = pd.DataFrame([data])
    df['total_income'] = df['basic_salary']+df['incentives']
    df['total_expenses']= df['spends']+df['recharge']+df['grocery']
    df['net_savings']= df['total_income']  - df['total_expenses']
    df['savings_percentage'] = (df['net_savings']/df['total_income'])*100

    plt.figure(figsize=(10,6))
    categories = ['Income','Expenses','Savings']
    values = [df['total_income'].values[0],df['total_expenses'].values[0],df['net_savings'].values[0]]

    plt.bar(categories,values,color=['green','red','blue'])
    plt.title('Salary Breakdown')
    plt.ylabel('Amount ($)')

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes,format='png')
    img_bytes.seek(0)
    plot_url = base64.b64encode(img_bytes.getvalue()).decode()
    print('hi')

    return {
       
        'calculations': df.to_dict('records')[0],
        'plot':plot_url
    }
