# 运维学习进度

## 已完成 ✅

### Linux基础
- 常用命令：pwd、mkdir、cp、mv、rm、vim、cat、grep、tail
- 输出重定向 > 和 >>
- crontab定时任务

### Git
- git init、add、commit、push
- 分支操作
- GitHub远程仓库

### Python
- 变量、if/elif/else、for循环
- 字典、列表、函数
- 文件读写、按行读日志挑ERROR
- subprocess调用Linux命令
- requests发HTTP请求（钉钉告警）
- try/except异常处理

### Docker
- 安装Docker + 国内镜像加速器
- docker run/ps/images/stop/rm/logs/exec
- Nginx容器（8082）、MySQL容器（3306）
- 数据卷挂载 -v（加:z解决SELinux）
- docker-compose一键启动多容器

### Prometheus监控
- Prometheus跑起来（9090）
- node_exporter采集服务器指标（9100）
- 配置prometheus.yml采集target
- 常用查询：CPU使用率、内存使用率、磁盘使用率
- 告警规则 alert_rules.yml
- 告警状态：PENDING → FIRING

### Ansible批量运维
- 安装ansible（2.14.18）
- 配置主机清单 ansible_hosts
- SSH免密登录（ssh-keygen + ssh-copy-id）
- ad-hoc命令：ping模块、shell模块远程执行命令
- Playbook剧本：批量执行多个任务
- dnf模块：远程安装软件（become: yes）
- copy模块：远程创建/写文件
- service模块：远程重启服务

## 进行中 🔵
- Alertmanager告警自动发钉钉

## 复习小测 🔁
- 每个工作日晚上 8 点自动出题检测（一题一题作答，逐题批改）
- 历史记录与易错点：见 [docs/review-log.md](review-log.md)
- 最近一次（2026-11-11）：已答 3 题、 2 对 1 错（`mv` ✅、`cat` ❌、`tail` ✅），第 4 题 `>` 重定向未答
- 前一次（2026-11-10）：首轮 3 对 2 错 1 半对，补强 3 题全对；延伸题 4 题 2 对 2 待巩固
- 待补薄弱点：`cd` 与 `cat` 的区别、`tail -f` 的 `-f`、`>` 与 `>>` 的区别（pwd/ls、rm 无回收站、grep 顺序已补齐）

## 待学习 ⬜
- K8s容器编排
- Terraform基础设施即代码
