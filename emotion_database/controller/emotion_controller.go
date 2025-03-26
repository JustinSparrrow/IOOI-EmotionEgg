package controller

import (
	"emotion_database/database"
	"emotion_database/model"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

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

	record := model.EmotionInteraction{
		UserID:       input.UserID,
		Text:         input.Text,
		VideoPath:    input.VideoPath,
		AudioPath:    input.AudioPath,
		EmotionLabel: input.EmotionLabel,
		Suggestion:   input.Suggestion,
		Timestamp:    time.Now(),
	}

	if err := database.DB.Create(&record).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "保存失败"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "上传成功"})
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

// GetEmotionStats GET /api/emotions?filter=year&year=2025&user_id=1
func GetEmotionStats(c *gin.Context) {
	filter := c.Query("filter")
	userID := c.Query("user_id")
	if userID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "user_id required"})
		return
	}

	var labels []string
	var data []int

	type Result struct {
		Label string
		Avg   float64
	}

	var results []Result
	query := database.DB.Model(&model.EmotionInteraction{}).Where("user_id = ?", userID)

	switch filter {
	case "year":
		year := c.Query("year")
		query = query.Where("EXTRACT(YEAR FROM timestamp) = ?", year).
			Select("TO_CHAR(timestamp, 'Mon') AS label, ROUND(AVG(emotion_label::int)) AS avg").
			Group("label").Order("MIN(EXTRACT(MONTH FROM timestamp))")
	case "month":
		year := c.Query("year")
		month := c.Query("month")
		query = query.Where("EXTRACT(YEAR FROM timestamp) = ? AND EXTRACT(MONTH FROM timestamp) = ?", year, month).
			Select("CONCAT('Week ', week_in_month) AS label, ROUND(AVG(emotion_label::int)) AS avg").
			Group("label").Order("MIN(week_in_month)")
	default:
		c.JSON(http.StatusBadRequest, gin.H{"error": "Unsupported filter"})
		return
	}

	if err := query.Scan(&results).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to query data"})
		return
	}

	for _, r := range results {
		labels = append(labels, r.Label)
		data = append(data, int(r.Avg))
	}

	c.JSON(http.StatusOK, gin.H{
		"labels": labels,
		"data":   data,
	})
}
