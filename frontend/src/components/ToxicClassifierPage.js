// ToxicClassifierPage.js
import React, { useState } from 'react';

const ToxicClassifierPage = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState({
    toxic: 0,
    'non-toxic': 0,
    toxic_comments: [],
  });

  const sendToAPI = async () => {
    try {
      // Replace the following URL with the actual API endpoint
      const apiUrl = `http://localhost:8080/predict?text=${inputText}`;
      const response = await fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Add any other headers as needed
        },
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      // Display the API response
      console.log(data);
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
      setResult({
        toxic: 0,
        'non-toxic': 0,
        toxic_comments: [],
      });
    }
  };

  return (
    <div className="container">
      <h2 className="mt-5">Check Toxic comments</h2>
      <form id="apiForm">
        <div className="form-group">
          <label htmlFor="inputText">Enter Video ID</label>
          <input
            type="text"
            className="form-control"
            id="inputText"
            placeholder="video-id"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
        </div>
        <button type="button" className="btn btn-primary" onClick={sendToAPI}>
          Submit
        </button>
      </form>
      <div id="result" className="mt-3">
        <p>Total Toxic Comments: {result.toxic}</p>
        <p>Total Non-Toxic Comments: {result['non-toxic']}</p>
        <h3>Top 10 Comments:</h3>
        <ol>
          {result.toxic_comments.slice(0, 10).map((comment, index) => (
            <li key={index}>{comment}</li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default ToxicClassifierPage;
