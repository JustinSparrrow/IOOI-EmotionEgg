package controller

import (
	"emotion_database/database"
	"emotion_database/model"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

/*
case 3: return "😊";
case 2: return "😐";
case 1: return "😢";
case 0: return "😡";
default: return "😐";
*/

type UploadEmotionInput struct {
	UserID       uint   `json:"user_id" binding:"required"`
	Text         string `json:"text" binding:"required"`
	VideoPath    string `json:"video_path" binding:"required"`
	AudioPath    string `json:"audio_path" binding:"required"`
	EmotionLabel string `json:"emotion_label" binding:"required"`
	Suggestion   string `json:"suggestion"`
}

func UploadEmotion(c *gin.Context) {
	var input UploadEmotionInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	now := time.Now()
	weekInMonth := getWeekInMonth(now)

	record := model.EmotionInteraction{
		UserID:       input.UserID,
		Text:         input.Text,
		VideoPath:    input.VideoPath,
		AudioPath:    input.AudioPath,
		EmotionLabel: input.EmotionLabel,
		Suggestion:   input.Suggestion,
		Timestamp:    now,
		WeekInMonth:  weekInMonth,
	}

	if err := database.DB.Create(&record).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "保存失败"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "上传成功"})
}

func getWeekInMonth(t time.Time) int {
	_, firstWeek := time.Date(t.Year(), t.Month(), 1, 0, 0, 0, 0, t.Location()).ISOWeek()
	_, currentWeek := t.ISOWeek()
	return currentWeek - firstWeek + 1
}

// GetEmotionYears GET /api/emotion-years?user_id=1
func GetEmotionYears(c *gin.Context) {
	userIDStr := c.Query("user_id")
	if userIDStr == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "user_id required"})
		return
	}

	var years []int
	err := database.DB.
		Model(&model.EmotionInteraction{}).
		Select("DISTINCT EXTRACT(YEAR FROM timestamp)::int").
		Where("user_id = ?", userIDStr).
		Pluck("EXTRACT(YEAR FROM timestamp)", &years).Error

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get years"})
		return
	}

	c.JSON(http.StatusOK, years)
}

// GetDominantEmotionByTime GET /api/emotions/dominant?filter=year|month|week|day&user_id=1
func GetDominantEmotionByTime(c *gin.Context) {
	filter := c.Query("filter")
	userID := c.Query("user_id")
	year := c.Query("year")
	month := c.Query("month")
	day := c.Query("day") // 获取 day 参数
	if userID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "user_id required"})
		return
	}

	var results []struct {
		Label        string
		EmotionLabel string
		Text         string
		Suggestion   string
	}
	query := database.DB.Model(&model.EmotionInteraction{}).Where("user_id = ?", userID)

	switch filter {
	case "year":
		query = query.Where("emotion_label IS NOT NULL AND emotion_label != ''").
			Select("TO_CHAR(timestamp, 'YYYY-MM') AS label, mode() WITHIN GROUP (ORDER BY emotion_label) AS emotion_label").
			Group("label").
			Order("label")

	case "month":
		query = query.Where("emotion_label IS NOT NULL AND emotion_label != ''").
			Where("EXTRACT(YEAR FROM timestamp) = ? AND EXTRACT(MONTH FROM timestamp) = ?", year, month).
			Select("CONCAT('Week ', week_in_month) AS label, mode() WITHIN GROUP (ORDER BY emotion_label) AS emotion_label").
			Group("label").
			Order("label")

	case "day":
		if year == "" || month == "" || day == "" { // 添加 day 参数校验
			c.JSON(http.StatusBadRequest, gin.H{"error": "year, month and day required"})
			return
		}
		query = query.Where("EXTRACT(YEAR FROM timestamp) = ? AND EXTRACT(MONTH FROM timestamp) = ? AND EXTRACT(DAY FROM timestamp) = ?", year, month, day).
			Select("TO_CHAR(timestamp, 'HH24:00') AS label, emotion_label, text, suggestion").
			Order("label")

	case "week":
		if year == "" || month == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "year and month required"})
			return
		}
		query = query.Where("emotion_label IS NOT NULL AND emotion_label != ''").
			Where("EXTRACT(YEAR FROM timestamp) = ? AND EXTRACT(MONTH FROM timestamp) = ?", year, month).
			Select("TO_CHAR(timestamp, 'YYYY-MM-DD') AS label, mode() WITHIN GROUP (ORDER BY emotion_label) AS emotion_label").
			Group("label").
			Order("label")

	default:
		c.JSON(http.StatusBadRequest, gin.H{"error": "Unsupported filter"})
		return
	}

	if err := query.Scan(&results).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	if len(results) == 0 {
		c.JSON(http.StatusOK, gin.H{"data": map[string]string{}})
		return
	}
	emotionData := make(map[string]map[string]string) // 每个 label 对应一个 map

	for _, r := range results {
		emotionData[r.Label] = map[string]string{
			"emotion_label": r.EmotionLabel,
			"text":          r.Text,
			"suggestion":    r.Suggestion,
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"data": emotionData,
	})

}

// GetAllEmotions GET /api/emotion/all?user_id=1
func GetAllEmotions(c *gin.Context) {
	userID := c.Query("user_id")
	if userID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "user_id required"})
		return
	}

	type EmotionRecord struct {
		Text         string    `json:"text"`
		EmotionLabel string    `json:"emotion_label"`
		Timestamp    time.Time `json:"timestamp"`
	}

	var records []EmotionRecord
	if err := database.DB.
		Model(&model.EmotionInteraction{}).
		Select("text, emotion_label, timestamp").
		Where("user_id = ?", userID).
		Order("timestamp desc").
		Find(&records).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get emotion records"})
		return
	}

	c.JSON(http.StatusOK, records)
}
