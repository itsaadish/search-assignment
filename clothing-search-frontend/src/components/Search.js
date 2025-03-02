import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

// Search Component
function Search() {
  const navigate = useNavigate();
  const [prompt, setPrompt] = useState("");
  const [searchId, setSearchId] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "/api/search/",
        { prompt },
        {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
          },
        }
      );
      setSearchId(response.data.search_id);
      navigate(`/results/${response.data.search_id}`);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  return (
    <div className="centered-box">
  <div className="search-container">
    <h1 className="search-title">Clothing Search</h1>
    <form onSubmit={handleSearch} className="search-form">
      <div className="search-input-container">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your search prompt..."
          className="search-input"
          required
        />
        <button type="submit" className="search-button">
          <span className="search-icon">&#128269;</span> {/* Magnifying glass icon */}
        </button>
      </div>
    </form>
  </div>
</div>
  );
}

export default Search;
