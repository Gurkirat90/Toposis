from flask import Flask, render_template, request
import pandas as pd
import numpy as np
# We removed the 'smtplib' and 'email' imports since we aren't using real email anymore
import io

app = Flask(__name__)

# --- 1. TOPSIS LOGIC (Same as before) ---
def calculate_topsis(df, weights, impacts):
    try:
        # Extract numeric data (assuming first col is non-numeric)
        data = df.iloc[:, 1:].values.astype(float)
        attributes = df.columns[1:]
        
        # Validation
        if len(weights) != len(attributes) or len(impacts) != len(attributes):
            return None, "Error: Count of weights/impacts must match numeric columns."
        
        # Normalization
        norm_data = data / np.sqrt((data**2).sum(axis=0))
        
        # Weighted Normalization
        weighted_data = norm_data * weights
        
        # Ideal Best & Worst
        ideal_best = []
        ideal_worst = []
        
        for i in range(len(attributes)):
            if impacts[i] == '+':
                ideal_best.append(max(weighted_data[:, i]))
                ideal_worst.append(min(weighted_data[:, i]))
            else:
                ideal_best.append(min(weighted_data[:, i]))
                ideal_worst.append(max(weighted_data[:, i]))
                
        # Euclidean Distances
        dist_best = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
        dist_worst = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
        
        # Score & Rank
        score = dist_worst / (dist_best + dist_worst)
        df['Topsis Score'] = score
        df['Rank'] = df['Topsis Score'].rank(ascending=False)
        
        return df, None
    except Exception as e:
        return None, str(e)

# --- 2. MOCK EMAIL FUNCTION ---
def send_email(to_email, result_df):
    # This function pretends to send an email so the code doesn't crash.
    # It prints to the server logs instead.
    print(f"--------------------------------------------------")
    print(f" [MOCK EMAIL] To: {to_email}")
    print(f" [CONTENT] Topsis Results Calculated Successfully.")
    print(f"--------------------------------------------------")
    return True # Always returns True to simulate success

# --- 3. ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get Form Data
            file = request.files['file']
            weights_str = request.form['weights']
            impacts_str = request.form['impacts']
            email_id = request.form['email'] # We still accept the email input
            
            if not file or not weights_str or not impacts_str or not email_id:
                return render_template('index.html', message="Error: All fields are required.")

            # Process Data
            df = pd.read_csv(file)
            weights = [float(w) for w in weights_str.split(',')]
            impacts = impacts_str.split(',')
            
            # Run Topsis
            result_df, error = calculate_topsis(df, weights, impacts)
            
            if error:
                return render_template('index.html', message=error)
            
            # Send (Mock) Email
            success = send_email(email_id, result_df)
            
            if success:
                return render_template('index.html', message=f"Success! Result sent to {email_id}")
            else:
                return render_template('index.html', message="Error: Could not send email.")
                
        except Exception as e:
            return render_template('index.html', message=f"Error: {str(e)}")
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
