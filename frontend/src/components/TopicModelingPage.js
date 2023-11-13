// // TopicModelingPage.js
// import React, { useState } from 'react';

// const TopicModelingPage = () => {
//   const [inputText, setInputText] = useState('');
//   const [result, setResult] = useState([]);

//   const sendToAPI = async () => {
//     try {
//       // Replace the following URL with the actual API endpoint
//       const apiUrl = `http://localhost:8000/topics?text=${inputText}`;
//       const response = await fetch(apiUrl, {
//         method: 'GET',
//         headers: {
//           'Content-Type': 'application/json',
//           // Add any other headers as needed
//         },
//       });

//       if (!response.ok) {
//         throw new Error('Network response was not ok');
//       }

//       const data = await response.json();

//       // Display the API response
//       console.log(data);
//       setResult(data.result.top_topics);
//     } catch (error) {
//       console.error('Error:', error);
//       setResult([]);
//     }
//   };

//   // const displayComments = (topicIndex, comments) => (
//   //   <div key={topicIndex} className="comment-card">
//   //     <h5>Topic {topicIndex+1}</h5>
//   //     <ul>
//   //       {comments.map((comment, index) => (
//   //         <li key={index}>
//   //           {`${comment[0].substring(0, 500)} (${comment[1].toFixed(2)})`}
//   //         </li>
//   //       ))}
//   //     </ul>
//   //   </div>
//   // );

//   const displayComments = (topicIndex, comments) => {
//     const commentContainer = document.getElementById('result');
//     const topicCard = document.createElement('div');
//     topicCard.className = 'comment-card';

//     // Check if comments is an array before using .map
//     if (Array.isArray(comments)) {
//       comments = comments.map(comment => [comment[0].substring(0, 500), comment[1]]);
//       topicCard.innerHTML = `<h5>Topic ${topicIndex}</h5><ul>${comments.map(comment => `<li>${comment[0]} (${comment[1].toFixed(2)})</li>`).join('')}</ul>`;
//       commentContainer.appendChild(topicCard);
//     } else {
//       // Handle the case where comments is not an array
//       console.error('Comments is not an array:', comments);
//     }
//   };


//   return (
//     <div className="container">
//       <h2 className="mt-5">Check Top Topics</h2>
//       <form id="apiForm">
//         <div className="form-group">
//           <label htmlFor="inputText">Enter Video ID</label>
//           <input
//             type="text"
//             className="form-control"
//             id="inputText"
//             placeholder="video-id"
//             value={inputText}
//             onChange={(e) => setInputText(e.target.value)}
//           />
//         </div>
//         <button type="button" className="btn btn-primary" onClick={sendToAPI}>
//           Submit
//         </button>
//       </form>
//       <div id="result" className="mt-3">
//         {result.map((comments, index) => displayComments(index, comments))}
//       </div>
//     </div>
//   );
// };

// export default TopicModelingPage;

import React, { useState, useEffect } from 'react';

const TopicModelingPage = () => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);

  const sendToAPI = () => {
    // Replace the following URL with the actual API endpoint
    const apiUrl = `http://localhost:8000/topics?text=${inputText}`;

    // Make a simple GET request to the API
    fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Add any other headers as needed
      },
    })
      .then((response) => response.json())
      .then((data) => {
        // Set the result in state
        setResult(data);
      })
      .catch((error) => {
        console.error('Error:', error);
        // Handle errors if needed
      });
  };

  useEffect(() => {
    // You may want to fetch the result when the component mounts or when inputText changes.
    // For now, we'll fetch the result when the component mounts.
    sendToAPI();
  }, []); // Empty dependency array means this effect runs once after the initial render

  const displayComments = () => {
    const commentContainer = document.getElementById('result');

    // Check if result exists and has top_topics property
    if (result && result.top_topics) {
      for (const topicIndex in result.top_topics) {
        const comments = result.top_topics[topicIndex];

        const topicCard = document.createElement('div');
        topicCard.className = 'comment-card';

        // Check if comments is an array before using .map
        if (Array.isArray(comments)) {
          comments.forEach((comment) => {
            const truncatedComment = comment[0].substring(0, 500);
            const listItem = document.createElement('li');
            listItem.innerHTML = `${truncatedComment} (${comment[1].toFixed(2)})`;
            topicCard.appendChild(listItem);
          });

          const heading = document.createElement('h5');
          heading.textContent = `Topic ${topicIndex}`;
          topicCard.insertBefore(heading, topicCard.firstChild);

          commentContainer.appendChild(topicCard);
        } else {
          // Handle the case where comments is not an array
          console.error('Comments is not an array:', comments);
        }
      }
    } else {
      console.error('Invalid result format:', result);
    }
  };

  return (
    <div className="container">
      <h2 className="mt-5">Check Top Topics</h2>
      <form
        id="apiForm"
        onSubmit={(e) => {
          e.preventDefault();
          sendToAPI();
        }}
      >
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
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
      <div id="result" className="mt-3"></div>
      {result && <button onClick={displayComments}>Display Comments</button>}
    </div>
  );
};

export default TopicModelingPage;
