import React, { useState, useRef } from 'react';
import { Upload, Leaf, Loader2, RefreshCw, CheckCircle, Activity } from 'lucide-react';

const Recognition = ({ apiKey }) => {
  const [step, setStep] = useState(1); // 1: Upload, 2: Analyze, 3: Results
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      processFile(droppedFile);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (selectedFile) => {
    if (!selectedFile.type.match('image.*')) {
      setError("Please upload an image file (JPG, PNG).");
      return;
    }
    
    // Check file size (max 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError("File size should be less than 10MB.");
      return;
    }

    setFile(selectedFile);
    setError(null);
    
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
      setStep(2); // Move to Analyze step
    };
    reader.readAsDataURL(selectedFile);
  };

  // Removed Gemini AIAssessment function

  const handleAnalyze = async () => {
    if (!file) return;
    
    setStep(2);
    setError(null);
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      // Connect to FastAPI Backend
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000/predict";
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error("Failed to get prediction from server.");
      }
      
      const data = await response.json();
      setResult(data);
      setStep(3); // Move to Results
      
      // AI function removed
      
    } catch (err) {
      setError(err.message || "An error occurred during analysis.");
      setStep(1);
    }
  };

  const handleReset = () => {
    setStep(1);
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  // Helper to safely render markdown-like bolded text from gemini
  const renderMarkdown = (text) => {
    // Very simple inline markdown parser for bold and lists
    if (!text) return null;
    const parts = text.split('\n');
    
    return parts.map((part, idx) => {
      if (part.startsWith('* ') || part.startsWith('- ')) {
        const content = part.substring(2).split('**');
        return (
          <li key={idx}>
            {content.map((c, i) => i % 2 === 1 ? <strong key={i}>{c}</strong> : c)}
          </li>
        );
      } else if (part.match(/^\d+\./)) { // Numbered lists
         const content = part.substring(part.indexOf('.') + 1).trim().split('**');
         return (
          <li key={idx} style={{listStyleType: 'decimal', marginLeft: '1rem'}}>
             {content.map((c, i) => i % 2 === 1 ? <strong key={i}>{c}</strong> : c)}
          </li>
         )
      } else if (part.trim() === '') {
        return <br key={idx} />;
      } else {
        const content = part.split('**');
        return (
          <p key={idx}>
            {content.map((c, i) => i % 2 === 1 ? <strong key={i}>{c}</strong> : c)}
          </p>
        );
      }
    });
  };

  return (
    <div className="recognition-container">
      <div className="recognition-header">
        <div className="icon-container">
          <Leaf size={40} />
        </div>
        <h1>Plant Disease Recognition</h1>
        <p>Upload a leaf image to detect diseases instantly</p>
      </div>

      {/* Custom Stepper */}
      <div className="stepper">
        <div className={`step-wrapper ${step >= 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
          <div className="step-indicator">1</div>
          <span className="step-label" style={{marginTop: '0.5rem'}}>Upload</span>
        </div>
        <div className={`step-divider ${step >= 2 ? 'active' : ''}`}></div>
        
        <div className={`step-wrapper ${step >= 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
          <div className="step-indicator">2</div>
          <span className="step-label" style={{marginTop: '0.5rem'}}>Analyze</span>
        </div>
        <div className={`step-divider ${step >= 3 ? 'active' : ''}`}></div>
        
        <div className={`step-wrapper ${step >= 3 ? 'active' : ''}`}>
          <div className="step-indicator">3</div>
          <span className="step-label" style={{marginTop: '0.5rem'}}>Results</span>
        </div>
      </div>

      {/* Step 1: Upload */}
      {step === 1 && (
        <div 
          className={`upload-zone ${isDragging ? 'drag-active' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <Leaf size={48} className="upload-icon" />
          <h3>Drop your leaf image here</h3>
          <p>JPG, PNG — up to 10MB</p>
          <button className="btn btn-secondary" style={{ marginTop: '1rem', pointerEvents: 'none' }}>
            Choose file
          </button>
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileInput} 
            accept="image/jpeg, image/png, image/jpg" 
            style={{ display: 'none' }} 
          />
          {error && <p style={{ color: 'var(--danger)', marginTop: '1rem' }}>{error}</p>}
        </div>
      )}

      {/* Step 2: Analyze Preview */}
      {step === 2 && preview && (
        <div className="card" style={{ textAlign: 'center', maxWidth: '500px', margin: '0 auto' }}>
          <img src={preview} alt="Upload preview" style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: 'var(--radius-md)', marginBottom: '1.5rem', objectFit: 'contain' }} />
          
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <button className="btn btn-secondary" onClick={handleReset}>Cancel</button>
            <button className="btn btn-primary" onClick={handleAnalyze}>
              {<Loader2 size={18} className="spinner" style={{ display: 'none' }} />} {/* Add spinner manually via state if needed */}
              Analyze Image
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Results */}
      {step === 3 && result && (
         <div className="result-container">
            <div className={`result-card`}>
              <div className={`result-header ${result.is_healthy ? 'healthy' : 'disease'}`}>
                <div className="result-title">
                  {result.is_healthy ? <CheckCircle size={32} color="var(--success)" /> : <Activity size={32} color="var(--danger)" />}
                  <h2>{result.disease_name}</h2>
                </div>
                <div className="confidence-badge">
                  Confidence: {result.confidence.toFixed(2)}%
                </div>
              </div>
              
              <div className="result-body">
                <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
                  <div style={{ flex: '1', minWidth: '250px' }}>
                     <img src={preview} alt="Analyzed" style={{ width: '100%', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }} />
                  </div>
                  
                  <div style={{ flex: '2', minWidth: '300px' }}>
                    <div className="ai-analytics" style={{ marginTop: 0, paddingTop: 0, borderTop: 'none' }}>
                      <div className="ai-header">
                        {result.is_healthy ? <Leaf size={24} /> : <Activity size={24} />}
                        Disease Details
                      </div>
                      
                      <div className="ai-content">
                        <div>
                          <p style={{marginBottom: "1rem"}}><strong>Description:</strong> {result.description}</p>
                          <p><strong>Recommended Action:</strong> {result.remedy}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '2rem', borderTop: '1px solid var(--border)', paddingTop: '1.5rem' }}>
                   <button className="btn btn-secondary" onClick={handleReset}>
                      <RefreshCw size={18} />
                      Analyze Another Image
                   </button>
                </div>
              </div>
            </div>
         </div>
      )}
    </div>
  );
};

export default Recognition;
