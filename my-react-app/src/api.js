import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5001", // Flask backend
});

export const predictDisease = async (symptoms) => {
  const response = await API.post("/predict", { symptoms });
  return response.data;
};
