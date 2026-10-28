package main

import (
	"emotion_database/config"
	"emotion_database/database"
	"emotion_database/router"
	"log"
)

func main() {
	// 配置必须最先加载，database 与 middleware 都依赖它。
	cfg := config.Load()

	database.InitDB()

	r := router.SetupRouter()

	// 限制可信代理，避免客户端伪造 X-Forwarded-For 污染日志与限流依据。
	if err := r.SetTrustedProxies(cfg.Server.TrustedProxies); err != nil {
		log.Fatalf("设置可信代理失败: %v", err)
	}

	addr := ":" + cfg.Server.Port
	log.Printf("服务启动于 http://localhost%s", addr)

	// 启动失败必须以非零状态码退出，否则容器与 CI 无法感知异常。
	if err := r.Run(addr); err != nil {
		log.Fatalf("HTTP 服务启动失败: %v", err)
	}
}
