import { baseURL } from "./config.js";

export function getToken() {
    return localStorage.getItem("token") || "";
}

export async function login(username, password) {
  try {
    const res = await fetch(`${baseURL}/user/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "登录失败");

    localStorage.setItem("token", data.token);
    return true;
  } catch (err) {
    alert("登录失败：" + err.message);
    return false;
  }
}

export async function register(username, email, password, confirmPassword) {
  if (password !== confirmPassword) {
    alert("两次输入的密码不一致！");
    return false;
  }

  try {
    const res = await fetch(`${baseURL}/user/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "注册失败");

    alert("注册成功，请登录");
    return true;
  } catch (err) {
    alert("注册失败：" + err.message);
    return false;
  }
}