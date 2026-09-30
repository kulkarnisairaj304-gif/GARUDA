import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("garuda_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export async function login(username: string, password: string) {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);

  const response = await api.post("/auth/login", formData, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  localStorage.setItem("garuda_token", response.data.access_token);

  return response.data;
}

export async function register(
  username: string,
  email: string,
  password: string
) {
  const response = await api.post("/auth/register", {
    username,
    email,
    password,
  });

  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get("/auth/me");
  return response.data;
}

export async function analyzePhishing(data: {
  sender: string;
  subject: string;
  body: string;
  urls?: string[];
}) {
  const response = await api.post("/phishing/analyze", data);
  return response.data;
}

export function logout() {
  localStorage.removeItem("garuda_token");
  localStorage.removeItem("garuda_username");
}

export async function getProjects() {
  const response = await api.get("/projects");
  return response.data;
}

export async function getApplications() {
  const response = await api.get("/applications");
  return response.data;
}

export async function getScans() {
  const response = await api.get("/scans");
  return response.data;
}
