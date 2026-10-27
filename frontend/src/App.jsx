import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // =========================
  // Chat State
  // =========================

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // =========================
  // Upload State
  // =========================

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");

  // =========================
  // Document State
  // =========================

  const [documents, setDocuments] = useState([]);
  const [loadingDocuments, setLoadingDocuments] = useState(false);
  const [deletingDocument, setDeletingDocument] = useState(null);

  // =========================
  // Load Documents
  // =========================

  const loadDocuments = async () => {
    setLoadingDocuments(true);

    try {
      const response = await fetch(`${API_URL}/documents`);

      if (!response.ok) {
        throw new Error("Failed to load documents.");
      }

      const data = await response.json();

      setDocuments(data);
    } catch (error) {
      console.error("Error loading documents:", error);
    } finally {
      setLoadingDocuments(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  // =========================
  // Clear Chat
  // =========================

  const clearChat = () => {
    setMessages([]);
  };

  // =========================
  // Ask Question
  // =========================

  const askQuestion = async () => {
    if (!question.trim() || loading) {
      return;
    }

    const userQuestion = question.trim();

    // Save conversation history BEFORE adding
    // the current question.
    const conversationHistory = messages.map((message) => ({
      role: message.role,
      content: message.content,
    }));

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
          conversation_history: conversationHistory,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get answer.");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, something went wrong while contacting StudyMate AI.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // Select PDF
  // =========================

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    if (file.type !== "application/pdf") {
      setSelectedFile(null);
      setUploadMessage("Please select a PDF file.");
      return;
    }

    setSelectedFile(file);
    setUploadMessage("");
  };

  // =========================
  // Upload PDF
  // =========================

  const uploadPDF = async () => {
    if (!selectedFile || uploading) {
      return;
    }

    setUploading(true);
    setUploadMessage("Uploading and indexing PDF...");

    const formData = new FormData();

    formData.append("file", selectedFile);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to upload PDF."
        );
      }

      setUploadMessage(
        `Successfully uploaded "${data.filename}" and indexed ${data.total_chunks} chunks.`
      );

      setSelectedFile(null);

      const fileInput = document.getElementById("pdf-upload");

      if (fileInput) {
        fileInput.value = "";
      }

      await loadDocuments();
    } catch (error) {
      console.error(error);

      setUploadMessage(
        error.message ||
          "Something went wrong while uploading."
      );
    } finally {
      setUploading(false);
    }
  };

  // =========================
  // Delete Document
  // =========================

  const deleteDocument = async (filename) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete "${filename}"?`
    );

    if (!confirmed) {
      return;
    }

    setDeletingDocument(filename);

    try {
      const response = await fetch(
        `${API_URL}/documents/${encodeURIComponent(filename)}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to delete document."
        );
      }

      setDocuments((previous) =>
        previous.filter(
          (document) =>
            document.filename !== filename
        )
      );

      setUploadMessage(
        `"${filename}" was deleted successfully.`
      );
    } catch (error) {
      console.error(error);

      setUploadMessage(
        error.message ||
          "Something went wrong while deleting the document."
      );
    } finally {
      setDeletingDocument(null);
    }
  };

  // =========================
  // Render
  // =========================

  return (
    <div className="app">

      {/* =========================
          Fixed Header
      ========================= */}

      <header className="header">

        <div className="header-content">
          <h1>StudyMate AI</h1>

          <p>Your AI Study Assistant</p>
        </div>

      </header>

      {/* =========================
          Main
      ========================= */}

      <main className="chat-container">

        {/* =========================
            Study Materials
        ========================= */}

        <section className="documents-section">

          <div className="section-header">

            <div>
              <h2>📚 My Study Materials</h2>

              <p>
                Manage the lecture PDFs used by
                StudyMate AI.
              </p>
            </div>

            <span className="document-count">
              {documents.length}{" "}
              {documents.length === 1
                ? "document"
                : "documents"}
            </span>

          </div>

          {/* Loading */}

          {loadingDocuments && (
            <div className="documents-loading">
              Loading documents...
            </div>
          )}

          {/* Empty */}

          {!loadingDocuments &&
            documents.length === 0 && (
              <div className="empty-documents">

                <div className="empty-icon">
                  📄
                </div>

                <h3>
                  No study materials yet
                </h3>

                <p>
                  Upload a PDF lecture below to
                  start studying.
                </p>

              </div>
            )}

          {/* Document List */}

          {!loadingDocuments &&
            documents.length > 0 && (
              <div className="document-list">

                {documents.map((document) => (
                  <div
                    key={document.filename}
                    className="document-card"
                  >

                    <div className="document-info">

                      <div className="document-icon">
                        📄
                      </div>

                      <div className="document-details">

                        <div className="document-name">
                          {document.filename}
                        </div>

                        <div className="document-meta">
                          {document.total_chunks}{" "}
                          {document.total_chunks === 1
                            ? "chunk"
                            : "chunks"}
                        </div>

                      </div>

                    </div>

                    <button
                      className="delete-button"
                      onClick={() =>
                        deleteDocument(
                          document.filename
                        )
                      }
                      disabled={
                        deletingDocument ===
                        document.filename
                      }
                    >
                      {deletingDocument ===
                      document.filename
                        ? "Deleting..."
                        : "Delete"}
                    </button>

                  </div>
                ))}

              </div>
            )}

        </section>

        {/* =========================
            Upload Section
        ========================= */}

        <section className="upload-section">

          <div className="upload-header">

            <h2>Upload New PDF</h2>

            <p>
              Add a new lecture to your StudyMate
              knowledge base.
            </p>

          </div>

          <div className="upload-controls">

            <input
              id="pdf-upload"
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
            />

            <button
              className="upload-button"
              onClick={uploadPDF}
              disabled={
                !selectedFile || uploading
              }
            >
              {uploading
                ? "Uploading..."
                : "Upload PDF"}
            </button>

          </div>

          {selectedFile && (
            <div className="selected-file">
              Selected:{" "}
              <strong>
                {selectedFile.name}
              </strong>
            </div>
          )}

          {uploadMessage && (
            <div className="upload-message">
              {uploadMessage}
            </div>
          )}

        </section>

        {/* =========================
            Chat Messages
        ========================= */}

        <section className="messages">

          {messages.length === 0 && (
            <div className="welcome">

              <h2>
                👋 Welcome to StudyMate AI
              </h2>

              <p>
                Ask questions about your lecture
                materials.
              </p>

            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role}`}
            >

              <div className="message-label">
                {message.role === "user"
                  ? "You"
                  : "StudyMate AI"}
              </div>

              <div className="message-content">
                {message.content}
              </div>

              {/* =========================
                  Sources
              ========================= */}

              {message.sources &&
                message.sources.length > 0 && (
                  <div className="sources">

                    <div className="sources-header">
                      <strong>
                        Sources (
                        {message.sources.length})
                      </strong>
                    </div>

                    {message.sources.map(
                      (
                        source,
                        sourceIndex
                      ) => (
                        <div
                          key={sourceIndex}
                          className="source"
                        >

                          <div className="source-name">
                            📄{" "}
                            {source.source}
                          </div>

                          <div className="source-details">
                            Page{" "}
                            {source.page_number}
                            {" · "}
                            Chunk{" "}
                            {source.chunk_index}
                            {" · "}
                            Distance:{" "}
                            {source.distance.toFixed(
                              3
                            )}
                          </div>

                        </div>
                      )
                    )}

                  </div>
                )}

            </div>
          ))}

          {/* Loading */}

          {loading && (
            <div className="message assistant">

              <div className="message-label">
                StudyMate AI
              </div>

              <div className="message-content">
                Thinking...
              </div>

            </div>
          )}

        </section>

      </main>

      {/* =========================
          Fixed Question Input
      ========================= */}

      <div className="input-bar">

        <div className="input-area">

          <textarea
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={(event) => {
              if (
                event.key === "Enter" &&
                !event.shiftKey
              ) {
                event.preventDefault();
                askQuestion();
              }
            }}
            placeholder="Ask something about your lectures..."
            rows="2"
          />

          <div className="input-buttons">

            <button
              className="ask-button"
              onClick={askQuestion}
              disabled={
                loading || !question.trim()
              }
            >
              {loading ? "..." : "Ask"}
            </button>

            <button
              className="clear-button"
              onClick={clearChat}
              disabled={messages.length === 0}
            >
              Clear Chat
            </button>

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;