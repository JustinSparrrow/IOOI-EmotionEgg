package router

import (
	"emotion_database/controller"
	"emotion_database/middleware"
	"github.com/gin-gonic/gin"
)

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}

func SetupRouter() *gin.Engine {
	r := gin.Default()
	r.Use(CORSMiddleware())

	api := r.Group("/api")
	{
		api.POST("/emotion/upload", controller.UploadEmotion)
		api.GET("/emotion-years", controller.GetEmotionYears)
		api.GET("/emotions/dominant", controller.GetDominantEmotionByTime)
	}

	user := r.Group("/user")
	{
		user.POST("/register", controller.Register)
		user.POST("/login", controller.Login)
	}

	protected := r.Group("/log")
	protected.Use(middleware.AuthMiddleware())
	{
		protected.GET("/user/profile", controller.GetProfile)
		protected.PUT("/user/profile", controller.UpdateProfile)
		protected.POST("/community/post", controller.CreateCommunityPost)
		protected.GET("/community/posts", controller.GetCommunityPosts)
		protected.GET("/user/lastInteraction", controller.GetLatestInteraction)
	}

	return r
}
