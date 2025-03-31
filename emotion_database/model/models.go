package model

import "time"

type User struct {
	ID        uint   `gorm:"primaryKey"`
	Username  string `gorm:"unique;not null"`
	Email     string
	Password  string `gorm:"not null"`
	CreatedAt time.Time
	Signature string // Added Signature field
	Avatar    string // Added Avatar field
}

type EmotionInteraction struct {
	ID           uint      `gorm:"primaryKey"`
	UserID       uint      `gorm:"not null"`
	Text         string    // 用户说的话
	VideoPath    string    // 情绪小人视频
	AudioPath    string    // 系统生成音频
	EmotionLabel string    // 情绪标签（如 joy, sad, angry）
	Suggestion   string    // AI agent 提议
	NetworkState string    // 网络状态（例如 "wifi", "4g", "offline"）
	Timestamp    time.Time `gorm:"autoCreateTime"`
	WeekInMonth  int       // 属于该月的第几周
}

type CommunityPost struct {
	ID        uint      `gorm:"primaryKey"`
	UserID    uint      `gorm:"not null"`          // 日志发布者
	Content   string    `gorm:"type:text"`         // 日志内容
	Likes     int       `gorm:"default:0"`         // 点赞数
	Comments  []Comment `gorm:"foreignKey:PostID"` // 评论列表
	CreatedAt time.Time `gorm:"autoCreateTime"`    // 创建时间
}

type Comment struct {
	ID        uint      `gorm:"primaryKey"`
	PostID    uint      `gorm:"not null"`       // 所属日志
	AuthorID  uint      `gorm:"not null"`       // 评论者
	Content   string    `gorm:"type:text"`      // 评论内容
	CreatedAt time.Time `gorm:"autoCreateTime"` // 评论时间
}

// CalcWeekInMonth returns the week number (1-based) of the given time in its month.
func CalcWeekInMonth(t time.Time) int {
	day := t.Day()
	weekday := int(t.Weekday())
	if weekday == 0 {
		weekday = 7 // make Sunday = 7
	}
	// Calculate which week the date falls in
	return (day+weekday-1)/7 + 1
}
