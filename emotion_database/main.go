package main

import (
	"emotion_database/database"
	"emotion_database/router"
)

func main() {
	database.InitDB() // ✅ 添加这一行来初始化 DB 连接
	r := router.SetupRouter()
	err := r.SetTrustedProxies([]string{"127.0.0.1"})
	if err != nil {
		return
	} // 🟢 设置可信代理
	err = r.Run(":8080")
	if err != nil {
		return
	} // ✅ 必须有冒号
}
