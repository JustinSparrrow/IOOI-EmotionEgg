import { baseURL } from "./config.js";
import { getToken } from "./auth.js";

const signatureInput = document.getElementById("signature");
const avatarInput = document.getElementById("avatar");
const form = document.getElementById("profile-form");
const message = document.getElementById("update-message");

async function loadProfile() {
  try {
    const res = await fetch(`${baseURL}/log/user/profile`, {
      headers: {
        Authorization: "Bearer " + getToken(),
      },
    });
    const data = await res.json();
    signatureInput.value = data.signature || "";
    avatarInput.value = data.avatar || "";
  } catch (err) {
    alert("加载失败：" + err.message);
  }
}

avatarInput.addEventListener("input", () => {
  const preview = document.getElementById("avatar-preview");
  preview.src = avatarInput.value.trim() || "public/images/example.jpg";
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    const res = await fetch(`${baseURL}/log/user/profile`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + getToken(),
      },
      body: JSON.stringify({
        signature: signatureInput.value.trim(),
        avatar: avatarInput.value.trim(),
      }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "更新失败");
    message.classList.remove("hidden");
    message.textContent = "✅ 个人信息已更新";
    setTimeout(() => {
      message.classList.add("hidden");
    ;
    signatureInput.value = "";
    avatarInput.value = "";
    
  },2000);

  } catch (err) {
    alert("❌ 更新失败：" + err.message);
  }
});

document.addEventListener("DOMContentLoaded", loadProfile);
