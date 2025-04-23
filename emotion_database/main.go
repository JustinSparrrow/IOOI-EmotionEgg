package main

import (
	"emotion_database/database"
	"emotion_database/router"
)

func main() {
	database.InitDB() //
	r := router.SetupRouter()
	err := r.SetTrustedProxies([]string{"127.0.0.1"})
	if err != nil {
		return
	} // 设置可信代理
	err = r.Run(":8080")
	if err != nil {
		return
	}
}
