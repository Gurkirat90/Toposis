from flask import Flask, render_template, request, send_file
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import io

app = Flask(__name__)

# --- TOPSIS LOGIC ---
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

# --- EMAIL LOGIC ---
def send_email(to_email, result_df):
    from_email = "your-email@gmail.com"   # <--- REPLACE THIS
    password = "your-app-password"        # <--- REPLACE THIS (Google App Password)
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Your TOPSIS Result File"
    
    body = "Hello,\n\nPlease find attached the result file with Topsis Scores and Ranks.\n\nRegards,\nTopsis Web Service"
    msg.attach(MIMEText(body, 'plain'))
    
    # Convert DF to CSV in memory
    buffer = io.StringIO()
    result_df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    part = MIMEBase('application', "octet-stream")
    part.set_payload(buffer.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="result.csv"')
    msg.attach(part)
    
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(from_email, password)
        s.sendmail(from_email, to_email, msg.as_string())
        s.quit()
        return True
    except Exception as e:
        print("Email Error:", e)
        return False

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # 1. Get Form Data
            file = request.files['file']
            weights_str = request.form['weights']
            impacts_str = request.form['impacts']
            email_id = request.form['email']
            
            if not file or not weights_str or not impacts_str or not email_id:
                return render_template('index.html', message="Error: All fields are required.")

            # 2. Process Data
            df = pd.read_csv(file)
            weights = [float(w) for w in weights_str.split(',')]
            impacts = impacts_str.split(',')
            
            # 3. Run Topsis
            result_df, error = calculate_topsis(df, weights, impacts)
            
            if error:
                return render_template('index.html', message=error)
            
            # 4. Send Email
            success = send_email(email_id, result_df)
            
            if success:
                return render_template('index.html', message=f"Success! Result sent to {email_id}")
            else:
                return render_template('index.html', message="Error: Could not send email. Check server logs.")
                
        except Exception as e:
            return render_template('index.html', message=f"Error: {str(e)}")
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
