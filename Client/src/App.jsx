import { useState } from "react";
import AsyncSelect from "react-select/async";

function App() {
  const [coverage, setCoverage] = useState(null);
  const [selectedAddress, setSelectedAddress] = useState(null);

  const loadOptions = (inputValue, callback) => {
    if (inputValue.length > 5) {
      fetch(`http://localhost:8000/proxy/?address=${inputValue}`)
        .then((response) => response.json())
        .then((data) => {
          const features = data.features;
          console.log(features);
          const labels = features.map((feature) => ({
            label: feature.properties.label,
            value: feature.properties.label,
            x: feature.properties.x,
            y: feature.properties.y,
            long: feature.geometry.coordinates[0],
            lat: feature.geometry.coordinates[1],
          }));
          callback(labels);
        })
        .catch((error) => console.error("Erreur lors de la requête:", error));
    } else {
      callback([]);
    }
  };

  const handleSearchNetwork = async () => {
    if (selectedAddress) {
      console.log(selectedAddress);

      try {
        const response = await fetch("http://localhost:8000/coverage", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(selectedAddress),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        setCoverage(data);
        console.log("Réponse du backend :", data);
      } catch (error) {
        console.error("Erreur lors de la requête vers le backend:", error);
      }
    }
  };

  return (
    <div>
      <h1>Recherche de couverture réseau</h1>
      <p>Tapez l'adresse que vous souhaitez analyser</p>
      <div>
        <AsyncSelect
          cacheOptions
          defaultOptions
          loadOptions={loadOptions}
          isSearchable={true}
          onChange={(selectedOption) => setSelectedAddress(selectedOption)}
        />
      </div>
      <div>
        <button onClick={handleSearchNetwork}>Chercher réseau</button>
      </div>
      <div>
        {coverage && 
        <>
        <h2>Résultat</h2>
        <pre>{JSON.stringify(coverage, null, 2)}</pre>
        </>
      }
      </div>
    </div>
  );
}

export default App;
