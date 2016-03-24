DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
	IN p_username VARCHAR(100)
)
BEGIN
	SELECT * FROM users WHERE username = p_username;
END $$
DELIMITER ;
