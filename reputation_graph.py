import sys
import pandas as pd
import matplotlib.pyplot as plt
import os

if len(sys.argv) != 3:
    print("Usage: python reputation_graph.py <file> <channel_id>")
    sys.exit(1)

file_path = sys.argv[1]
channel_id = int(sys.argv[2])

# Load CSV data
df = pd.read_csv(file_path)

# Filter for the specified outgoing channel ID
df_filtered = df[df['outgoing_channel_id'] == channel_id]

if df_filtered.empty:
    print(f"No data found for outgoing channel ID {channel_id}")
    sys.exit(1)

# Compute the y-values for the graph
reputation_delta = df_filtered['incoming_revenue'] - df_filtered['outgoing_reputation'] - df_filtered['in_flight_risk'] - df_filtered['htlc_risk']

# Outlier detection using IQR (Interquartile Range)
Q1 = reputation_delta.quantile(0.25)
Q3 = reputation_delta.quantile(0.75)
IQR = Q3 - Q1

# Remove outliers beyond 1.5 * IQR
reputation_delta_clean = reputation_delta[(reputation_delta >= (Q1 - 1.5 * IQR)) & (reputation_delta <= (Q3 + 1.5 * IQR))]

# Generate x-axis values (assuming each row is one second apart)
x_values = range(len(reputation_delta_clean))

# Plot the data with a thinner line
plt.figure(figsize=(10, 5))
plt.plot(x_values, reputation_delta_clean, label='Reputation', color='blue', linewidth=1)  # Thin line

# Set Y-axis limits: lower bound is capped at -1e9, upper bound based on the cleaned data range
y_min = min(reputation_delta_clean)
y_max = max(reputation_delta_clean)
y_padding = (y_max - y_min) * 0.1  # 10% padding on the upper bound

# Set the minimum Y value to -1e9, and let the upper bound adjust dynamically
plt.ylim(max(y_min, -1e9), y_max + y_padding)

plt.xlabel("Transaction Count")
plt.ylabel("Value")
plt.title(f"Reputation Graph for Channel {channel_id}")
plt.legend()
plt.grid()

# Save the graph in the same directory as the input file
output_dir = os.path.dirname(file_path)
file_name = os.path.basename(file_path).rsplit('.', 1)[0]  # Remove extension
output_path = os.path.join(output_dir, f"{file_name}_reputation.png")
plt.savefig(output_path)

print(f"Graph saved to {output_path}")
