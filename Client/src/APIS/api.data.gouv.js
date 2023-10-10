const url = "https://api-adresse.data.gouv.fr/search/?q=";

export const searchAddress = async (address) => {
  if (address.length > 6) {
    try {
      fetch(`${url}${address}`).then(function (response) {
        return response.json;
      });
    } catch (error) {
      console.error("Error:", error);
      throw error;
    }
  }
};
