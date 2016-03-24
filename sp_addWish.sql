DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addWish`(
	IN p_title VARCHAR(100),
	IN p_description VARCHAR(100),
	IN p_user INT
)
BEGIN
	INSERT INTO wishes (title, description, user, date) VALUES (p_title, p_description, p_user, NOW());
END $$
DELIMITER ;
