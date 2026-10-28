package database

import (
	"emotion_database/config"
	"emotion_database/model"
	"fmt"
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// DB 全局数据库句柄。
// 这是当前的阶段性取舍：让 controller 可以直接使用。
// 后续引入 service 层时会改为依赖注入，去掉这个包级变量。
var DB *gorm.DB

// InitDB 连接数据库并执行自动迁移。
// 前置条件：调用方必须已执行 config.Load()，配置才有值。
func InitDB() {
	cfg := config.Get()

	db, err := gorm.Open(postgres.Open(cfg.DB.DSN()), &gorm.Config{})
	if err != nil {
		log.Fatal("数据库连接失败: ", err)
	}

	// 自动迁移：让表结构与 model 定义保持一致。
	// 注意 AutoMigrate 只做增量补齐，不会删除旧字段，
	// 因此它适合开发期快速迭代，不适合作为生产环境的版本化迁移方案。
	err = db.AutoMigrate(
		&model.User{},
		&model.EmotionInteraction{},
		&model.CommunityPost{},
		&model.Comment{},
	)
	if err != nil {
		log.Fatal("数据库迁移失败: ", err)
	}

	DB = db
	fmt.Printf("数据库已连接并完成迁移: %s@%s:%s/%s\n",
		cfg.DB.User, cfg.DB.Host, cfg.DB.Port, cfg.DB.Name)
}
