-- mysql -u root -p --local-infile=1 mybase < init.sql

SET NAMES utf8mb4;

-- ----------------------------
-- 1. 创建国家信息表（无外键修改）
-- ----------------------------
DROP TABLE IF EXISTS countries;
CREATE TABLE countries (
    created_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    iso CHAR(3) PRIMARY KEY COMMENT 'ISO3代码',
    country VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    subregion VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    region VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
);

-- ----------------------------
-- 2. 创建灾害主表（移除 iso 外键）
-- ----------------------------
DROP TABLE IF EXISTS disasters;
CREATE TABLE disasters (
    created_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dis_no VARCHAR(20) PRIMARY KEY COMMENT '灾害编号 (如2004-0659)',
    classification_key CHAR(20) NOT NULL,
    disaster_group VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    disaster_subgroup VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    disaster_type VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    disaster_subtype VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    event_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
    iso CHAR(3) NOT NULL,  -- 保留字段但移除外键约束
    country VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    subregion VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    region VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    location TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
    origin TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
    ofda_response BOOLEAN NOT NULL,
    appeal BOOLEAN NOT NULL,
    declaration BOOLEAN NOT NULL,
    magnitude DECIMAL(10,2) NULL DEFAULT NULL,
    magnitude_scale VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
    latitude DECIMAL(9,6) NULL DEFAULT NULL,
    longitude DECIMAL(9,6) NULL DEFAULT NULL,
    river_basin TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
    start_year INT NULL DEFAULT NULL,
    start_month INT NULL DEFAULT NULL,
    start_day INT NULL DEFAULT NULL,
    end_year INT NULL DEFAULT NULL,
    end_month INT NULL DEFAULT NULL,
    end_day INT NULL DEFAULT NULL,
    start_date DATE NULL DEFAULT NULL,
    end_date DATE NULL DEFAULT NULL,
    duration_days INT NULL DEFAULT NULL
);

-- ----------------------------
-- 3. 创建经济损失表（移除 dis_no 外键）
-- ----------------------------
DROP TABLE IF EXISTS economic_loss;
CREATE TABLE economic_loss (
    created_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dis_no VARCHAR(20) PRIMARY KEY,
    disaster_type VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    country VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    reconstruction_adjusted DECIMAL(15,2) NULL DEFAULT NULL,
    insured_adjusted DECIMAL(15,2) NULL DEFAULT NULL,
    total_adjusted DECIMAL(15,2) NULL DEFAULT NULL,
    cpi DECIMAL(15,8) NULL DEFAULT NULL,
    start_year INT NULL DEFAULT NULL,
    start_date DATE NULL DEFAULT NULL,
    end_date DATE NULL DEFAULT NULL
);

-- ----------------------------
-- 4. 创建人员影响表（移除 dis_no 外键）
-- ----------------------------
DROP TABLE IF EXISTS human_impact;
CREATE TABLE human_impact (
    created_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dis_no VARCHAR(20) PRIMARY KEY,
    disaster_type VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    country VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    total_deaths INT NULL DEFAULT NULL,
    num_injured INT NULL DEFAULT NULL,
    num_affected INT NULL DEFAULT NULL,
    num_homeless INT NULL DEFAULT NULL,
    total_affected INT NULL DEFAULT NULL,
    start_year INT NULL DEFAULT NULL,
    start_date DATE NULL DEFAULT NULL,
    end_date DATE NULL DEFAULT NULL
);

-- ----------------------------
-- 5. 创建关联灾害类型表（移除 dis_no 外键）
-- ----------------------------
DROP TABLE IF EXISTS associated_types;
CREATE TABLE associated_types (
    created_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL  DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dis_no VARCHAR(20),
    type_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (dis_no, type_name)
);


-- ----------------------------
-- 导入数据（假设CSV文件路径为 /path/to/your/data/）
-- ----------------------------

-- 导入国家数据（需从disasters.csv去重提取）
-- 注意：此处需要先提取国家数据到独立文件 countries.csv
LOAD DATA INFILE 'D:/MySQL Server 5.7/Uploads/countries.csv'
INTO TABLE countries
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(iso, country, subregion, region);

-- 导入灾害主表数据
LOAD DATA INFILE 'D:/MySQL Server 5.7/Uploads/disasters.csv'
INTO TABLE disasters
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    created_at, updated_at, dis_no, classification_key, disaster_group, disaster_subgroup,
    disaster_type, disaster_subtype, event_name, iso, country, subregion, region, location,
    origin, ofda_response, appeal, declaration,
    @magnitude, magnitude_scale,
    @latitude, @longitude, river_basin,
    @start_year, @start_month, @start_day,
    @end_year, @end_month, @end_day,
    @start_date, @end_date, @duration_days
)
SET
    magnitude = NULLIF(@magnitude, ''),
    latitude = NULLIF(@latitude, ''),
    longitude = NULLIF(@longitude, ''),
    start_year = NULLIF(@start_year, ''),
    start_month = NULLIF(@start_month, ''),
    start_day = NULLIF(@start_day, ''),
    end_year = NULLIF(@end_year, ''),
    end_month = NULLIF(@end_month, ''),
    end_day = NULLIF(@end_day, ''),
    start_date = NULLIF(@start_date, ''),
    end_date = NULLIF(@end_date, ''),
    duration_days = NULLIF(@duration_days, '');

-- 导入经济损失数据
LOAD DATA INFILE 'D:/MySQL Server 5.7/Uploads/economic_loss.csv'
INTO TABLE economic_loss
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(dis_no, disaster_type, country, @reconstruction_adjusted, @insured_adjusted, @total_adjusted, @cpi, start_year, @start_date, @end_date)
SET
    reconstruction_adjusted = NULLIF(@reconstruction_adjusted, ''),
    insured_adjusted = NULLIF(@insured_adjusted, ''),
    total_adjusted = NULLIF(@total_adjusted, ''),
    cpi = NULLIF(@cpi, ''),
    start_date = NULLIF(@start_date, ''),
    end_date = NULLIF(@end_date, '');

-- 导入人员影响数据
LOAD DATA INFILE 'D:/MySQL Server 5.7/Uploads/human_impact.csv'
INTO TABLE human_impact
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(dis_no, disaster_type, country, @total_deaths, @num_injured, @num_affected, @num_homeless, @total_affected, start_year, @start_date, @end_date)
SET
    total_deaths = NULLIF(@total_deaths, ''),
    num_injured = NULLIF(@num_injured, ''),
    num_affected = NULLIF(@num_affected, ''),
    num_homeless = NULLIF(@num_homeless, ''),
    total_affected = NULLIF(@total_affected, ''),
    start_date = NULLIF(@start_date, ''),
    end_date = NULLIF(@end_date, '');

-- 导入关联灾害类型数据（需预处理为独立CSV）
LOAD DATA INFILE 'D:/MySQL Server 5.7/Uploads/associated_types.csv'
INTO TABLE associated_types
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(dis_no, type_name);

-- 启用外键约束检查
SET FOREIGN_KEY_CHECKS = 1;

-- 创建索引优化查询性能
-- CREATE INDEX idx_start_date ON disasters(start_date);
-- CREATE INDEX idx_disaster_type ON disasters(disaster_type);
-- CREATE INDEX idx_region ON disasters(region);