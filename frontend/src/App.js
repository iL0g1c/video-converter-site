import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [format, setFormat] = useState("mp4");
  const [downloadUrl, setDownloadUrl] = useState("");

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("format", format);

    try {
      const response = await axios.post(
        "http://localhost:8000/upload/",
        formData
      );
      const { file_id, output_path } = response.data;

      // Set download URL
      setDownloadUrl(
        `http://localhost:8000/download/${file_id}?format=${format}`
      );
      alert("File converted successfully!");
    } catch (error) {
      console.error("Error uploading file", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎥 Video Converter</h1>
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <select value={format} onChange={(e) => setFormat(e.target.value)}>
          <option value="mp4">MP4</option>
          <option value="avi">AVI</option>
          <option value="mkv">MKV</option>
        </select>
        <button onClick={uploadFile}>Convert Video</button>

        {downloadUrl && (
          <a
            href={downloadUrl}
            download
            target="_blank"
            rel="noopener noreferrer"
          >
            🎉 Download Converted File
          </a>
        )}
      </header>
    </div>
  );
}

export default App;
