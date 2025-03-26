package controller

import (
	"emotion_database/database"
	"emotion_database/model"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// CreateCommunityPost POST /community/post
func CreateCommunityPost(c *gin.Context) {
	userID := c.MustGet("user_id").(float64)

	var input struct {
		Content string `json:"content" binding:"required"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	post := model.CommunityPost{
		UserID:    uint(userID),
		Content:   input.Content,
		Likes:     0,
		CreatedAt: time.Now(),
	}
	if err := database.DB.Create(&post).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create post"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Post created"})
}

// GetCommunityPosts GET /community/posts
func GetCommunityPosts(c *gin.Context) {
	var posts []model.CommunityPost
	if err := database.DB.Preload("Comments").Find(&posts).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to load posts"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"data": posts})
}
