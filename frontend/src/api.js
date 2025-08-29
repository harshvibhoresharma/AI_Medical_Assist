import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:5001", // your Flask app.py port
});

export const predictDisease = (payload) =>
  api.post("/predict", payload).then((r) => r.data);
