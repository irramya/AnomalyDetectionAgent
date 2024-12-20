import os
# paths

project_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
project_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(project_path, 'data/financial_anomaly_data.csv')
uploaded_files = os.path.join(project_path, 'data/uploaded_files')
temp_file = os.path.join(uploaded_files, 'temp_file.csv')
temp_ext_file = os.path.join(uploaded_files, 'temp_ext_file.csv')
temp_anom_file = os.path.join(uploaded_files, 'temp_anom_file.csv')