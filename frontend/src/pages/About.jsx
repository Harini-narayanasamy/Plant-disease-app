import React from 'react';

const About = () => {
  return (
    <div className="section-container" style={{ maxWidth: '800px' }}>
      <div className="card" style={{ padding: '3rem' }}>
        <h1 style={{ fontSize: '2rem', marginBottom: '1.5rem', color: 'var(--primary)' }}>ℹ️ About This Project</h1>
        
        <p style={{ fontSize: '1.125rem', marginBottom: '2rem', color: 'var(--text-muted)' }}>
          This project utilizes a <strong>Convolutional Neural Network (CNN)</strong> to accurately detect plant leaf diseases from user-uploaded images, providing instant diagnostics and AI-powered treatment plans.
        </p>

        <h3 style={{ marginBottom: '1rem' }}>🔄 Project Workflow</h3>
        <ol style={{ paddingLeft: '1.5rem', marginBottom: '2rem', color: 'var(--text-muted)' }}>
           <li style={{ marginBottom: '0.5rem' }}>User uploads a high-quality plant leaf image</li>
           <li style={{ marginBottom: '0.5rem' }}>The React frontend sends the image to our FastAPI backend</li>
           <li style={{ marginBottom: '0.5rem' }}>The image is resized and processed by a trained CNN model</li>
           <li style={{ marginBottom: '0.5rem' }}>The predicted disease class and confidence score are calculated</li>
           <li style={{ marginBottom: '0.5rem' }}>The classification is passed to Google Gemini to generate a tailored remedy guide</li>
           <li style={{ marginBottom: '0.5rem' }}>Rich results are presented dynamically to the user</li>
        </ol>

        <h3 style={{ marginBottom: '1rem' }}>🌾 Applications</h3>
        <ul style={{ paddingLeft: '1.5rem', marginBottom: '2rem', color: 'var(--text-muted)' }}>
           <li style={{ marginBottom: '0.5rem' }}>Early disease detection in crops to prevent spreading</li>
           <li style={{ marginBottom: '0.5rem' }}>Helps farmers take quick, preventive action</li>
           <li style={{ marginBottom: '0.5rem' }}>Reduces overall crop loss and maximizes yield</li>
           <li style={{ marginBottom: '0.5rem' }}>Supports modern smart agriculture solutions</li>
           <li style={{ marginBottom: '0.5rem' }}>Educational tool for botany and agricultural students</li>
        </ul>
      </div>
    </div>
  );
};

export default About;
