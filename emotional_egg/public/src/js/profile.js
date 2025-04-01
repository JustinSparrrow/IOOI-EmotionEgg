// src/js/profile.js
import { baseURL } from './config.js';
import { getToken } from './auth.js';

const userNameEl = document.getElementById('user-name');
const userEmailEl = document.getElementById('user-email');
const userIntroEl = document.getElementById('user-intro');
const diaryCountEl = document.getElementById('diary-count');
const emotionTrendCanvas = document.getElementById('emotion-trend-chart');
const emotionStatisticsCanvas = document.getElementById('emotion-statistics-chart');
const editProfileBtn = document.getElementById('edit-profile-btn');

function getEmotionFromScore(score) {
  switch (score) {
    case 3: return '😊';
    case 2: return '😐';
    case 1: return '😢';
    case 0: return '😡';
    default: return '😐';
  }
}

async function loadUserProfile() {
  try {
    const res = await fetch(`${baseURL}/log/user/profile`, {
      headers: {
        'Authorization': 'Bearer ' + getToken()
      }
    });
    const data = await res.json();
    userNameEl.textContent = data.username || '未知用户';
    userEmailEl.textContent = data.email || '无邮箱';
    userIntroEl.textContent = data.signature || '这个人很神秘，没有留下任何签名。';
    diaryCountEl.textContent = `${data.log_count || 0} 条`;
  } catch (err) {
    console.error('加载用户资料失败:', err);
  }
}

async function loadEmotionTrend() {
  try {
    const res = await fetch(`${baseURL}/api/emotions?filter=week`, {
      headers: {
        'Authorization': 'Bearer ' + getToken()
      }
    });
    const result = await res.json();
    new Chart(emotionTrendCanvas.getContext('2d'), {
      type: 'line',
      data: {
        labels: result.labels,
        datasets: [{
          label: '情绪变化',
          data: result.data,
          borderColor: '#FF90BC',
          backgroundColor: 'rgba(255, 144, 188, 0.2)',
          borderWidth: 2,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            ticks: {
              stepSize: 1,
              callback: getEmotionFromScore
            }
          }
        }
      }
    });
  } catch (err) {
    console.error('加载情绪趋势失败:', err);
  }
}

async function loadEmotionStatistics() {
  try {
    const now = new Date();
    const res = await fetch(`${baseURL}/api/emotions?filter=month&year=${now.getFullYear()}&month=${now.getMonth() + 1}`, {
      headers: {
        'Authorization': 'Bearer ' + getToken()
      }
    });
    const result = await res.json();
    const count = [0, 0, 0, 0];
    result.data.forEach(score => count[score]++);
    new Chart(emotionStatisticsCanvas.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['😡 生气', '😢 悲伤', '😐 平静', '😊 开心'],
        datasets: [{
          label: '出现次数',
          data: count,
          backgroundColor: ['#F87171', '#60A5FA', '#FBBF24', '#34D399']
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            stepSize: 1
          }
        }
      }
    });
  } catch (err) {
    console.error('加载情绪统计失败:', err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadUserProfile();
  loadEmotionTrend();
  loadEmotionStatistics();

  editProfileBtn.addEventListener('click', () => {
    window.location.href = 'profile-edit.html';
  });
});


document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("token");  // 清除JWT
  alert("您已成功退出登录！");
  window.location.href = "index.html";  //返回主页面
});
