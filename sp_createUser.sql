DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
	IN p_name VARCHAR(100),
	IN p_username VARCHAR(100),
	IN p_password VARCHAR(100)
)
BEGIN
	IF(SELECT EXISTS (SELECT 1 FROM users WHERE username = p_username)) THEN
		SELECT 'Username exists!';
	ELSE
		INSERT INTO users (name, username, password) VALUES (p_name, p_username, p_password);
	END IF;
END $$
DELIMITER ;
