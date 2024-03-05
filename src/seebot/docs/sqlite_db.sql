CREATE TABLE `flow` (
  `code` VARCHAR(50) DEFAULT NULL,
  `steps` TEXT DEFAULT NULL,
  `is_sync` INTEGER DEFAULT NULL,
  `updated` TEXT DEFAULT NULL,
  `synced` TEXT DEFAULT NULL
);

CREATE TABLE `setting` (
  `key` VARCHAR(50) DEFAULT NULL,
  `value` VARCHAR(2000) DEFAULT NULL
);