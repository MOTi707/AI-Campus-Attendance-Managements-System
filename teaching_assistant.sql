/*
 Navicat Premium Data Transfer

 Source Server         : a
 Source Server Type    : MySQL
 Source Server Version : 80038 (8.0.38)
 Source Host           : localhost:3306
 Source Schema         : teaching_assistant

 Target Server Type    : MySQL
 Target Server Version : 80038 (8.0.38)
 File Encoding         : 65001

 Date: 10/12/2025 00:20:47
*/
CREATE DATABASE IF NOT EXISTS teaching_assistant;
use teaching_assistant;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for attendance_records
-- ----------------------------
DROP TABLE IF EXISTS `attendance_records`;
CREATE TABLE `attendance_records`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `teacher_id` int NOT NULL,
  `student_id` int NOT NULL,
  `check_in_time` timestamp NULL DEFAULT NULL,
  `check_in_method` enum('qr_code','manual') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'qr_code',
  `check_in_location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `is_present` tinyint NULL DEFAULT 1,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_task_student`(`task_id` ASC, `student_id` ASC) USING BTREE,
  INDEX `teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_task_id`(`task_id` ASC) USING BTREE,
  INDEX `idx_student_id`(`student_id` ASC) USING BTREE,
  CONSTRAINT `attendance_records_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `attendance_tasks` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `attendance_records_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `attendance_records_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of attendance_records
-- ----------------------------

-- ----------------------------
-- Table structure for attendance_tasks
-- ----------------------------
DROP TABLE IF EXISTS `attendance_tasks`;
CREATE TABLE `attendance_tasks`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int NOT NULL,
  `task_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `class_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `subject` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `task_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` enum('pending','in_progress','completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'pending',
  `start_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `expected_count` int NULL DEFAULT 0,
  `actual_count` int NULL DEFAULT 0,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `task_code`(`task_code` ASC) USING BTREE,
  INDEX `idx_teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE,
  INDEX `idx_task_code`(`task_code` ASC) USING BTREE,
  CONSTRAINT `attendance_tasks_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of attendance_tasks
-- ----------------------------
INSERT INTO `attendance_tasks` VALUES (1, 18, '2025-12-10 ', '2320', '计算机', 'TASK20251210000401d3e9d9ee', 'pending', NULL, NULL, 10, 0, '', '2025-12-09 16:04:01', '2025-12-09 16:04:01', NULL);
INSERT INTO `attendance_tasks` VALUES (2, 18, '1', '2', '', 'TASK202512100008492098a888', 'pending', NULL, NULL, 0, 0, '1', '2025-12-09 16:08:50', '2025-12-09 16:08:50', NULL);

-- ----------------------------
-- Table structure for barrage_likes
-- ----------------------------
DROP TABLE IF EXISTS `barrage_likes`;
CREATE TABLE `barrage_likes`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '点赞ID',
  `message_id` int NOT NULL COMMENT '消息ID',
  `student_id` int NOT NULL COMMENT '学生ID',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `message_id`(`message_id` ASC) USING BTREE,
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  CONSTRAINT `barrage_likes_ibfk_1` FOREIGN KEY (`message_id`) REFERENCES `barrage_messages` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `barrage_likes_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of barrage_likes
-- ----------------------------

-- ----------------------------
-- Table structure for barrage_messages
-- ----------------------------
DROP TABLE IF EXISTS `barrage_messages`;
CREATE TABLE `barrage_messages`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `student_id` int NOT NULL,
  `message_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `message_color` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '#333333',
  `is_pinned` tinyint NULL DEFAULT 0,
  `like_count` int NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  INDEX `idx_task_id`(`task_id` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `barrage_messages_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `interaction_tasks` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `barrage_messages_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of barrage_messages
-- ----------------------------
INSERT INTO `barrage_messages` VALUES (1, 4, 1, '老师讲得很清楚呢！', '#FF6B6B', 1, 15, '2025-12-07 22:00:41', NULL);
INSERT INTO `barrage_messages` VALUES (2, 4, 2, '二叉树的中序遍历怎么实现？', '#4ECDC4', 1, 12, '2025-12-07 22:01:41', NULL);
INSERT INTO `barrage_messages` VALUES (3, 4, 3, '我觉得递归的方式比较好理解', '#FFE66D', 0, 18, '2025-12-07 22:02:41', NULL);
INSERT INTO `barrage_messages` VALUES (4, 4, 4, '这个知识点在面试中经常考', '#95DE64', 0, 22, '2025-12-07 22:03:41', NULL);
INSERT INTO `barrage_messages` VALUES (5, 4, 5, '我完全同意，刚才看题目就懂了', '#FF85C0', 0, 9, '2025-12-07 22:04:41', NULL);
INSERT INTO `barrage_messages` VALUES (6, 4, 6, '能再讲一遍中序遍历吗？', '#40C057', 0, 11, '2025-12-07 22:05:41', NULL);
INSERT INTO `barrage_messages` VALUES (7, 4, 7, '总结得非常好，获益匪浅', '#FF6B6B', 0, 20, '2025-12-07 22:06:41', NULL);
INSERT INTO `barrage_messages` VALUES (8, 4, 8, '原来二叉树还有这么多应用场景', '#4ECDC4', 0, 17, '2025-12-07 22:07:11', NULL);
INSERT INTO `barrage_messages` VALUES (9, 4, 9, '下次课能讲平衡二叉树吗？', '#FFE66D', 0, 25, '2025-12-07 22:07:41', NULL);
INSERT INTO `barrage_messages` VALUES (10, 4, 10, '我把笔记都整理好了', '#95DE64', 0, 13, '2025-12-07 22:08:11', NULL);
INSERT INTO `barrage_messages` VALUES (11, 4, 1, '这是今年听过最清楚的讲解了', '#FF85C0', 0, 30, '2025-12-07 22:08:41', NULL);
INSERT INTO `barrage_messages` VALUES (12, 4, 2, '大家有什么疑问吗？', '#40C057', 0, 8, '2025-12-07 22:08:56', NULL);
INSERT INTO `barrage_messages` VALUES (13, 4, 3, '我有个问题，红黑树和AVL树的区别是什么？', '#FF6B6B', 0, 19, '2025-12-07 22:09:11', NULL);
INSERT INTO `barrage_messages` VALUES (14, 4, 4, '红黑树的自平衡比较复杂，但性能更好', '#4ECDC4', 0, 16, '2025-12-07 22:09:21', NULL);
INSERT INTO `barrage_messages` VALUES (15, 4, 5, '今天学到了很多东西，感谢老师！', '#FFE66D', 1, 35, '2025-12-07 22:09:31', NULL);

-- ----------------------------
-- Table structure for chat_conversations
-- ----------------------------
DROP TABLE IF EXISTS `chat_conversations`;
CREATE TABLE `chat_conversations`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '会ID',
  `teacher_id` int NOT NULL COMMENT '教师ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '会话标题',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `teacher_id`(`teacher_id` ASC) USING BTREE,
  CONSTRAINT `chat_conversations_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_conversations
-- ----------------------------
INSERT INTO `chat_conversations` VALUES (1, 18, '你有什么想法吗？你是什么模型？', '2025-12-09 13:31:57', '2025-12-09 15:50:16', NULL);

-- ----------------------------
-- Table structure for chat_messages
-- ----------------------------
DROP TABLE IF EXISTS `chat_messages`;
CREATE TABLE `chat_messages`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '消息ID',
  `conversation_id` int NOT NULL COMMENT '会话ID',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色: user/assistant',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息内容',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `conversation_id`(`conversation_id` ASC) USING BTREE,
  CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `chat_conversations` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 41 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_messages
-- ----------------------------
INSERT INTO `chat_messages` VALUES (27, 1, 'user', '如何安排Python大作业？', '2025-12-09 14:14:44');
INSERT INTO `chat_messages` VALUES (28, 1, 'assistant', '安排Python大作业需要综合考虑教学目标、学生水平和实践价值。以下是我的专业建议：\n\n1. **确定目标**\n- 明确考察重点：基础语法/算法/OOP/数据分析等\n- 建议分层设计：基础部分(60%)+拓展部分(40%)\n\n2. **题目设计**\n推荐5类实用选题方向：\n√ 数据处理分析(如疫情数据可视化)\n√ 实用小工具(如文件批量处理器)\n√ 简单游戏开发(如猜数字/井字棋)\n√ 网络爬虫应用(如天气数据获取)\n√ 算法实践(如路径规划模拟)\n\n3. **时间规划**\n- 建议周期：2-3周\n- 关键节点：\n  第1周：需求分析+设计方案\n  第2周：编码实现\n  第3周：测试优化+文档撰写\n\n4. **评估标准**\n建议包含：\n- 代码质量(40%)：规范性、可读性\n- 功能实现(30%)：完整性、正确性\n- 文档报告(20%)：说明文档、注释\n- 创新性(10%)：额外功能实现\n\n5. **实用建议**\n- 提供基础代码框架\n- 设置阶段性检查点\n- 鼓励使用Git进行版本管理\n- 要求提交README和使用说明\n\n是否需要我针对某个具体方向(如数据分析、游戏开发等)提供更详细的大作业设计方案？', '2025-12-09 14:14:59');
INSERT INTO `chat_messages` VALUES (29, 1, 'user', '查询学生成绩情况', '2025-12-09 14:15:50');
INSERT INTO `chat_messages` VALUES (30, 1, 'assistant', '关于查询学生成绩，我可以为您提供以下建议和信息：\n\n1. 常规查询方式：\n- 建议教师通过学校教务系统查询（请提供具体登录路径）\n- 班级成绩汇总表（Excel格式）通常包含：\n  * 学号、姓名\n  * 平时成绩\n  * 期中/期末成绩\n  * 总评成绩\n  * 备注栏\n\n2. 如需我协助分析：\n请提供：\n- 具体班级/课程名称\n- 想了解的统计维度（平均分、及格率、分数段分布等）\n- 特殊学生个案（如需重点关注的学生）\n\n3. 温馨提示：\n- 成绩发布前请务必核对无误\n- 注意保护学生隐私信息\n- 建议保留原始成绩记录备份\n\n您是需要查询某个具体班级的成绩，还是想了解成绩分析的技巧？我可以根据您的具体需求提供更针对性的建议。', '2025-12-09 14:16:05');
INSERT INTO `chat_messages` VALUES (31, 1, 'user', '查询学生成绩情况', '2025-12-09 14:23:10');
INSERT INTO `chat_messages` VALUES (32, 1, 'assistant', '作为教学助手，我需要说明：\n\n1. 关于学生成绩查询的权限：\n- 我无法直接访问学校的学生成绩数据库\n- 成绩信息属于个人隐私数据\n\n2. 建议您可以：\n\n对于教师：\n- 登录学校教务系统查询所教授课程的学生成绩\n- 如需协助分析成绩数据，我可以提供统计方法和教学改进建议\n\n对于学生：\n- 请通过学校官方成绩查询渠道查看\n- 如有疑问建议直接联系授课教师或教务处\n\n3. 其他我能提供的帮助：\n- 解释成绩评定标准\n- 提供成绩分析模板\n- 建议补考/重修的学习方法\n- 分享提升学业表现的策略\n\n您是否需要以上某一方面的具体帮助？', '2025-12-09 14:23:17');
INSERT INTO `chat_messages` VALUES (33, 1, 'user', '查询学生成绩情况', '2025-12-09 14:23:49');
INSERT INTO `chat_messages` VALUES (34, 1, 'assistant', '关于查询学生成绩情况，我可以为您提供以下帮助：\n\n1. 成绩管理系统查询：\n- 请提供学生姓名/学号和课程名称\n- 我可以告知您学校的成绩查询流程\n\n2. 成绩统计分析：\n- 可协助计算班级平均分、最高/最低分\n- 生成成绩分布图表（如需）\n\n3. 特殊查询需求：\n- 补考/重修学生名单\n- 成绩预警学生筛查\n- 特定分数段学生统计\n\n请注意：\n- 成绩信息属于敏感数据，需要验证教师身份\n- 建议通过学校官方教务系统查询最准确\n- 如需详细统计报告，建议联系教务处\n\n您是需要查询个别学生成绩，还是需要班级整体的成绩分析？我可以根据具体需求提供更详细的指导。', '2025-12-09 14:23:56');
INSERT INTO `chat_messages` VALUES (35, 1, 'user', '查询学生成绩情况', '2025-12-09 14:24:32');
INSERT INTO `chat_messages` VALUES (36, 1, 'assistant', '以下是三位学生的成绩概况及针对性建议：\n\n1. 张明远（优秀）\n- 成绩表现：作业均分92（100%完成），期中88（第3名）\n- 优势项：代码规范优秀，学习态度稳定\n- 薄弱点：接口vs抽象类（7分）、异常处理（5分）\n建议：提供企业级接口设计案例对比练习，补充异常处理最佳实践小测验\n\n2. 李晓萌（中等）\n- 成绩表现：作业均分75（85%完成），期中68（第22名）\n- 待改进：泛型通配符（作业3）、内存管理（期中-12分）、多线程（期中-15分）\n建议：安排内存可视化工具演示，设计泛型编码闯关游戏，推荐《Java并发编程实战》补充阅读\n\n3. 王浩宇（预警）\n- 成绩表现：作业均分58（60%完成），期中45（第38名）\n- 关键问题：作业延期4次、面向对象特性（期中-25分）、异常语法（期中-18分）\n建议：\n• 立即启动学习预警流程\n• 定制基础补救计划（含UML核心概念动画教程）\n• 强制代码格式化工具安装（IDEA-Alibaba插件）\n• 建议设立结对编程帮扶（推荐张明远作为导师）\n\n教学策略调整：\n1. 下周开设\"抽象概念诊所\"工作坊（针对前20%学生）\n2. 增加内存管理LAB实战环节（使用JVisualVM）\n3. 对预警学生启用每日代码提交打卡制度\n\n需特别注意：王浩宇的作业拖欠可能涉及学习动力问题，建议预约面谈了解深层原因。', '2025-12-09 14:24:46');
INSERT INTO `chat_messages` VALUES (37, 1, 'user', '如何安排Python大作业？', '2025-12-09 15:49:24');
INSERT INTO `chat_messages` VALUES (38, 1, 'assistant', '针对三位学生的学习情况，建议采用**分层任务设计**+**个性化指导**的方式安排Python大作业：\n\n---\n### **1. 分层任务设计**\n**A级任务（张明远）**  \n• 开发一个**Flask/Django小型Web系统**（如学生选课系统）  \n• 要求：  \n  - 实现MVC分层架构  \n  - 使用抽象类设计接口规范  \n  - 自定义异常处理模块  \n  - 附加：用多线程优化性能（结合期中薄弱点）  \n\n**B级任务（李晓萌）**  \n• 开发**数据分析工具**（如CSV文件处理器）  \n• 要求：  \n  - 使用泛型实现数据容器（强化泛型理解）  \n  - 通过上下文管理器处理资源（巩固内存管理）  \n  - 基础异常处理实现  \n\n**C级任务（王浩宇）**  \n• 完成**基础功能模块**（如银行账户管理系统）  \n• 要求：  \n  - 强制使用PEP8规范检查工具（解决代码混乱）  \n  - 用类图明确三大特征（封装/继承/多态）  \n  - 简化版异常处理（try-catch基础应用）  \n\n---\n### **2. 进度管理策略**\n| 学生     | 里程碑检查节点               | 特别关注点                   |\n|----------|------------------------------|------------------------------|\n| 张明远   | 架构设计评审→核心模块演示    | 接口设计的扩展性             |\n| 李晓萌   | 每周代码片段提交（Git）      | 泛型容器单元测试必交         |\n| 王浩宇   | 分阶段验收（3次）            | 首次验收重点检查代码规范     |\n\n---\n### **3. 配套支持**\n• 为王浩宇提供**代码模板**（含预置类结构）  \n• 给李晓萌推荐`memory_profiler`工具检测内存泄漏  \n• 要求张明远在答辩时**解释多线程设计取舍**  \n\n---\n**关键点**：  \n通过任务难度分级保持挑战性，同时针对期中薄弱环节设计必做项。建议设置**提前批改通道**，让张明远这类学生能迭代优化作品。', '2025-12-09 15:49:48');
INSERT INTO `chat_messages` VALUES (39, 1, 'user', '查询学生成绩情况', '2025-12-09 15:49:53');
INSERT INTO `chat_messages` VALUES (40, 1, 'assistant', '以下是三位学生的成绩情况汇总分析，建议采用分层辅导策略：\n\n**1. 张明远（优秀）**\n- 优势项：作业完成率100%（均分92）、代码规范优秀\n- 薄弱点：接口与抽象类区别、异常处理机制（期中失分重点）\n- 建议：提供高阶挑战任务（如设计模式实践项目），安排1次专项答疑重点讲解接口与抽象类的应用场景差异\n\n**2. 李晓萌（中等）**\n- 风险项：作业延期记录、泛型通配符理解模糊、内存管理/多线程薄弱\n- 关键数据：期中68分（低于班级平均线）\n- 建议：\n  - 每周固定时间进行泛型与内存管理专题辅导\n  - 布置补充练习（推荐《Java核心技术》第9章习题）\n  - 建立学习进度检查表（每周核对关键知识点）\n\n**3. 王浩宇（预警）**\n- 紧急问题：作业完成率仅60%、面向对象基础缺失、代码规范待改进\n- 干预建议：\n  - 立即启动面谈制定学习补救计划\n  - 要求重修核心章节（封装/继承/多态）\n  - 启用结对编程（安排张明远作为助教）\n  - 设置阶段性检查点（如每周提交代码片段）\n\n教学策略补充：建议在课程平台新增\"常见错误案例库\"，收录三类典型错误样本（可匿名使用王浩宇的格式问题作为反面案例）。\n\n需要我为您生成具体的学习补救计划模板或专题辅导材料吗？', '2025-12-09 15:50:16');

-- ----------------------------
-- Table structure for documents
-- ----------------------------
DROP TABLE IF EXISTS `documents`;
CREATE TABLE `documents`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '??ID',
  `teacher_id` int NOT NULL COMMENT '????ID',
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '???',
  `original_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '?????',
  `file_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '??????',
  `file_size` int NULL DEFAULT NULL COMMENT '????(??)',
  `file_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '????: pdf/doc/docx/pptx/txt?',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '????',
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '????',
  `keywords` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '??????(JSON??)',
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '??: ??/??/???',
  `sub_category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '???',
  `confidence_score` decimal(3, 2) NULL DEFAULT 0.00 COMMENT '?????(0-1)',
  `tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '??(JSON??)',
  `is_auto_classified` tinyint(1) NULL DEFAULT 0 COMMENT '??????',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '????',
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '????',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_category`(`category` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `documents_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '???' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of documents
-- ----------------------------
INSERT INTO `documents` VALUES (1, 18, '18_20251207124710_Web.docx', 'Web.docx', 'uploads/documents\\18_20251207124710_Web.docx', 30027, 'docx', '', '', '[]', '综合', '综合资料', 0.33, '[\"综合\", \"综合资料\"]', 1, '2025-12-07 12:47:11', '2025-12-07 23:14:47', NULL);
INSERT INTO `documents` VALUES (2, 18, '18_20251207130750_document.txt', 'document.txt', 'uploads/documents\\18_20251207130750_document.txt', 885, 'txt', '', '', '[\"存在\", \"fx\", \"实数\", \"二次\", \"函数\", \"图像\", \"直线\", \"坐标\", \"是否\", \"使得\"]', '数学', '高等数学', 0.86, '[\"数学\", \"高等数学\"]', 1, '2025-12-07 13:07:51', '2025-12-07 23:14:44', NULL);
INSERT INTO `documents` VALUES (3, 18, '18_20251207130816_document.txt', 'document.txt', 'uploads/documents\\18_20251207130816_document.txt', 1336, 'txt', '', '', '[\"函数\", \"抛物线\", \"顶点\", \"二次\", \"称为\", \"图像\", \"ax\", \"对称轴\", \"实根\", \"性质\"]', '数学', '高等数学', 0.95, '[\"数学\", \"高等数学\"]', 1, '2025-12-07 13:08:16', '2025-12-07 23:14:40', NULL);

-- ----------------------------
-- Table structure for interaction_tasks
-- ----------------------------
DROP TABLE IF EXISTS `interaction_tasks`;
CREATE TABLE `interaction_tasks`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int NOT NULL,
  `task_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `task_type` enum('poll','question','barrage') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `subject` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `status` enum('draft','active','completed') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'draft',
  `start_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `participation_count` int NULL DEFAULT 0,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_task_type`(`task_type` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE,
  CONSTRAINT `interaction_tasks_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of interaction_tasks
-- ----------------------------
INSERT INTO `interaction_tasks` VALUES (1, 18, 'Python基础知识问卷', 'question', 'Python编程', '考察学生对Python基础知识的理解', 'active', '2025-12-07 22:05:34', NULL, 0, '这是一个测试任务', '2025-12-07 22:05:34', '2025-12-07 22:05:34', NULL);
INSERT INTO `interaction_tasks` VALUES (2, 18, '课堂知识讨论', 'barrage', '数据结构与算法', '关于二叉树的实时课堂讨论', 'active', '2025-12-07 21:55:34', NULL, 0, '这是一个弹幕讨论任务', '2025-12-07 22:05:34', '2025-12-07 22:05:34', NULL);
INSERT INTO `interaction_tasks` VALUES (3, 18, 'Python基础知识问卷', 'question', 'Python编程', '考察学生对Python基础知识的理解', 'active', '2025-12-07 22:08:05', NULL, 0, '这是一个测试任务', '2025-12-07 22:08:05', '2025-12-07 22:08:05', NULL);
INSERT INTO `interaction_tasks` VALUES (4, 18, '课堂知识讨论', 'barrage', '数据结构与算法', '关于二叉树的实时课堂讨论', 'active', '2025-12-07 21:59:26', NULL, 0, '这是一个弹幕讨论任务', '2025-12-07 22:09:26', '2025-12-07 22:09:26', NULL);
INSERT INTO `interaction_tasks` VALUES (5, 18, '本节课重点理解吗？', 'poll', '数学讲座', '测试学生对本节课内容的理解程度', 'active', '2025-12-07 22:23:28', NULL, 15, '投票任务1', '2025-12-07 22:23:28', '2025-12-07 22:25:08', NULL);
INSERT INTO `interaction_tasks` VALUES (6, 18, '课程难度评估', 'poll', '进阶数学', '评估课程难度是否适当', 'active', '2025-12-07 22:24:07', NULL, 17, '投票任务2', '2025-12-07 22:24:07', '2025-12-07 22:25:08', NULL);

-- ----------------------------
-- Table structure for learning_predictions
-- ----------------------------
DROP TABLE IF EXISTS `learning_predictions`;
CREATE TABLE `learning_predictions`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '??ID',
  `student_id` int NOT NULL COMMENT '??ID',
  `teacher_id` int NOT NULL COMMENT '??ID',
  `predicted_grade` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '??????(A-D)',
  `predicted_score` decimal(5, 2) NULL DEFAULT NULL COMMENT '????',
  `confidence_score` decimal(3, 2) NULL DEFAULT 0.00 COMMENT '????',
  `analysis_text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '????',
  `suggestions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '??(JSON)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '????',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_student_id`(`student_id` ASC) USING BTREE,
  INDEX `idx_teacher_id`(`teacher_id` ASC) USING BTREE,
  CONSTRAINT `learning_predictions_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `learning_predictions_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '?????' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of learning_predictions
-- ----------------------------

-- ----------------------------
-- Table structure for learning_warnings
-- ----------------------------
DROP TABLE IF EXISTS `learning_warnings`;
CREATE TABLE `learning_warnings`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '??ID',
  `student_id` int NOT NULL COMMENT '??ID',
  `teacher_id` int NOT NULL COMMENT '??ID',
  `warning_level` enum('low','medium','high') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'low' COMMENT '????',
  `warning_reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '????',
  `subject` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '????',
  `status` enum('active','resolved') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'active' COMMENT '??',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '????',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_student_id`(`student_id` ASC) USING BTREE,
  INDEX `idx_teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_warning_level`(`warning_level` ASC) USING BTREE,
  CONSTRAINT `learning_warnings_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `learning_warnings_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '?????' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of learning_warnings
-- ----------------------------

-- ----------------------------
-- Table structure for poll_options
-- ----------------------------
DROP TABLE IF EXISTS `poll_options`;
CREATE TABLE `poll_options`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `option_text` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `option_order` int NULL DEFAULT 0,
  `vote_count` int NULL DEFAULT 0,
  `percentage` decimal(5, 2) NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_task_id`(`task_id` ASC) USING BTREE,
  CONSTRAINT `poll_options_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `interaction_tasks` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of poll_options
-- ----------------------------
INSERT INTO `poll_options` VALUES (1, 5, '非常理解', 1, 8, NULL, '2025-12-07 22:24:18');
INSERT INTO `poll_options` VALUES (2, 5, '基本理解', 2, 5, NULL, '2025-12-07 22:24:18');
INSERT INTO `poll_options` VALUES (3, 5, '不太理解', 3, 2, NULL, '2025-12-07 22:24:18');
INSERT INTO `poll_options` VALUES (4, 6, '太简单', 1, 2, NULL, '2025-12-07 22:24:25');
INSERT INTO `poll_options` VALUES (5, 6, '适中', 2, 12, NULL, '2025-12-07 22:24:25');
INSERT INTO `poll_options` VALUES (6, 6, '太难', 3, 3, NULL, '2025-12-07 22:24:25');

-- ----------------------------
-- Table structure for poll_votes
-- ----------------------------
DROP TABLE IF EXISTS `poll_votes`;
CREATE TABLE `poll_votes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `option_id` int NOT NULL,
  `student_id` int NOT NULL,
  `vote_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_task_student`(`task_id` ASC, `student_id` ASC) USING BTREE,
  INDEX `option_id`(`option_id` ASC) USING BTREE,
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  INDEX `idx_task_id`(`task_id` ASC) USING BTREE,
  CONSTRAINT `poll_votes_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `interaction_tasks` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `poll_votes_ibfk_2` FOREIGN KEY (`option_id`) REFERENCES `poll_options` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `poll_votes_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of poll_votes
-- ----------------------------
INSERT INTO `poll_votes` VALUES (1, 5, 1, 1, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (2, 5, 1, 2, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (3, 5, 1, 3, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (4, 5, 1, 4, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (5, 5, 1, 5, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (6, 5, 1, 6, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (7, 5, 1, 7, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (8, 5, 1, 8, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (9, 5, 2, 9, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (10, 5, 2, 10, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (11, 5, 2, 11, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (12, 5, 2, 12, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (13, 5, 2, 13, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (14, 5, 3, 14, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (15, 5, 3, 15, '2025-12-07 22:24:48');
INSERT INTO `poll_votes` VALUES (16, 6, 4, 1, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (17, 6, 4, 2, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (18, 6, 5, 3, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (19, 6, 5, 4, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (20, 6, 5, 5, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (21, 6, 5, 6, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (22, 6, 5, 7, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (23, 6, 5, 8, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (24, 6, 5, 9, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (25, 6, 5, 10, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (26, 6, 5, 11, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (27, 6, 5, 12, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (28, 6, 5, 13, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (29, 6, 6, 14, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (30, 6, 6, 15, '2025-12-07 22:24:58');
INSERT INTO `poll_votes` VALUES (31, 6, 6, 16, '2025-12-07 22:24:58');

-- ----------------------------
-- Table structure for question_answers
-- ----------------------------
DROP TABLE IF EXISTS `question_answers`;
CREATE TABLE `question_answers`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `student_id` int NOT NULL,
  `answer_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_correct` tinyint NULL DEFAULT NULL,
  `answer_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_question_student`(`question_id` ASC, `student_id` ASC) USING BTREE,
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  INDEX `idx_question_id`(`question_id` ASC) USING BTREE,
  CONSTRAINT `question_answers_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `question_answers_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of question_answers
-- ----------------------------

-- ----------------------------
-- Table structure for questions
-- ----------------------------
DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` int NOT NULL,
  `question_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `question_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` enum('pending','answered','closed') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'pending',
  `answer_count` int NULL DEFAULT 0,
  `correct_answer` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_task_id`(`task_id` ASC) USING BTREE,
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `interaction_tasks` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of questions
-- ----------------------------
INSERT INTO `questions` VALUES (1, 1, '什么是Python中的列表(list)？请说出它的三个主要特性。', 'essay', 'pending', 0, '有序，可变，可包含任何类型的对象', '2025-12-07 22:05:34');
INSERT INTO `questions` VALUES (2, 1, '如何在Python中创建一个字典？请给出一个例子。', 'essay', 'pending', 0, 'd = {\"key\": \"value\"}', '2025-12-07 22:05:34');
INSERT INTO `questions` VALUES (3, 1, '解释Python中的lambda函数是什么，并给出一个使用例子。', 'essay', 'pending', 0, 'lambda是匿名函数，例如: square = lambda x: x**2', '2025-12-07 22:05:34');
INSERT INTO `questions` VALUES (4, 1, '什么是Python中的装饰器(decorator)？', 'essay', 'pending', 0, '装饰器是修改或增强函数功能的函数', '2025-12-07 22:05:34');
INSERT INTO `questions` VALUES (5, 1, '如何在Python中处理异常？', 'essay', 'pending', 0, '使用try-except-else-finally语句块', '2025-12-07 22:05:34');

-- ----------------------------
-- Table structure for student_scores
-- ----------------------------
DROP TABLE IF EXISTS `student_scores`;
CREATE TABLE `student_scores`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '成绩ID',
  `student_id` int NOT NULL COMMENT '学生ID',
  `teacher_id` int NOT NULL COMMENT '教师ID',
  `subject` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '科目',
  `exam_number` int NULL DEFAULT NULL COMMENT '第几次考试',
  `score` float NOT NULL COMMENT '成绩',
  `full_score` float NULL DEFAULT NULL COMMENT '满分',
  `exam_date` date NULL DEFAULT NULL COMMENT '考试日期',
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '备注',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `deleted_at` datetime NULL DEFAULT NULL COMMENT '删除时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `student_id`(`student_id` ASC) USING BTREE,
  INDEX `teacher_id`(`teacher_id` ASC) USING BTREE,
  CONSTRAINT `student_scores_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `student_scores_ibfk_2` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 81 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student_scores
-- ----------------------------
INSERT INTO `student_scores` VALUES (1, 19, 18, '计算机技术', 1, 88, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (2, 19, 18, '计算机技术', 2, 92, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (3, 19, 18, '数据结构', 1, 85, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (4, 19, 18, 'Python编程', 1, 90, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (5, 19, 18, '算法设计', 1, 87, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (6, 20, 18, '计算机技术', 1, 75, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (7, 20, 18, '计算机技术', 2, 78, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (8, 20, 18, '数据结构', 1, 72, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (9, 20, 18, 'Python编程', 1, 80, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (10, 20, 18, '算法设计', 1, 76, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (11, 21, 18, '计算机技术', 1, 95, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (12, 21, 18, '计算机技术', 2, 98, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (13, 21, 18, '数据结构', 1, 93, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (14, 21, 18, 'Python编程', 1, 96, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (15, 21, 18, '算法设计', 1, 94, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (16, 22, 18, '计算机技术', 1, 82, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (17, 22, 18, '计算机技术', 2, 85, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (18, 22, 18, '数据结构', 1, 79, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (19, 22, 18, 'Python编程', 1, 83, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (20, 22, 18, '算法设计', 1, 81, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (21, 23, 18, '计算机技术', 1, 90, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (22, 23, 18, '计算机技术', 2, 93, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (23, 23, 18, '数据结构', 1, 88, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (24, 23, 18, 'Python编程', 1, 91, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (25, 23, 18, '算法设计', 1, 89, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (26, 24, 18, '计算机技术', 1, 68, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (27, 24, 18, '计算机技术', 2, 72, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (28, 24, 18, '数据结构', 1, 65, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (29, 24, 18, 'Python编程', 1, 70, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (30, 24, 18, '算法设计', 1, 74, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (31, 25, 18, '计算机技术', 1, 86, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (32, 25, 18, '计算机技术', 2, 89, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (33, 25, 18, '数据结构', 1, 84, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (34, 25, 18, 'Python编程', 1, 87, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (35, 25, 18, '算法设计', 1, 85, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (36, 26, 18, '计算机技术', 1, 91, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (37, 26, 18, '计算机技术', 2, 94, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (38, 26, 18, '数据结构', 1, 90, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (39, 26, 18, 'Python编程', 1, 92, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (40, 26, 18, '算法设计', 1, 93, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (41, 27, 18, '计算机技术', 1, 77, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (42, 27, 18, '计算机技术', 2, 80, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (43, 27, 18, '数据结构', 1, 75, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (44, 27, 18, 'Python编程', 1, 78, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (45, 27, 18, '算法设计', 1, 79, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (46, 28, 18, '计算机技术', 1, 84, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (47, 28, 18, '计算机技术', 2, 87, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (48, 28, 18, '数据结构', 1, 82, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (49, 28, 18, 'Python编程', 1, 85, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (50, 28, 18, '算法设计', 1, 86, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (51, 29, 18, '计算机技术', 1, 79, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (52, 29, 18, '计算机技术', 2, 82, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (53, 29, 18, '数据结构', 1, 77, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (54, 29, 18, 'Python编程', 1, 80, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (55, 29, 18, '算法设计', 1, 81, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (56, 30, 18, '计算机技术', 1, 89, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (57, 30, 18, '计算机技术', 2, 91, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (58, 30, 18, '数据结构', 1, 87, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (59, 30, 18, 'Python编程', 1, 89, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (60, 30, 18, '算法设计', 1, 88, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (61, 31, 18, '计算机技术', 1, 73, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (62, 31, 18, '计算机技术', 2, 76, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (63, 31, 18, '数据结构', 1, 70, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (64, 31, 18, 'Python编程', 1, 74, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (65, 31, 18, '算法设计', 1, 75, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (66, 32, 18, '计算机技术', 1, 88, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (67, 32, 18, '计算机技术', 2, 90, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (68, 32, 18, '数据结构', 1, 86, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (69, 32, 18, 'Python编程', 1, 88, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (70, 32, 18, '算法设计', 1, 87, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (71, 33, 18, '计算机技术', 1, 92, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (72, 33, 18, '计算机技术', 2, 95, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (73, 33, 18, '数据结构', 1, 91, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (74, 33, 18, 'Python编程', 1, 94, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (75, 33, 18, '算法设计', 1, 92, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);
INSERT INTO `student_scores` VALUES (76, 34, 18, '计算机技术', 1, 81, 100, '2025-09-15', '第一次月考', '2025-09-15 10:00:00', '2025-09-15 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (77, 34, 18, '计算机技术', 2, 84, 100, '2025-10-20', '第二次月考', '2025-10-20 10:00:00', '2025-10-20 10:00:00', NULL);
INSERT INTO `student_scores` VALUES (78, 34, 18, '数据结构', 1, 80, 100, '2025-09-18', '期中考试', '2025-09-18 14:00:00', '2025-09-18 14:00:00', NULL);
INSERT INTO `student_scores` VALUES (79, 34, 18, 'Python编程', 1, 82, 100, '2025-10-10', '上机考试', '2025-10-10 15:00:00', '2025-10-10 15:00:00', NULL);
INSERT INTO `student_scores` VALUES (80, 34, 18, '算法设计', 1, 83, 100, '2025-11-05', '课程作业', '2025-11-05 16:00:00', '2025-11-05 16:00:00', NULL);

-- ----------------------------
-- Table structure for teacher_students
-- ----------------------------
DROP TABLE IF EXISTS `teacher_students`;
CREATE TABLE `teacher_students`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '??ID',
  `teacher_id` int NOT NULL COMMENT '??ID',
  `student_id` int NOT NULL COMMENT '??ID',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '????',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_teacher_student`(`teacher_id` ASC, `student_id` ASC) USING BTREE,
  INDEX `idx_teacher_id`(`teacher_id` ASC) USING BTREE,
  INDEX `idx_student_id`(`student_id` ASC) USING BTREE,
  CONSTRAINT `teacher_students_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `teacher_students_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 47 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '???????' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of teacher_students
-- ----------------------------
INSERT INTO `teacher_students` VALUES (1, 2, 6, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (2, 2, 7, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (3, 2, 8, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (4, 2, 9, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (5, 2, 10, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (6, 2, 11, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (7, 2, 12, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (8, 2, 13, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (9, 2, 14, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (10, 2, 15, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (11, 3, 6, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (12, 3, 7, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (13, 3, 8, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (14, 3, 9, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (15, 3, 10, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (16, 3, 11, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (17, 3, 12, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (18, 3, 13, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (19, 3, 14, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (20, 3, 15, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (21, 4, 6, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (22, 4, 7, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (23, 4, 8, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (24, 4, 9, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (25, 4, 10, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (26, 4, 11, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (27, 4, 12, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (28, 4, 13, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (29, 4, 14, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (30, 4, 15, '2025-12-07 20:46:14', NULL);
INSERT INTO `teacher_students` VALUES (31, 18, 19, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (32, 18, 20, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (33, 18, 21, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (34, 18, 22, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (35, 18, 23, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (36, 18, 24, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (37, 18, 25, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (38, 18, 26, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (39, 18, 27, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (40, 18, 28, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (41, 18, 29, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (42, 18, 30, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (43, 18, 31, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (44, 18, 32, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (45, 18, 33, '2025-12-07 21:32:08', NULL);
INSERT INTO `teacher_students` VALUES (46, 18, 34, '2025-12-07 21:32:08', NULL);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '??ID',
  `identity` enum('student','teacher') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '????',
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '???/??/??',
  `fullname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '??',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '??????',
  `subject` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '????',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'JWT??',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '????',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '????',
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '????',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  INDEX `idx_username`(`username` ASC) USING BTREE,
  INDEX `idx_identity`(`identity` ASC) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '???' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'teacher', 'T001', '沈腾', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', '??', NULL, '2025-12-07 20:46:14', '2025-12-07 22:30:24', NULL);
INSERT INTO `users` VALUES (2, 'teacher', 'T002', '许南枝', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', '??', NULL, '2025-12-07 20:46:14', '2025-12-07 22:30:45', NULL);
INSERT INTO `users` VALUES (3, 'teacher', 'T003', '温若雪', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', '??', NULL, '2025-12-07 20:46:14', '2025-12-07 22:30:43', NULL);
INSERT INTO `users` VALUES (4, 'teacher', 'T004', '叶梓萱', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', '??', NULL, '2025-12-07 20:46:14', '2025-12-07 22:30:41', NULL);
INSERT INTO `users` VALUES (5, 'teacher', 'T005', '朱莉', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', '??', NULL, '2025-12-07 20:46:14', '2025-12-07 22:30:38', NULL);
INSERT INTO `users` VALUES (6, 'student', 'S001', '杨静', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:41', NULL);
INSERT INTO `users` VALUES (7, 'student', 'S002', '赵雷', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:45', NULL);
INSERT INTO `users` VALUES (8, 'student', 'S003', '孙丽娜', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:49', NULL);
INSERT INTO `users` VALUES (9, 'student', 'S004', '周杰', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:50', NULL);
INSERT INTO `users` VALUES (10, 'student', 'S005', '吴倩', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:56', NULL);
INSERT INTO `users` VALUES (11, 'student', 'S006', '徐鹏', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:59', NULL);
INSERT INTO `users` VALUES (12, 'student', 'S007', '郑怡', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:29:02', NULL);
INSERT INTO `users` VALUES (13, 'student', 'S008', '冯宇', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:29:05', NULL);
INSERT INTO `users` VALUES (14, 'student', 'S009', '王芳', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:30', NULL);
INSERT INTO `users` VALUES (15, 'student', 'S010', '李明', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:33', NULL);
INSERT INTO `users` VALUES (16, 'student', 'S011', '刘晓婷', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:36', NULL);
INSERT INTO `users` VALUES (17, 'student', 'S012', '陈浩', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 20:46:14', '2025-12-07 22:28:38', NULL);
INSERT INTO `users` VALUES (18, 'teacher', 'admin', '张三', 'pbkdf2:sha256:600000$6aFIyssDYDo4NXsx$fcdd57db61bf8e7e28b63503b94c550232110ca50e08ee6371bab02f560f9e44', '计算机技术', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxOCwiaWRlbnRpdHkiOiJ0ZWFjaGVyIiwidXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTc2Nzg4NTM5NywiaWF0IjoxNzY1MjkzMzk3fQ.UiiOhjrDpRQmVVQssFYDiL9EzAMVcx8fg0mIncq3jfo', '2025-12-07 12:46:56', '2025-12-09 15:16:37', NULL);
INSERT INTO `users` VALUES (19, 'student', 'S013', '何梦瑶', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:08', NULL);
INSERT INTO `users` VALUES (20, 'student', 'S014', '吕晨', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:11', NULL);
INSERT INTO `users` VALUES (21, 'student', 'S015', '施雨涵', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:15', NULL);
INSERT INTO `users` VALUES (22, 'student', 'S016', '郭强', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:18', NULL);
INSERT INTO `users` VALUES (23, 'student', 'S017', '林晓雯', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:21', NULL);
INSERT INTO `users` VALUES (24, 'student', 'S018', '马睿', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:23', NULL);
INSERT INTO `users` VALUES (25, 'student', 'S019', '罗欣怡', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:26', NULL);
INSERT INTO `users` VALUES (26, 'student', 'S020', '梁博', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:29', NULL);
INSERT INTO `users` VALUES (27, 'student', 'S021', '宋佳', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:32', NULL);
INSERT INTO `users` VALUES (28, 'student', 'S022', '谢东', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:35', NULL);
INSERT INTO `users` VALUES (29, 'student', 'S023', '韩雪', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:40', NULL);
INSERT INTO `users` VALUES (30, 'student', 'S024', '唐泽', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:42', NULL);
INSERT INTO `users` VALUES (31, 'student', 'S025', '邓紫棋', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:45', NULL);
INSERT INTO `users` VALUES (32, 'student', 'S026', '曹逸飞', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:47', NULL);
INSERT INTO `users` VALUES (33, 'student', 'S027', '蒋婉清', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:29:49', NULL);
INSERT INTO `users` VALUES (34, 'student', 'S028', '张伟', '$2b$12$VIx3x3W9.V9dB3jZ5N2R2uQ5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5Q5', NULL, NULL, '2025-12-07 21:32:08', '2025-12-07 22:28:24', NULL);

SET FOREIGN_KEY_CHECKS = 1;
