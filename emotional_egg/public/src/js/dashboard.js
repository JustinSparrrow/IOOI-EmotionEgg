import { baseURL } from './config.js';
import { getToken } from './auth.js';
import {jwtDecode} from "https://cdn.jsdelivr.net/npm/jwt-decode@4.0.0/build/esm/index.js";
// 获取 DOM 元素

if (!localStorage.getItem("token")) {
    window.location.href = "login.html";
}


const yearSelector = document.getElementById("year-selector");
const monthSelector = document.getElementById("month-selector");
const weekSelector = document.getElementById("week-selector");
const dateSelector = document.getElementById("date-selector");
const avatar = document.getElementById("emotion-avatar");

// 示例：全局按钮点击时检查 token
// 初始化 Chart.js
const ctx = document.getElementById("emotion-chart").getContext("2d");
let emotionChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "情绪变化",
            data: [],
            borderColor: "#FF90BC",
            backgroundColor: "rgba(255, 144, 188, 0.2)",
            borderWidth: 2,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1,
                    callback: value => getEmotionFromScore(value)
                }
            }
        }
    }
});

// 填充年份选择器（从后端拿数据）
async function loadYearOptions() {

    const token = getToken();
    const decoded = jwtDecode(token);
    const userId = decoded.user_id;

    try {
        const res = await fetch(`${baseURL}/api/emotion-years?user_id=${userId}`, {
            headers: { 'Authorization': 'Bearer ' + getToken() }
        });
        console.log(userId);
        const years = await res.json();
        console.log("📅 获取到年份：", years); 
        yearSelector.innerHTML = years.map(y => `<option value="${y}">${y}</option>`).join('');
    } catch (err) {
        console.error("加载年份失败", err);
    }
}

// 填充月份选择器
function loadMonthOptions() {
    monthSelector.innerHTML = '';
    for (let m = 1; m <= 12; m++) {
        const option = document.createElement("option");
        option.value = m;
        option.text = `${m} 月`;
        monthSelector.appendChild(option);
    }
}

// 动态更新周选择器（固定四周）
function updateWeekOptions() {
    const weeks = ["第1周", "第2周", "第3周", "第4周"];
    weekSelector.innerHTML = weeks.map((week, index) => 
        `<option value="${index + 1}">${week}</option>`
    ).join('');
}

// 当前过滤方式
let currentFilter = "year";

// 切换时间粒度
function setTimeFilter(filter) {
    currentFilter = filter;
    yearSelector.classList.add("hidden");
    monthSelector.classList.add("hidden");
    weekSelector.classList.add("hidden");
    dateSelector.classList.add("hidden");

    if (filter === "year") {
        yearSelector.classList.remove("hidden");
    } else if (filter === "month") {
        yearSelector.classList.remove("hidden");
        monthSelector.classList.remove("hidden");
    } else if (filter === "week") {
        yearSelector.classList.remove("hidden");
        monthSelector.classList.remove("hidden");
        weekSelector.classList.remove("hidden");
        updateWeekOptions();
    } else if (filter === "day") {
        dateSelector.classList.remove("hidden");
    }
}

// 从后端获取情绪数据
async function updateChartWithSelection() {
    const token = getToken();
    const decoded = jwtDecode(token);
    const userId = decoded.user_id;
    let apiUrl = `${baseURL}/api/emotions/dominant?filter=${currentFilter}&user_id=${userId}`;

    if (currentFilter === "year") {
        apiUrl += `&year=${yearSelector.value}`;
    } else if (currentFilter === "month") {
        apiUrl += `&year=${yearSelector.value}&month=${monthSelector.value}`;
    } else if (currentFilter === "week") {
        apiUrl += `&year=${yearSelector.value}&month=${monthSelector.value}&week=${weekSelector.value}`;
    } else if (currentFilter === "day") {
        const date = new Date(dateSelector.value);
        apiUrl += `&year=${date.getFullYear()}&month=${date.getMonth() + 1}&day=${date.getDate()}`;
    }

    try {
        console.log("🎯 正在请求接口：", apiUrl);

        const res = await fetch(apiUrl, {
            headers: { 'Authorization': 'Bearer ' + getToken() }
        });
        const result = await res.json();
        console.log("📊 获取到的 JSON 数据：", result);
        const chartContainer = document.getElementById("chart-container");
        chartContainer.classList.remove("hidden");
        chartContainer.classList.add("show");

        setTimeout(() => {
            chartContainer.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 300);

        emotionChart.data.labels = result.labels || [];
        emotionChart.data.datasets[0].data = result.data || [];
        emotionChart.update();
        
    } catch (err) {
        console.error("图表数据请求失败", err);
    }
}

// 从后端获取最近一次情绪记录
async function loadLatestAvatar() {

    try {
        const res = await fetch(`${baseURL}/log/user/lastInteraction`, {
            headers: { 'Authorization': 'Bearer ' + getToken() }
        });
        const data = await res.json();
        avatar.textContent = getEmotionFromScore(data.emotion_label || 2);
    } catch (err) {
        console.warn("加载小人失败", err);
    }
}

// 情绪分数转表情
function getEmotionFromScore(score) {
    switch (score) {
        case 3: return "😊";
        case 2: return "😐";
        case 1: return "😢";
        case 0: return "😡";
        default: return "😐";
    }
}

// 初始化页面
document.addEventListener("DOMContentLoaded", () => {
    loadYearOptions();
    loadMonthOptions();
    loadLatestAvatar();

});

// 为按钮绑定事件监听器（替代 HTML 中 onclick）
document.addEventListener("DOMContentLoaded", () => {
    loadYearOptions();
    loadMonthOptions();
    loadLatestAvatar();

    document.getElementById("btn-year").addEventListener("click", () => setTimeFilter("year"));
    document.getElementById("btn-month").addEventListener("click", () => setTimeFilter("month"));
    document.getElementById("btn-week").addEventListener("click", () => setTimeFilter("week"));
    document.getElementById("btn-day").addEventListener("click", () => setTimeFilter("day"));

    document.getElementById("query-button").addEventListener("click", updateChartWithSelection);
});
document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("token");  // 清除JWT
    alert("您已成功退出登录！");
    window.location.href = "index.html";  // 返回主页面
  });
