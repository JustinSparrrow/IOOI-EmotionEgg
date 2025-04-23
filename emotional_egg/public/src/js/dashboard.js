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
const dateSelectorForLogs = document.getElementById("log-date-selector");


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


// 填充年份选择器 更新日志函数->更新情绪小人和交互内容即可
async function updateLogs() {
    const token = getToken();
    const decoded = jwtDecode(token);
    const userId = decoded.user_id;
    const selectedDate = document.getElementById("log-date-selector").value;

    if (!selectedDate) {
        console.error("请选择日期");
        return;  // 如果没有选择日期，直接返回
    }
    //分割日期选择
    const [year, month, day] = selectedDate.split("-");

    //构建查询参数
    const filter = "day";  // 假设我们查询的是按天的日志
    const queryParams = new URLSearchParams({
        user_id: userId,
        day: day,
        month: month,
        year: year,
        filter: filter
    }).toString();

    try {
        const res = await fetch(`${baseURL}/api/emotions/dominant?${queryParams}`, {
            headers: { 'Authorization': 'Bearer ' + token }
        });

        if (res.ok) {
            const data = await res.json();
            const logs = data.data; // 获取返回的数据

            const logContainer = document.getElementById("interaction-log");
            logContainer.innerHTML = '';  // 清空现有内容

            // 遍历每个时间段（例如 "15:00"）
            for (let time in logs) {
                const log = logs[time];

                const logElement = document.createElement('div');
                logElement.classList.add('log-item', 'bg-white', 'p-4', 'rounded-lg', 'shadow-md', 'mb-4');

                // 添加时间
                const timeElement = document.createElement('h3');
                timeElement.classList.add('font-semibold', 'text-gray-800');
                timeElement.textContent = `${time}`;

                // 添加“情绪标签”
                const emotionLabel = document.createElement('p');
                emotionLabel.classList.add('font-semibold', 'text-gray-600');
                emotionLabel.textContent = `情绪: ${log.emotion_label || '无情绪'}`;

                // 添加“您说”（text）
                const userText = document.createElement('p');
                userText.classList.add('font-semibold', 'text-gray-800');
                userText.textContent = `您说: ${log.text || '无内容'}`;

                // 添加“建议”（suggestion）
                const suggestion = document.createElement('p');
                suggestion.classList.add('text-sm', 'text-gray-500');
                suggestion.textContent = `建议: ${log.suggestion || '无建议'}`;

                // 将所有元素添加到 logElement 中
                logElement.appendChild(timeElement);
                logElement.appendChild(emotionLabel);
                logElement.appendChild(userText);
                logElement.appendChild(suggestion);

                // 将 logElement 添加到 logContainer 中
                logContainer.appendChild(logElement);
            }
        } else {
            console.error('Failed to fetch logs:', res.statusText);
        }
    } catch (err) {
        console.error('Error fetching logs:', err);
    }
}







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
    console.log("运行到这里了");
    const token = getToken();
    const decoded = jwtDecode(token);
    const userId = decoded.user_id;
    console.log("测试currentfillter",currentFilter);

    let apiUrl = `${baseURL}/api/emotions/dominant?filter=${currentFilter}&user_id=${userId}`;
    console.log("测试处理前apiurl",apiUrl);
    const chartMessage = document.getElementById("chart-message");
    const chartContainer = document.getElementById("chart-container");
    if (currentFilter === "year") {
        apiUrl += `&year=${yearSelector.value}`;
        console.log("测试处理逻辑1 apiurl",apiUrl);
    } else if (currentFilter === "month") {
        apiUrl += `&year=${yearSelector.value}&month=${monthSelector.value}&year=${yearSelector.value}`;
        console.log("测试处理逻辑2 apiurl",apiUrl);
    }

    try {
        console.log("🎯 正在请求接口：", apiUrl);

        const res = await fetch(apiUrl, {
            headers: { 'Authorization': 'Bearer ' + getToken() }
        });
        console.log("测试访问成功了吗",res);
        const result = await res.json();
        console.log("json解析成功了吗",result);
        const chartContainer = document.getElementById("chart-container");
        //解析js
        const data = result.data; 
        //const entries = Object.entries(data);
        // 使用 Object.entries 转换数据并仅保留 `emotion_label`
        const entries = Object.entries(data).map(([label, { emotion_label }]) => [label, emotion_label]);

        console.log(entries);
        console.log("画图数组里是什么", entries);

        entries.sort((a, b) => new Date(a[0]) - new Date(b[0]));
        const labels = entries.map(([label, _]) => label);

        //映射规则在哪没找到呀，我在这里补一个
        const labelMap = {
            happy: 3,  
            calm: 2,   
            sad: 1,   
            angry: 0  
        };
        
        //const dataPoints = entries.map(([_, value]) => Number(value));
        
        const dataPoints = entries.map(([_, value]) => labelMap[value] || 0); // 如果无法识别的标签返回 0

        

        console.log("横坐标解析成功了吗", labels);
        console.log("纵坐标解析成功了吗", dataPoints);
        //判断是否获取有效信息
        if (!labels.length || !dataPoints.length || dataPoints.some(isNaN)) {
            chartMessage.textContent = "暂无有效数据，请先记录你的情绪吧～";
            chartMessage.classList.remove("hidden");
            chartContainer.classList.add("hidden"); // 隐藏图表
            return;
        }     

        chartMessage.classList.add("hidden");
        chartContainer.classList.remove("hidden");
        chartContainer.classList.add("show");

        setTimeout(() => {
            chartContainer.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 300);

        emotionChart.data.labels = labels;
        emotionChart.data.datasets[0].data = dataPoints;
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
        default: return "😊";
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
    document.getElementById("query-button").addEventListener("click", updateChartWithSelection);
    document.getElementById("log-query-button").addEventListener("click",updateLogs);
});

document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem("token");  // 清除JWT
    alert("您已成功退出登录！");
    window.location.href = "index.html";  // 返回主页面
  });

