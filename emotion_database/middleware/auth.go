package middleware

import (
	"emotion_database/config"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

// AuthMiddleware 校验 Authorization 头中的 Bearer Token。
// 校验通过后把 user_id 写入上下文，供后续 handler 取用。
func AuthMiddleware() gin.HandlerFunc {
	secret := []byte(config.Get().JWT.Secret)

	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" || !strings.HasPrefix(authHeader, "Bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "缺少或格式错误的 Authorization 头"})
			return
		}

		tokenStr := strings.TrimPrefix(authHeader, "Bearer ")

		// 必须显式限定签名算法。
		// 若不限定，攻击者可将 header 中的 alg 改为 none，或换成其他算法族，
		// 利用解析器"按 token 自称的算法去验证"的行为绕过签名检查（alg 混淆攻击）。
		token, err := jwt.Parse(
			tokenStr,
			func(token *jwt.Token) (interface{}, error) {
				return secret, nil
			},
			jwt.WithValidMethods([]string{jwt.SigningMethodHS256.Alg()}),
		)
		if err != nil || !token.Valid {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "无效的 Token"})
			return
		}

		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "无法解析 Token 载荷"})
			return
		}

		// 保存 user_id 到上下文中
		c.Set("user_id", claims["user_id"])
		c.Next()
	}
}
