import { useState, useEffect } from "react";
// import { fetchNetworkCoverage } from "./APIS/api.backend";
// import Select from "react-select";
import AsyncSelect from "react-select/async";
// import { searchAddress } from './APIS/api.data.gouv';

function App() {
  // const [address, setAddress] = useState("");
  const [coverage, setCoverage] = useState({});
  const [proxyResponse, setProxyResponse] = useState(null);
  // const [suggestions, setSuggestions] = useState([]);

  // const handleAddressChange = (selectedOption) => {
  //   // selectedOption contient la nouvelle valeur sélectionnée
  //   const newAddress = selectedOption ? selectedOption.value : ''; // Obtenez la valeur sélectionnée ou une chaîne vide si rien n'est sélectionné
  //   setAddress(newAddress);
  // };

  // useEffect(() => {
  //   if (address.length > 5) {
  //     fetch(`http://localhost:8000/proxy/?address=${address}`)
  //       .then((response) => response.json())
  //       .then((data) => {
  //         const features = data.features;
  //         const labels = features.map((feature) => feature.properties.label);
  //         setSuggestions(labels);
  //         console.log(suggestions);
  //       })
  //       .catch((error) => console.error("Erreur lors de la requête:", error));
  //   } else {
  //     setSuggestions([]);
  //   }
  // }, [address]);

  // const formattedSuggestions = suggestions.map((suggestion) => ({
  //   label: suggestion,
  //   value: suggestion,
  // }));

  const loadOptions = (inputValue, callback) => {
    if (inputValue.length > 5) {
      fetch(`http://localhost:8000/proxy/?address=${inputValue}`)
        .then((response) => response.json())
        .then((data) => {
          const features = data.features;
          const labels = features.map((feature) => ({
            label: feature.properties.label,
            value: feature.properties.label,
          }));
          callback(labels);
        })
        .catch((error) => console.error("Erreur lors de la requête:", error));
    } else {
      callback([]);
    }
  };

  // const fetchProxyResponse = async () => {
  //   try {
  //     console.log(address);
  //     const response = await fetch(
  //       `http://localhost:8000/proxy/?address=${address}`
  //     );
  //     const data = await response.json();
  //     setProxyResponse(data.features);
  //     console.log(data.features);
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

  // const fetchCoverage = async () => {
  //   try {
  //     const data = await fetchNetworkCoverage(address);
  //     setCoverage(data);
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

  return (
    <div>
      <h1>Network Coverage Checker</h1>
      <div>
        {/* <input
          type="text"
          placeholder="Enter address..."
          value={address}
          onChange={handleAddressChange}
        /> */}
        {/* 
        <Select
          type="text"
          placeholder="Enter address..."
          value={address}
          onChange={handleAddressChange}
          options={formattedSuggestions}
          isSearchable={true}
          // onChange={(selectedOption) => setAddress(selectedOption.value)}
        /> */}
        <AsyncSelect
          cacheOptions
          defaultOptions
          loadOptions={loadOptions}
          isSearchable={true}
        />
        {/* <button onClick={fetchCoverage}>Check Coverage</button>
        <button onClick={fetchProxyResponse}>Fetch Proxy Response</button> */}
      </div>
      <div>
        <h2>Network Coverage:</h2>
        <pre>{JSON.stringify(coverage, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
