package controller

import (
	"emotion_database/database"
	"emotion_database/model"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type CreateLogInput struct {
	VideoPath    string `json:"video_path"`
	AudioPath    string `json:"audio_path"`
	EmotionState int    `json:"emotion_state"`
	NetworkState string `json:"network_state"`
	WeekInMonth  int    `json:"week_in_month"`
}

func CreateEmotionLog(c *gin.Context) {
	var input CreateLogInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	userID := c.MustGet("user_id").(float64)

	log := model.EmotionLog{
		UserID:       uint(userID),
		VideoPath:    input.VideoPath,
		AudioPath:    input.AudioPath,
		EmotionState: input.EmotionState,
		NetworkState: input.NetworkState,
		WeekInMonth:  input.WeekInMonth,
		Timestamp:    time.Now(),
	}

	if err := database.DB.Create(&log).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create log"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Log created"})
}

func ListEmotionLogs(c *gin.Context) {
	userID := c.MustGet("user_id").(float64)

	var logs []model.EmotionLog
	if err := database.DB.Where("user_id = ?", uint(userID)).Find(&logs).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch logs"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": logs})
}
