import React from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Activity, CheckCircle, Info, Stethoscope, Droplet } from 'lucide-react';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <h1>Plant Disease Recognition</h1>
        <p>Automatically identify plant leaf diseases from images using deep learning — helping farmers take quick, informed action for healthier crops.</p>
        <button className="btn btn-primary" style={{ marginTop: '2rem', backgroundColor: 'white', color: 'var(--primary)' }} onClick={() => navigate('/recognition')}>
          Try it now
        </button>
      </section>

      {/* Stats Grid */}
      <section className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon"><Activity size={24} /></div>
          <div className="stat-info">
            <p>Model type</p>
            <h3>CNN</h3>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><CheckCircle size={24} /></div>
          <div className="stat-info">
            <p>Framework</p>
            <h3>Keras</h3>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon"><UploadCloud size={24} /></div>
          <div className="stat-info">
            <p>Interface</p>
            <h3>React + Vite</h3>
          </div>
        </div>
      </section>

      <div className="section-container">
        <h2 className="section-title">Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon-wrapper"><UploadCloud size={24} /></div>
            <div className="feature-content">
              <h3>Image upload</h3>
              <p>Upload any plant leaf photo directly from your device securely and quickly.</p>
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrapper"><Activity size={24} /></div>
            <div className="feature-content">
              <h3>Disease prediction</h3>
              <p>CNN model identifies the specific disease with high accuracy instantly.</p>
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrapper"><CheckCircle size={24} /></div>
            <div className="feature-content">
              <h3>Confidence score</h3>
              <p>See exactly how certain the AI model is about its prediction.</p>
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrapper"><Info size={24} /></div>
            <div className="feature-content">
              <h3>Disease info</h3>
              <p>Get detailed descriptions dynamically generated about the detected condition.</p>
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrapper"><Stethoscope size={24} /></div>
            <div className="feature-content">
              <h3>Remedy guide</h3>
              <p>Actionable treatment and prevention recommendations linked directly to the disease.</p>
            </div>
          </div>
          <div className="feature-card">
            <div className="feature-icon-wrapper"><Droplet size={24} /></div>
            <div className="feature-content">
              <h3>Simple UI</h3>
              <p>A clean, user-friendly interface designed for users of all skill levels.</p>
            </div>
          </div>
        </div>

        <h2 className="section-title" style={{ marginTop: '4rem' }}>How to Use</h2>
        <div className="steps-container">
          {[
            { title: 'Navigate to Recognition Page', desc: 'Click on Disease Recognition in the navbar.' },
            { title: 'Upload a clear leaf image', desc: 'Use a well-lit, focused photo for best results. Supported formats: JPG, PNG.' },
            { title: 'Click Analyze', desc: 'The Deep Learning model processes the leaf and predicts the disease.' },
            { title: 'View Diagnostics', desc: 'Read the detailed descriptions, confidence score, and remedies to heal your plant.' }
          ].map((step, idx) => (
            <div className="step-item" key={idx}>
              <div className="step-number">{idx + 1}</div>
              <div className="step-content">
                <h3>{step.title}</h3>
                <p>{step.desc}</p>
              </div>
            </div>
          ))}
        </div>

        <h2 className="section-title" style={{ marginTop: '4rem' }}>Technologies Used</h2>
        <div className="tags-list">
          {['Python', 'TensorFlow', 'Keras', 'NumPy', 'React', 'FastAPI', 'CNN'].map((tag, idx) => (
            <div className="tag" key={idx}>
              <div className="dot" style={{ backgroundColor: `hsl(${idx * 40}, 70%, 50%)` }}></div>
              {tag}
            </div>
          ))}
        </div>

        <div className="callout-banner">
          <Info size={24} color="var(--primary)" />
          <p>For best accuracy, upload a clear and properly visible leaf image with good lighting. Avoid blurry or heavily shadowed photos.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
