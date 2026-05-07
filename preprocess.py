import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import glob

def process_participant_data(base_dir):
    # Initialize lists to store all processed dataframes
    all_touch_logs = []
    all_sensor_logs = []

    # Get all participant folders
    participant_folders = sorted(glob.glob(os.path.join(base_dir, 'data', 'P-*')))
    
    # Target package
    TARGET_PACKAGE = 'com.ss.android.ugc.trill'
    
    # Iterate over participant folders
    for folder in tqdm(participant_folders, desc="Processing Participants"):
        participant_id = os.path.basename(folder)
        
        for condition in ['Mindful', 'Mindless']:
            touch_file = os.path.join(folder, f'TouchLog_{participant_id}_{condition}.csv')
            sensor_file = os.path.join(folder, f'SensorLog_{participant_id}_{condition}.csv')
            
            if not (os.path.exists(touch_file) and os.path.exists(sensor_file)):
                print(f"Skipping {participant_id} {condition} - Files not found.")
                continue
                
            # 1. TouchLog Trimming & Feature Engineering
            try:
                touch_df = pd.read_csv(touch_file)
            except Exception as e:
                print(f"Error reading {touch_file}: {e}")
                continue

            # Keep only target package
            if 'PackageName' in touch_df.columns:
                touch_df = touch_df[touch_df['PackageName'] == TARGET_PACKAGE].copy()
            else:
                continue

            if touch_df.empty:
                continue
                
            # Need to sort by timestamp for delta calculations
            if 'Timestamp' not in touch_df.columns:
                continue
                
            # Enforce numeric timestamp
            touch_df['Timestamp'] = pd.to_numeric(touch_df['Timestamp'], errors='coerce')
            touch_df = touch_df.dropna(subset=['Timestamp'])
                
            touch_df = touch_df.sort_values(by='Timestamp').copy()
            
            # Form numeric variables
            for col in ['ScrollDeltaX', 'ScrollDeltaY']:
                if col in touch_df.columns:
                    touch_df[col] = pd.to_numeric(touch_df[col], errors='coerce').fillna(0)
            
            # Get Session Boundaries
            min_timestamp = touch_df['Timestamp'].min()
            max_timestamp = touch_df['Timestamp'].max()
            
            # Calculate Time_Delta_Sec
            time_diff = touch_df['Timestamp'].diff()
            touch_df['Time_Delta_Sec'] = time_diff / 1000.0 
            
            # Calculate Swipe_Distance
            if 'ScrollDeltaX' in touch_df.columns and 'ScrollDeltaY' in touch_df.columns:
                touch_df['Swipe_Distance'] = np.sqrt(touch_df['ScrollDeltaX']**2 + touch_df['ScrollDeltaY']**2)
            else:
                touch_df['Swipe_Distance'] = np.nan
                
            # Calculate Scroll_Velocity
            safe_time_delta = touch_df['Time_Delta_Sec'].replace(0, np.nan)
            touch_df['Scroll_Velocity'] = touch_df['Swipe_Distance'] / safe_time_delta
            
            # Context Labeling
            touch_df['Participant_ID'] = participant_id
            touch_df['Condition'] = condition
            
            all_touch_logs.append(touch_df)
            
            # 2. SensorLog Trimming & Feature Engineering
            try:
                sensor_df = pd.read_csv(sensor_file)
            except Exception as e:
                print(f"Error reading {sensor_file}: {e}")
                continue
                
            if 'Timestamp' not in sensor_df.columns:
                continue
                
            # Enforce numeric timestamp
            sensor_df['Timestamp'] = pd.to_numeric(sensor_df['Timestamp'], errors='coerce')
            sensor_df = sensor_df.dropna(subset=['Timestamp'])
                
            # Form numeric variables
            for col in ['X', 'Y', 'Z']:
                if col in sensor_df.columns:
                    sensor_df[col] = pd.to_numeric(sensor_df[col], errors='coerce').fillna(0)
                    
            # Filter matching timestamps
            sensor_df = sensor_df[(sensor_df['Timestamp'] >= min_timestamp) & (sensor_df['Timestamp'] <= max_timestamp)].copy()
            
            if sensor_df.empty:
                continue
                
            sensor_df = sensor_df.sort_values(by='Timestamp').copy()
            
            # Calculate Time_Delta_Sec
            s_time_diff = sensor_df['Timestamp'].diff()
            sensor_df['Time_Delta_Sec'] = s_time_diff / 1000.0
            
            # Calculate Magnitude
            if all(col in sensor_df.columns for col in ['X', 'Y', 'Z']):
                sensor_df['Magnitude'] = np.sqrt(sensor_df['X']**2 + sensor_df['Y']**2 + sensor_df['Z']**2)
                
                # Calculate Orientation
                is_accel = sensor_df['Sensor_Type'] == 'ACCEL' if 'Sensor_Type' in sensor_df.columns else pd.Series(False, index=sensor_df.index)
                
                # Pitch
                sensor_df.loc[is_accel, 'Pitch'] = np.degrees(np.arctan2(
                    sensor_df.loc[is_accel, 'Y'],
                    np.sqrt(sensor_df.loc[is_accel, 'X']**2 + sensor_df.loc[is_accel, 'Z']**2)
                ))
                
                # Roll
                sensor_df.loc[is_accel, 'Roll'] = np.degrees(np.arctan2(
                    -sensor_df.loc[is_accel, 'X'],
                    sensor_df.loc[is_accel, 'Z']
                ))
            else:
                sensor_df['Magnitude'] = np.nan
                sensor_df['Pitch'] = np.nan
                sensor_df['Roll'] = np.nan
                
            # Context Labeling
            sensor_df['Participant_ID'] = participant_id
            sensor_df['Condition'] = condition
            
            all_sensor_logs.append(sensor_df)

    # 3. Aggregation
    master_dir = os.path.join(base_dir, 'master')
    os.makedirs(master_dir, exist_ok=True)
    
    if all_touch_logs:
        master_touch = pd.concat(all_touch_logs, ignore_index=True)
        touch_out = os.path.join(master_dir, 'Master_TouchLog_All.csv')
        master_touch.to_csv(touch_out, index=False)
        print(f"Saved Master TouchLog with {len(master_touch)} rows to {touch_out}")
    else:
        print("No valid TouchLog data found.")
        
    if all_sensor_logs:
        master_sensor = pd.concat(all_sensor_logs, ignore_index=True)
        sensor_out = os.path.join(master_dir, 'Master_SensorLog_All.csv')
        master_sensor.to_csv(sensor_out, index=False)
        print(f"Saved Master SensorLog with {len(master_sensor)} rows to {sensor_out}")
    else:
        print("No valid SensorLog data found.")

if __name__ == '__main__':
    workspace_root = '.'  # Adjust if your data is in a different location
    process_participant_data(workspace_root)
