const url = "http://localhost:8000/";

// api.backend.js

export const fetchNetworkCoverage = async (address) => {
  try {
    const response = await fetch(`${url}network/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: address }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};
