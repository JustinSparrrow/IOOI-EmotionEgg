package config

import (
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/joho/godotenv"
)

// Config 聚合应用运行所需的全部配置。
// 约定：业务代码只从这里取配置，不再直接调用 os.Getenv，
// 这样配置的来源和默认值只有一个地方可以追溯。
type Config struct {
	DB     DBConfig
	Server ServerConfig
	JWT    JWTConfig
}

// DBConfig 数据库连接参数。
type DBConfig struct {
	Host     string
	Port     string
	User     string
	Password string
	Name     string
	SSLMode  string
}

// DSN 拼装 PostgreSQL 连接串。
// 把拼装逻辑收在此处，避免 db.go 和各处脚本重复写格式化字符串。
func (d DBConfig) DSN() string {
	return fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		d.Host, d.Port, d.User, d.Password, d.Name, d.SSLMode,
	)
}

// ServerConfig HTTP 服务参数。
type ServerConfig struct {
	Port           string
	TrustedProxies []string
}

// JWTConfig 令牌签发参数。
type JWTConfig struct {
	Secret string
	Expire time.Duration
}

var current *Config

// placeholderSecret 与 .env.example 中保持一致。
// 一旦出现在运行环境里，说明使用者直接复制了模板而未替换密钥。
const placeholderSecret = "change_me_to_a_random_32_byte_secret"

// Load 读取配置并缓存。
//
// 优先级：进程环境变量 > .env 文件 > 代码内默认值。
// 容器部署时通常不存在 .env 文件，配置由编排工具注入环境变量，
// 因此文件缺失只提示、不中断。
func Load() *Config {
	if err := godotenv.Load(); err != nil {
		log.Println("[config] 未发现 .env 文件，使用系统环境变量")
	} else {
		log.Println("[config] 已加载 .env 文件")
	}

	cfg := &Config{
		DB: DBConfig{
			Host:     getEnv("DB_HOST", "localhost"),
			Port:     getEnv("DB_PORT", "5432"),
			User:     getEnv("DB_USER", "postgres"),
			Password: getEnv("DB_PASSWORD", ""),
			Name:     getEnv("DB_NAME", "emotion_app"),
			SSLMode:  getEnv("DB_SSLMODE", "disable"),
		},
		Server: ServerConfig{
			Port:           getEnv("SERVER_PORT", "8080"),
			TrustedProxies: splitAndTrim(getEnv("TRUSTED_PROXIES", "127.0.0.1")),
		},
		JWT: JWTConfig{
			Secret: getEnv("JWT_SECRET", ""),
			Expire: time.Duration(getEnvInt("JWT_EXPIRE_HOURS", 72)) * time.Hour,
		},
	}

	// 密钥缺失时让服务启动失败，而不是带着空密钥继续对外提供服务。
	// 空密钥意味着任何人都能伪造 token，这属于不可接受的降级。
	// 同时拦截模板占位值：.env.example 里的默认串是公开的，
	// 若原样使用，等同于把签名密钥直接公布在仓库里。
	if cfg.JWT.Secret == "" || cfg.JWT.Secret == placeholderSecret {
		log.Fatal("[config] JWT_SECRET 未设置或仍为模板占位值，拒绝启动。生成命令: openssl rand -base64 32")
	}

	current = cfg
	return cfg
}

// Get 返回已加载的配置。
// 未初始化即视为编程错误，直接终止，调用方无需再做 nil 判断。
func Get() *Config {
	if current == nil {
		log.Fatal("[config] 配置未初始化，请先在 main 中调用 config.Load()")
	}
	return current
}

// getEnv 读取环境变量，为空时回退到默认值。
// 注意：设置了但内容为空字符串的变量也按“未设置”处理，
// 这样 .env.example 里留空的项不会意外覆盖默认值。
func getEnv(key, fallback string) string {
	if v := strings.TrimSpace(os.Getenv(key)); v != "" {
		return v
	}
	return fallback
}

// getEnvInt 读取整数型配置，非法值回退默认值并告警。
func getEnvInt(key string, fallback int) int {
	raw := strings.TrimSpace(os.Getenv(key))
	if raw == "" {
		return fallback
	}
	var n int
	if _, err := fmt.Sscanf(raw, "%d", &n); err != nil || n <= 0 {
		log.Printf("[config] %s=%q 非法，回退默认值 %d", key, raw, fallback)
		return fallback
	}
	return n
}

// splitAndTrim 把逗号分隔的配置切成切片，过滤空项。
func splitAndTrim(raw string) []string {
	parts := strings.Split(raw, ",")
	out := make([]string, 0, len(parts))
	for _, p := range parts {
		if v := strings.TrimSpace(p); v != "" {
			out = append(out, v)
		}
	}
	return out
}
