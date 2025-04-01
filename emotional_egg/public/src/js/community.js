document.addEventListener("DOMContentLoaded", async function () {
    const postList = document.getElementById("post-list");

    // 1. 获取社区帖子（来自后端）
    async function fetchPosts() {
        try {
            const response = await fetch("/log/community/posts");
            const posts = await response.json();
            renderPosts(posts);
        } catch (error) {
            console.error("❌ 无法获取社区数据：", error);
            postList.innerHTML = "<p class='text-gray-600'>无法加载社区内容，请稍后再试。</p>";
        }
    }

    // 2. 渲染帖子内容
    function renderPosts(posts) {
        postList.innerHTML = "";
        posts.forEach(post => {
            const postItem = document.createElement("div");
            postItem.className = "bg-white p-4 rounded-lg shadow-md mb-4";

            const commentsHtml = post.comments?.map(c => `
                <li class="text-sm text-gray-700 mb-1">🤖 <span class="italic">${c}</span></li>
            `).join("") || "";

            postItem.innerHTML = `
                <p class="text-gray-800 font-medium">🗣️ 用户说：${post.content}</p>
                <div class="mt-2">
                    <h4 class="text-sm font-semibold text-gray-600">💬 AI 回复：</h4>
                    <ul class="ml-4 mt-1">${commentsHtml}</ul>
                </div>
            `;

            postList.appendChild(postItem);
        });
    }

    // 初始化
    fetchPosts();
});

document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("token");  // 清除JWT
    alert("您已成功退出登录！");
    window.location.href = "index.html";  //返回主页面
  });
