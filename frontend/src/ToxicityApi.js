import axios from 'axios';

const baseUrl = 'http://localhost:8080/predict?text=';

async function getToxicity(id) {
  try {
    const response = await axios.get(`${baseUrl}${encodeURIComponent(id)}`);
    if (!response || !response.ok) throw Error('Failed to fetch toxicity score');
    return response.json().then(({ toxicity }) => ({ toxicity }));
  } catch (err) {
    console.error(err);
    throw err;
  }
}

export { getToxicity };