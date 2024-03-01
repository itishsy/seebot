CREATE TABLE `flow` (
  `flow_code` VARCHAR(50) DEFAULT NULL,
  `timestamp` DATETIME DEFAULT NULL,
  `username` VARCHAR(50) DEFAULT NULL
);

CREATE TABLE `flow_step` (
  `flow_code` VARCHAR(50) NOT NULL,
  `group_code` VARCHAR(255) DEFAULT NULL,
  `step_code` VARCHAR(50) NOT NULL,
  `step_name` VARCHAR(4000) NOT NULL,
  `action_code` VARCHAR(100) NOT NULL,
  `target_args` VARCHAR(8000) DEFAULT NULL,
  `action_args` VARCHAR(8000) DEFAULT NULL,
  `number` INT(11) NOT NULL,
  `level` INT(11) DEFAULT NULL,
  `status` INT(11) DEFAULT '1',
  `failed_retry` INT(11) DEFAULT NULL,
  `failed_strategy` INT(11) DEFAULT '0',
  `failed_skip_to` VARCHAR(100) DEFAULT NULL,
  `success_retry` INT(11) DEFAULT NULL,
  `skip_to` VARCHAR(100) DEFAULT NULL,
  `false_skip_to` VARCHAR(255) DEFAULT NULL,
  `skip_condition` VARCHAR(500) DEFAULT NULL,
  `wait_before` INT(11) DEFAULT NULL,
  `wait_after` INT(11) DEFAULT NULL,
  `timeout` INT(11) DEFAULT NULL,
  `type` INT(11) DEFAULT NULL,
  `open_edit` INT(11) DEFAULT NULL,
  `create_id` INT(11) DEFAULT NULL,
  `create_time` DATETIME DEFAULT NULL,
  `update_id` INT(11) DEFAULT NULL,
  `update_time` DATETIME DEFAULT NULL
);

CREATE TABLE `setting` (
  `key` VARCHAR(50) DEFAULT NULL,
  `value` VARCHAR(2000) DEFAULT NULL
);