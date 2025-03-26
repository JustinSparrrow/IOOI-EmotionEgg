package controller

import (
	"emotion_database/database"
	"emotion_database/model"
	"github.com/golang-jwt/jwt/v5"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
)

type RegisterInput struct {
	Username string `json:"username" binding:"required"`
	Email    string `json:"email"`
	Password string `json:"password" binding:"required"`
}

func Register(c *gin.Context) {
	var input RegisterInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// 加密密码
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(input.Password), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to encrypt password"})
		return
	}

	user := model.User{
		Username: input.Username,
		Email:    input.Email,
		Password: string(hashedPassword),
	}

	result := database.DB.Create(&user)
	if result.Error != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": result.Error.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Register success"})
}

type LoginInput struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func Login(c *gin.Context) {
	var input LoginInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var user model.User
	if err := database.DB.Where("username = ?", input.Username).First(&user).Error; err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid username or password"})
		return
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(input.Password)); err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid username or password"})
		return
	}

	// Create JWT token
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"user_id": user.ID,
		"exp":     time.Now().Add(time.Hour * 72).Unix(), // 3天有效
	})

	// Secret 密钥（后续可移到 config）
	tokenString, err := token.SignedString([]byte("mysecret"))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create token"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"token": tokenString})
}

func UpdateProfile(c *gin.Context) {
	userID := c.MustGet("user_id").(float64)

	var input struct {
		Signature string `json:"signature"`
		Avatar    string `json:"avatar"`
	}
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var user model.User
	if err := database.DB.First(&user, uint(userID)).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "User not found"})
		return
	}

	// 更新字段
	user.Signature = input.Signature
	user.Avatar = input.Avatar

	if err := database.DB.Save(&user).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update profile"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Profile updated"})
}

func GetProfile(c *gin.Context) {
	userID := c.MustGet("user_id").(float64)

	var user model.User
	if err := database.DB.First(&user, uint(userID)).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "User not found"})
		return
	}

	var count int64
	database.DB.Model(&model.EmotionInteraction{}).Where("user_id = ?", uint(userID)).Count(&count)

	c.JSON(http.StatusOK, gin.H{
		"username":  user.Username,
		"signature": user.Signature,
		"avatar":    user.Avatar,
		"log_count": count,
	})
}

func GetLatestInteraction(c *gin.Context) {
	userID := c.MustGet("user_id").(float64)

	var interaction model.EmotionInteraction
	if err := database.DB.
		Where("user_id = ?", uint(userID)).
		Order("timestamp DESC").
		First(&interaction).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "No interaction found"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"text":          interaction.Text,
		"audio_path":    interaction.AudioPath,
		"video_path":    interaction.VideoPath,
		"emotion_label": interaction.EmotionLabel,
		"suggestion":    interaction.Suggestion,
		"timestamp":     interaction.Timestamp,
	})
}
