import { baseURL } from './config.js';
import { getToken } from './auth.js';

if (!localStorage.getItem("token")) {
    window.location.href = "login.html";
}


document.addEventListener("DOMContentLoaded", async function () {
    const postList = document.getElementById("post-list");
    const postBtn = document.getElementById("post-btn");
    const postContent = document.getElementById("post-content");

 /**
 * 获取社区帖子列表（适配返回的数组格式）
 * @returns {Promise<Array<{
 *   ID: number,
 *   UserID: number,
 *   Content: string,
 *   Likes: number,
 *   Comments: Array<any>,
 *   CreatedAt: string
 * }>>} 标准化后的帖子数组
 */
async function fetchPosts() {
    try {
        const response = await fetch(`${baseURL}/log/community/posts`, {
            method: "GET",
            headers: {
                'Authorization': 'Bearer ' + getToken(),
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${await response.text()}`);
        }

        const { data } = await response.json(); // 解构data字段
        
        // 数据标准化处理
        return (Array.isArray(data) ? data : []).map(post => ({
            id: post.ID ?? 0,
            userId: post.UserID ?? 0,
            content: post.Content || "无内容",
            likes: post.Likes ?? 0,
            comments: Array.isArray(post.Comments) ? post.Comments : [],
            createdAt: post.CreatedAt || new Date().toISOString()
        }));

    } catch (error) {
        console.error("❌ 获取帖子失败:", error);
        showError("加载失败，请稍后重试");
        return []; // 始终返回数组
    }
}

// 统一错误显示函数
function showError(message) {
    const container = document.getElementById('post-list');
    if (container) {
        container.innerHTML = `
            <div class="error-alert">
                <span>⚠️ ${message}</span>
                <button onclick="location.reload()">刷新</button>
            </div>
        `;
    }
}

    // 2. 发布新帖子
    async function createPost(content) {
        try {
            const response = await fetch(`${baseURL}/log/community/post`, { // 注意是 /post 不是 /posts
                method: "POST",
                headers: { 'Authorization': 'Bearer ' + getToken() },
                body: JSON.stringify({ content })
            });
            const responseData = await response.json(); // 添加这行
            console.log("后端返回：", responseData); // 打印返回值
            
            if (!response.ok) throw new Error("发布失败");
            
            // 发布成功后重新加载帖子列表
            const posts = await fetchPosts(); // 调用获取帖子的函数
            renderPosts(posts); // 重新渲染页面
            return true;
            
        } catch (error) {
            console.error("❌ 发布失败：", error);
            alert("发布失败，请检查网络后重试");
            return false;
        }
    }
    // 3. 渲染帖子列表
    function renderPosts(posts) {
        if (posts.length === 0) {
            postList.innerHTML = `
                <div class="bg-blue-50 p-4 rounded-lg">
                    <p class="text-blue-600">✨ 社区还没有内容，快来第一个发言吧！</p>
                </div>
            `;
            return;
        }

        postList.innerHTML = "";
        posts.forEach(post => {
            const postItem = document.createElement("div");
            postItem.className = "bg-white p-4 rounded-lg shadow-md mb-4 animate-fade-in";

            const commentsHtml = post.comments?.map(c => `
                <li class="text-sm text-gray-700 mb-1 pl-4 border-l-2 border-purple-200">
                    <span class="font-medium text-purple-600">AI：</span>
                    <span class="italic">${c}</span>
                </li>
            `).join("") || "";

            postItem.innerHTML = `
                <div class="flex items-start">
                    <div class="bg-pink-100 w-8 h-8 rounded-full flex items-center justify-center mr-3">
                        <span class="text-pink-600">${post.userId ? post.userId.toString().slice(-2) : '?'}</span>
                    </div>
                    <div class="flex-1">
                        <p class="text-gray-800">${post.content}</p>
                        <div class="mt-3 text-sm text-gray-500">
                            ${new Date(post.createdAt).toLocaleString()}
                        </div>
                    </div>
                </div>
                ${commentsHtml ? `
                <div class="mt-3 pl-11">
                    <h4 class="text-xs font-semibold text-gray-500 mb-1">AI 分析：</h4>
                    <ul class="space-y-2">${commentsHtml}</ul>
                </div>
                ` : ''}
            `;
            postList.appendChild(postItem);
        });
    }

    // 4. 初始化加载 + 自动刷新
    async function loadAndRefresh() {
        const posts = await fetchPosts();
        renderPosts(posts);
        
        // 每30秒自动刷新
        setInterval(async () => {
            const newPosts = await fetchPosts();
            if (newPosts.length > 0) {
                renderPosts(newPosts);
            }
        }, 30000);
    }

    // 5. 发布事件处理
    postBtn.addEventListener("click", async () => {
        const content = postContent.value.trim();
        if (!content) {
            postContent.classList.add("border-red-300");
            setTimeout(() => postContent.classList.remove("border-red-300"), 2000);
            return;
        }

        postBtn.disabled = true;
        postBtn.textContent = "发布中...";
        
        const success = await createPost(content);
        if (success) {
            postContent.value = "";
            await loadAndRefresh(); // 刷新列表
        }

        postBtn.disabled = false;
        postBtn.textContent = "发布";
    });

    // 回车快捷发布
    postContent.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            postBtn.click();
        }
    });

    // 初始加载
    loadAndRefresh();
});

    // 初始化

document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("token");  // 清除JWT
    alert("您已成功退出登录！");
    window.location.href = "index.html";  //返回主页面
  });

