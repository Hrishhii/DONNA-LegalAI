import React, { useState, useEffect, useRef } from 'react';
import { 
  FileText, 
  Brain, 
  MessageSquare, 
  Newspaper,
  ArrowRight,
  Mail,
  Github,
  Linkedin,
  Shield,
  Zap,
  Clock,
  ChevronDown,
  Send,
  CheckCircle,
  Cpu,
  Server,
  Eye
} from 'lucide-react';
import './LandingPage.css';

const LandingPage = ({ onGetStarted }) => {
  const [scrollY, setScrollY] = useState(0);
  const [isVisible, setIsVisible] = useState({});
  const [contactForm, setContactForm] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const observerRef = useRef();

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    // Intersection Observer for scroll animations
    observerRef.current = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(prev => ({
              ...prev,
              [entry.target.id]: true
            }));
          }
        });
      },
      { threshold: 0.1 }
    );

    // Observe all sections
    const sections = document.querySelectorAll('[data-scroll-animate]');
    sections.forEach(section => {
      if (observerRef.current) {
        observerRef.current.observe(section);
      }
    });

    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, []);

  const handleContactSubmit = (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSubmitted(true);
      setContactForm({ name: '', email: '', message: '' });
      
      setTimeout(() => {
        setIsSubmitted(false);
      }, 3000);
    }, 1500);
  };

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({
      behavior: 'smooth'
    });
  };

  return (
    <div className="landing-page">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <a className="logo-text" href="#hero">
              DONNA<sup className="trademark">®</sup>
            </a>
          </div>
          <nav className="nav-links">
            <a href="#features" className="nav-item">Features</a>
            <a href="#technology" className="nav-item">Technology</a>
            <a href="#how-it-works" className="nav-item">How It Works</a>
            <a href="#contact" className="nav-item">Contact</a>
          </nav>
        </div>
      </header>


      {/* Hero Section */}
      <section className="hero-section" id="hero">
        <div className="hero-content">
          <div 
            className="hero-text"
            style={{ transform: `translateY(${scrollY * 0.2}px)` }}
          >
            <h1 className="hero-title">DONNA</h1>
            <p className="hero-subtitle">AI Assistant for Legal Excellence</p>
            <p className="hero-description">
              Transform complex legal documents into crystal-clear insights using cutting-edge AI. 
              Experience the future of legal document analysis.
            </p>
            <div className="hero-buttons">
              <button className="get-started-button" onClick={onGetStarted}>
                <span>Get Started</span>
                <ArrowRight size={20} />
              </button>
            </div>
          </div>
        </div>
        
        <div 
          className="scroll-indicator"
          onClick={() => scrollToSection('features')}
          style={{ opacity: Math.max(0, 1 - scrollY / 500) }}
        >
          <ChevronDown size={24} />
          <span>Discover More</span>
        </div>
      </section>

      {/* Features Section */}
      <section 
        id="features" 
        className="features-section"
        data-scroll-animate
      >
        <div className="container">
          <div className={`section-header ${isVisible.features ? 'animate-in' : ''}`}>
            <h2 className="section-title">Powerful Features</h2>
            <p className="section-subtitle">Everything you need to work with legal documents efficiently</p>
          </div>
          
          <div className="features-grid">
            {[
              {
                icon: Brain,
                title: "AI Document Summarization",
                description: "Get intelligent summaries of complex legal documents in seconds using Google's Gemini 2.0 Flash model. Our advanced AI understands legal context and extracts key information.",
                delay: 0
              },
              {
                icon: MessageSquare,
                title: "Interactive Q&A",
                description: "Ask questions about your documents and get instant, accurate answers powered by Groq's Llama 3.1 8B model. Chat with your legal documents like never before.",
                delay: 200
              },
              {
                icon: Newspaper,
                title: "Legal News Feed",
                description: "Stay updated with the latest legal developments and court rulings. Never miss important legal news that could impact your work.",
                delay: 400
              },
              {
                icon: Shield,
                title: "Secure Processing",
                description: "Your documents are processed with enterprise-level security. We prioritize confidentiality and data protection for all legal materials.",
                delay: 600
              }
            ].map((feature, index) => (
              <div 
                key={index}
                className={`feature-card ${isVisible.features ? 'animate-in' : ''}`}
                style={{ animationDelay: `${feature.delay}ms` }}
              >
                <div className="feature-icon">
                  <feature.icon size={32} />
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section 
        id="technology"
        className="technology-section"
        data-scroll-animate
      >
        <div className="container">
          <div className={`section-header ${isVisible.technology ? 'animate-in' : ''}`}>
            <h2 className="section-title">Built with Advanced AI</h2>
            <p className="section-subtitle">Powered by cutting-edge language models and modern technology stack</p>
          </div>
          
          <div className="tech-grid">
            {[
              {
                icon: Brain,
                title: "Google Gemini 2.0 Flash",
                subtitle: "Summarization Engine",
                description: "Ultra-fast document processing with deep legal comprehension and contextual understanding."
              },
              {
                icon: Server,
                title: "Groq Llama 3.1 8B", 
                subtitle: "Q&A Intelligence",
                description: "Lightning-fast inference with high-quality reasoning and contextual document understanding."
              },
              {
                icon: Cpu,
                title: "Vector Embeddings",
                subtitle: "Semantic Search",
                description: "HuggingFace transformers with ChromaDB vector storage for intelligent document retrieval."
              }
            ].map((tech, index) => (
              <div 
                key={index}
                className={`tech-card ${isVisible.technology ? 'animate-in' : ''}`}
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <div className="tech-icon">
                  <tech.icon size={40} />
                </div>
                <div className="tech-content">
                  <h3>{tech.title}</h3>
                  <span className="tech-subtitle">{tech.subtitle}</span>
                  <p>{tech.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section 
        id="how-it-works"
        className="how-it-works-section"
        data-scroll-animate
      >
        <div className="container">
          <div className={`section-header ${isVisible['how-it-works'] ? 'animate-in' : ''}`}>
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">Three simple steps to AI-powered insights</p>
          </div>
          
          <div className="workflow-steps">
            {[
              {
                step: "01",
                title: "Upload & Process",
                description: "Drag and drop your legal document. Our AI instantly begins analysis with advanced OCR and text extraction.",
                icon: FileText
              },
              {
                step: "02", 
                title: "AI Analysis",
                description: "Gemini and Llama models work in parallel to understand context, extract key information, and build knowledge graphs.",
                icon: Brain
              },
              {
                step: "03",
                title: "Interactive Insights",
                description: "Get instant summaries, ask complex questions, and explore your document like never before with conversational AI.",
                icon: MessageSquare
              }
            ].map((item, index) => (
              <div 
                key={index}
                className={`workflow-step ${isVisible['how-it-works'] ? 'animate-in' : ''}`}
                style={{ animationDelay: `${index * 300}ms` }}
              >
                <div className="step-number">{item.step}</div>
                <div className="step-content">
                  <div className="step-icon">
                    <item.icon size={32} />
                  </div>
                  <h3>{item.title}</h3>
                  <p>{item.description}</p>
                </div>
              </div>
            ))}
          </div>

          <div className={`stats-section ${isVisible['how-it-works'] ? 'animate-in' : ''}`}>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-number">24/7</span>
                <span className="stat-label">AI Availability</span>
              </div>
              <div className="stat-item">
                <span className="stat-number">&lt; 15s</span>
                <span className="stat-label">Processing Time</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section 
        id="contact" 
        className="contact-section"
        data-scroll-animate
      >
        <div className="container">
          <div className={`contact-content ${isVisible.contact ? 'animate-in' : ''}`}>
            <div className="contact-info">
              <h2 className="contact-title">Get In Touch</h2>
              <p className="contact-description">
                Ready to transform your legal workflow? Connect with us to learn more 
                about DONNA's capabilities or contribute to the project.
              </p>
              
              <div className="contact-methods">
                {[
                  { icon: Mail, label: "Email", value: "hrishi720kesh@gmail.com", href: "mailto:hrishi720kesh@gmail.com" },
                  { icon: Github, label: "GitHub", value:"", href: "https://github.com/Hrishhii" },
                  { icon: Linkedin, label: "LinkedIn", value: "", href: "https://linkedin.com/in/hrishikesh raparthi" }
                ].map((contact, index) => (
                  <a 
                    key={index}
                    href={contact.href}
                    className="contact-method"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <div className="contact-icon">
                      <contact.icon size={24} />
                    </div>
                    <div className="contact-details">
                      <span className="contact-label">{contact.label}</span>
                      <span className="contact-value">{contact.value}</span>
                    </div>
                    <ArrowRight size={16} className="contact-arrow" />
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <span className="logo-text">DONNA<sup className="trademark">®</sup></span>
            <p>&copy; 2025 DONNA-LegalAI.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;