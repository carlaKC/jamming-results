import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) != 3:
    print("Usage: python reputation_graph.py <file> <channel_id>")
    sys.exit(1)

file_path = sys.argv[1]
channel_id = int(sys.argv[2])

# Load CSV data
df = pd.read_csv(file_path)

# Filter for the specified outgoing channel ID
df_filtered = df[df['outgoing_channel_id'] == channel_id]


df_filtered['reputation_delta'] = df_filtered['outgoing_reputation'] - df_filtered['in_flight_risk'] - df_filtered['htlc_risk'] - df_filtered['incoming_revenue'] 

# Example DataFrame (replace this with your actual DataFrame)
# df_filtered = pd.DataFrame({'reputation_delta': your_data_here})

outlier_threshold = 1
lower_percentile = np.percentile(df_filtered['reputation_delta'], outlier_threshold)
upper_percentile = np.percentile(df_filtered['reputation_delta'], 100 - outlier_threshold)
df_smooth = df_filtered[(df_filtered['reputation_delta'] >= lower_percentile) & (df_filtered['reputation_delta'] <= upper_percentile)]

# Step 2: Calculate the Exponential Moving Average (EMA)
alpha = 0.01  # Adjust for how much decay you want
df_smooth['ema'] = df_smooth['reputation_delta'].ewm(alpha=alpha).mean()

# Step 3: Plot the original and EMA values
plt.figure(figsize=(10, 6))
# Change the first plot to show dots instead of a line
#plt.plot(df_filtered['reputation_delta'], 'o', label='Reputation Delta No Outliers', alpha=0.5)
plt.plot(df_smooth['reputation_delta'], 'o', label='Reputation Delta No Outliers', alpha=0.7)
plt.plot(df_smooth['ema'], label='Exponential Moving Average', linewidth=2)

# Add a red line at y = 0
plt.axhline(0, color='red', linewidth=2, linestyle='--', label='Zero Line')

plt.title('Reputation Delta with Moving Decaying Average')
plt.xlabel('Index')
plt.ylabel('Reputation Delta')
plt.legend()

output_dir = os.path.dirname(file_path)
file_name = os.path.basename(file_path).rsplit('.', 1)[0]  # Remove extension
output_path = os.path.join(output_dir, f"{file_name}_reputation.png")
plt.savefig(output_path)

print(f"Graph saved to {output_path}")
