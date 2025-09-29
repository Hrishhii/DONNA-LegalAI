import React, { useState, useEffect } from 'react';
import { 
  Upload, 
  FileText, 
  MessageSquare, 
  Send, 
  Loader2, 
  CheckCircle, 
  Copy,
  Newspaper,
  ExternalLink,
  Calendar,
  ChevronRight,
  ChevronLeft,
  X
} from 'lucide-react';
import axios from 'axios';
import LandingPage from './LandingPage';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [showDashboard, setShowDashboard] = useState(true);
  const [currentTab, setCurrentTab] = useState('upload');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [summary, setSummary] = useState('');
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [question, setQuestion] = useState('');
  const [conversation, setConversation] = useState([]);
  const [isAsking, setIsAsking] = useState(false);
  const [legalNews, setLegalNews] = useState([]);
  const [isLoadingNews, setIsLoadingNews] = useState(false);
  const [isNewsPanelOpen, setIsNewsPanelOpen] = useState(false);
  const [isCopied, setIsCopied] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);
  const [isMarkedLoaded, setIsMarkedLoaded] = useState(false);

  useEffect(() => {
    // Dynamically load the 'marked' library
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    script.onload = () => {
      console.log('Marked library loaded.');
      setIsMarkedLoaded(true);
    };
    script.onerror = () => {
      console.error('Failed to load marked library.');
    };
    document.head.appendChild(script);

    if (!showDashboard) {
      fetchLegalNews();
    }
  }, [showDashboard]);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileUpload({ target: { files: [file] } });
    }
  };

  const handleGetStarted = () => {
    setShowDashboard(false);
  };

  const fetchLegalNews = async () => {
    setIsLoadingNews(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/legal-news`);
      setLegalNews(response.data.articles);
    } catch (error) {
      console.error('Error fetching news:', error);
    } finally {
      setIsLoadingNews(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsUploading(true);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setUploadedFile(file);
      setShowSuccessMessage(true);
      setTimeout(() => setShowSuccessMessage(false), 3000);
    } catch (error) {
      console.error('Upload error:', error);
      // alert('Error uploading file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSummarize = async () => {
    if (!uploadedFile) return;

    setIsSummarizing(true);
    
    try {
      // No FormData needed for the new backend
      const response = await axios.post(`${API_BASE_URL}/summarize`);
      setSummary(response.data.summary);
      setCurrentTab('summary');
    } catch (error) {
      console.error('Summarization error:', error);
    } finally {
      setIsSummarizing(false);
    }
  };

  const handleAskQuestion = async () => {
    if (!uploadedFile || !question.trim()) return;

    setIsAsking(true);
    
    const formData = new FormData();
    formData.append('question', question);

    try {
      const response = await axios.post(`${API_BASE_URL}/ask-query`, formData);
      
      const newConversation = [
        ...conversation,
        {
          type: 'question',
          content: question,
          timestamp: new Date().toLocaleTimeString()
        },
        {
          type: 'answer',
          content: response.data.answer,
          timestamp: new Date().toLocaleTimeString()
        }
      ];
      
      setConversation(newConversation);
      setQuestion('');
    } catch (error) {
      console.error('Query error:', error);
      // alert('Error processing question. Please try again.');
    } finally {
      setIsAsking(false);
    }
  };

  const handleCopySummary = () => {
    navigator.clipboard.writeText(summary)
      .then(() => {
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
      })
      .catch((err) => {
        console.error('Failed to copy text: ', err);
      });
  };

  if (showDashboard) {
    return <LandingPage onGetStarted={handleGetStarted} />;
  }

  const TabButton = ({ id, icon: Icon, label, isActive, onClick }) => (
    <button
      onClick={onClick}
      className={`tab-button ${isActive ? 'active' : ''}`}
    >
      <Icon size={18} />
      <span>{label}</span>
    </button>
  );

  return (
    <div className={`app ${isNewsPanelOpen ? 'news-panel-open' : ''}`}>
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <FileText size={28} />
            <h1>DONNA</h1>
          </div>
          <div className="header-actions">
            <button 
              className="news-toggle-button"
              onClick={() => setIsNewsPanelOpen(!isNewsPanelOpen)}
            >
              {isNewsPanelOpen ? <ChevronRight size={24} /> : <Newspaper size={24} />}
            </button>
            <button 
              className="back-to-dashboard"
              onClick={() => setShowDashboard(true)}
            >
              <ChevronLeft size={16} />
              Back to Dashboard
            </button>
          </div>
        </div>
      </header>

      {showSuccessMessage && (
        <div className="floating-message success">
          <CheckCircle size={20} />
          <span>File uploaded successfully!</span>
        </div>
      )}

      <div className="main-container">
        <nav className="sidebar">
          <TabButton
            id="upload"
            icon={Upload}
            label="Upload PDF"
            isActive={currentTab === 'upload'}
            onClick={() => setCurrentTab('upload')}
          />
          <TabButton
            id="summary"
            icon={FileText}
            label="Summary"
            isActive={currentTab === 'summary'}
            onClick={() => setCurrentTab('summary')}
          />
          <TabButton
            id="qa"
            icon={MessageSquare}
            label="Q&A Chat"
            isActive={currentTab === 'qa'}
            onClick={() => setCurrentTab('qa')}
          />
        </nav>

        <main className="content">
          {currentTab === 'upload' && (
            <div className="tab-content">
              <div className="upload-section">
                <h2>Upload Legal Document</h2>
                <p>Upload a PDF document to analyze, summarize, and query.</p>
                
                <div 
                  className={`upload-area ${isDragOver ? 'drag-over' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileUpload}
                    disabled={isUploading}
                    id="file-upload"
                    className="file-input"
                  />
                  <label htmlFor="file-upload" className="upload-label">
                    {isUploading ? (
                      <Loader2 className="animate-spin" size={24} />
                    ) : (
                      <Upload size={24} />
                    )}
                    <span>
                      {isUploading
                        ? 'Uploading...'
                        : 'Click or drop PDF file here'}
                    </span>
                  </label>
                  {isUploading && (
                    <div className="upload-progress-container">
                      <div className="upload-progress-bar"></div>
                    </div>
                  )}
                </div>
                
                {uploadedFile && (
                  <div className="uploaded-file-card">
                    <div className="file-icon">
                      <FileText size={32} />
                    </div>
                    <div className="file-info">
                      <h4>{uploadedFile.name}</h4>
                      <p>{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                      <span className="file-status">Ready for analysis</span>
                    </div>
                    <button 
                      className="remove-file-button"
                      onClick={() => {
                        setUploadedFile(null);
                        setSummary('');
                        setConversation([]);
                        setCurrentTab('upload');
                      }}
                      title="Remove file"
                    >
                      <X size={18} />
                    </button>
                  </div>
                )}

                {uploadedFile && (
                  <div className="action-buttons">
                    <button
                      onClick={handleSummarize}
                      disabled={isSummarizing}
                      className="primary-button"
                    >
                      {isSummarizing ? (
                        <Loader2 className="animate-spin" size={16} />
                      ) : (
                        <FileText size={16} />
                      )}
                      {isSummarizing ? 'Summarizing...' : 'Generate Summary'}
                    </button>
                    
                    <button
                      onClick={() => setCurrentTab('qa')}
                      className="secondary-button"
                    >
                      <MessageSquare size={16} />
                      Start Q&A Chat
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {currentTab === 'summary' && (
            <div className="tab-content">
              <div className="summary-section">
                <div className="summary-panel">
                  <div className="summary-panel-header">
                    <h2>Document Summary</h2>
                    <button 
                      onClick={handleCopySummary}
                      className="copy-button"
                    >
                      <Copy size={16} />
                      <span className="copy-text">{isCopied ? 'Copied!' : 'Copy'}</span>
                    </button>
                  </div>
                  {summary ? (
                    <div className="summary-content" dangerouslySetInnerHTML={{ __html: isMarkedLoaded ? window.marked.parse(summary) : '' }}></div>
                  ) : (
                    <div className="empty-state">
                      <FileText size={48} />
                      <p>No summary generated yet.</p>
                      <p>Upload a PDF and generate a summary to see content here.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {currentTab === 'qa' && (
            <div className="tab-content">
              <div className="qa-section">
                <h2>Q&A Chat</h2>
                
                {!uploadedFile ? (
                  <div className="empty-state">
                    <MessageSquare size={48} />
                    <p>Upload a PDF first to start asking questions.</p>
                  </div>
                ) : (
                  <>
                    <div className="chat-container">
                      {conversation.length === 0 ? (
                        <div className="chat-empty">
                          <p>Ask questions about your uploaded document.</p>
                        </div>
                      ) : (
                        <div className="chat-messages">
                          {conversation.map((message, index) => (
                            <div
                              key={index}
                              className={`message ${message.type}`}
                            >
                              <div className="message-content">
                                {message.content}
                              </div>
                              <div className="message-timestamp">
                                {message.timestamp}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                    <div className="chat-input">
                      <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="Ask a question about your document..."
                        onKeyPress={(e) => {
                          if (e.key === 'Enter' && !isAsking) {
                            handleAskQuestion();
                          }
                        }}
                        disabled={isAsking}
                      />
                      <button
                        onClick={handleAskQuestion}
                        disabled={!question.trim() || isAsking}
                        className="send-button"
                      >
                        {isAsking ? (
                          <Loader2 className="animate-spin" size={16} />
                        ) : (
                          <Send size={16} />
                        )}
                      </button>
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
        </main>
        
        <aside className={`news-panel ${isNewsPanelOpen ? 'open' : ''}`}>
          <div className="news-panel-header">
            <h3>Legal News</h3>
            <button onClick={fetchLegalNews} className="refresh-button">
              {isLoadingNews ? (
                <Loader2 className="animate-spin" size={16} />
              ) : (
                'Refresh'
              )}
            </button>
          </div>
          
          <div className="news-panel-content">
            {isLoadingNews ? (
              <div className="loading-state">
                <Loader2 className="animate-spin" size={32} />
                <p>Loading legal news...</p>
              </div>
            ) : legalNews.length > 0 ? (
              <div className="news-grid">
                {legalNews.map((article, index) => (
                  <div key={index} className="news-card">
                    <h3>{article.title}</h3>
                    <p className="news-description">{article.description}</p>
                    <div className="news-meta">
                      <div className="news-source">
                        <span>{article.source}</span>
                      </div>
                      <div className="news-date">
                        <Calendar size={14} />
                        <span>{article.publishedAtFormatted}</span>
                      </div>
                    </div>
                    <a
                      href={article.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="news-link"
                    >
                      Read Full Article
                      <ExternalLink size={14} />
                    </a>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <Newspaper size={48} />
                <p>No legal news available at the moment.</p>
              </div>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}

export default App;
