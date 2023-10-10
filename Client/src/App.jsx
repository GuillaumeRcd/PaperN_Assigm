import { useState } from 'react';
import { fetchNetworkCoverage } from './APIS/api.backend';
// import { searchAddress } from './APIS/api.data.gouv';

function App() {
  const [address, setAddress] = useState('');
  const [coverage, setCoverage] = useState({});
  const [proxyResponse, setProxyResponse] = useState(null);

  const handleAddressChange = (e) => {
    setAddress(e.target.value);
  };

  const fetchProxyResponse = async () => {
    try {
      console.log(address);
      const response = await fetch(`http://localhost:8000/proxy/?address=${address}`);
      const data = await response.json();
      setProxyResponse(data);
      console.log(data); 
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const fetchCoverage = async () => {
    try {
      const data = await fetchNetworkCoverage(address);
      setCoverage(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>Network Coverage Checker</h1>
      <div>
        <input
          type="text"
          placeholder="Enter address..."
          value={address}
          onChange={handleAddressChange}
        />
        <button onClick={fetchCoverage}>Check Coverage</button>
        <button onClick={fetchProxyResponse}>Fetch Proxy Response</button>
      </div>
      <div>
        <h2>Network Coverage:</h2>
        <pre>{JSON.stringify(coverage, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
