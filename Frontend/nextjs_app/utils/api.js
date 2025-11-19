const BASE_URL = "http://127.0.0.1:8001/api/v1";

export async function api(route, method = "GET", body = null, token = null) {
  const res = await fetch(`${BASE_URL}${route}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` })
    },
    body: body ? JSON.stringify(body) : null
  });

  if (!res.ok) {
    let err = "API Error";
    try {
      const data = await res.json();
      err = data.detail || JSON.stringify(data);
    } catch {}
    throw new Error(err);
  }

  return res.json();
}
