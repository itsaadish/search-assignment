// import React, { useState, useEffect } from 'react';
// import { useParams } from 'react-router-dom';
// import axios from 'axios';

// // Results Component
// function Results() {
//     const { searchId } = useParams();
//     const [results, setResults] = useState([]);
//     const [loading, setLoading] = useState(true);

//     useEffect(() => {
//       const interval = setInterval(async () => {
//         try {
//           const response = await axios.get(`/api/results/${searchId}/`, {
//             headers: {
//               Authorization: `Token ${localStorage.getItem('token')}`
//             }
//           });

//           if (response.data.status === 'completed') {
//             setResults(response.data.results);
//             setLoading(false);
//             clearInterval(interval);
//           }
//         } catch (error) {
//           console.error('Error fetching results:', error);
//           clearInterval(interval);
//         }
//       }, 2000);

//       return () => clearInterval(interval);
//     }, [searchId]);

//     return (
//       <div className="results-container">
//         <h2>Search Results</h2>
//         {loading ? (
//           <p>Loading results...</p>
//         ) : (
//           <table className="results-table">
//             <thead>
//               <tr>
//                 <th>Image</th>
//                 <th>Website</th>
//                 <th>Title</th>
//                 <th>Price</th>
//                 <th>Size</th>
//                 <th>Link</th>
//               </tr>
//             </thead>
//             <tbody>
//               {results.map((result, index) => (
//                 <tr key={index}>
//                   <td>
//                     <img
//                       src={result.image_url}
//                       alt={result.title}
//                       className="product-image"
//                     />
//                   </td>
//                   <td>{result.website}</td>
//                   <td>{result.title}</td>
//                   <td>{result.price}</td>
//                   <td>{result.size}</td>
//                   <td>
//                     <a
//                       href={result.product_url}
//                       target="_blank"
//                       rel="noopener noreferrer"
//                     >
//                       View Product
//                     </a>
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         )}
//       </div>
//     );
//   }

// export default Results;

import React, { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function Results() {
  const { searchId } = useParams();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [logs, setLogs] = useState([]);
  const [ws, setWs] = useState(null);
  const [error, setError] = useState(null); // New state for error handling
  const wsRef = useRef(null);

  useEffect(() => {
    if (wsRef.current) {
      console.log("WebSocket already exists, skipping new connection...");
      return;
    }

    // Establish WebSocket connection
    const newWs = new WebSocket(`ws://localhost:3100/ws/search/${searchId}/`);

    newWs.onopen = () => {
      console.log("WebSocket connected");
    };

    newWs.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        // Handle log messages
        setLogs((prevLogs) => [...prevLogs, data.message]);
      } else if (data.status === "completed") {
        // Handle completion status
        fetchResults();
        newWs.close();
      } else if (data.status === "failed") {
        // Handle failure status
        setError("Something went wrong. Please try again.");
        setLoading(false);
        newWs.close();
      }
    };

    newWs.onerror = (error) => {
      console.error("WebSocket error:", error);
      setError("WebSocket connection failed. Please try again."); // Set error message
      setLoading(false); // Stop loading
    };

    newWs.onclose = (event) => {
      console.log("WebSocket disconnected", event.reason || "");
      wsRef.current = null; // Reset the ref when the connection is closed
    };

    wsRef.current = newWs;

    return () => {
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        console.log("Cleaning up WebSocket connection...");
        wsRef.current.close();
      }
    };
  }, [searchId]);

  const fetchResults = async () => {
    try {
      const response = await axios.get(`/api/results/${searchId}/`, {
        headers: {
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      });
      setResults(response.data.results);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching results:", error);
      setError("Failed to fetch results. Please try again."); // Set error message
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="results-container">
      <h2 style={{ textAlign: 'center', backgroundColor: 'blue', color: 'white', padding: '20px', borderRadius: '8px', marginTop: '-4px' }}>
        Search Results
      </h2>
      {loading ? (
        <div className="loading-container">
          <h3>Scraping Progress</h3>
          <div className="logs-container">
            {logs.map((log, index) => (
              <div key={index} className="log-entry">
                {log}
              </div>
            ))}
          </div>
        </div>
      ) : error ? (
        <div className="error-message">
          <p>{error}</p>
        </div>
      ) : (
        <table className="results-table">
          <thead>
            <tr>
              <th>Image</th>
              <th>Website</th>
              <th>Title</th>
              <th>Price</th>
              <th>Size</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => (
              <tr key={index}>
                <td>
                  <img
                    src={result.image_url}
                    alt={result.title}
                    className="product-image"
                  />
                </td>
                <td>{result.website}</td>
                <td>{result.title}</td>
                <td>{result.price}</td>
                <td>{result.size}</td>
                <td>
                  <a
                    href={result.product_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View Product
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Results;
