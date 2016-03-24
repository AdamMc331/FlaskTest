DELIMITER $$
CREATE PROCEDURE `sp_getWishByUser`(
	IN p_user INT
)
BEGIN
	SELECT * FROM wishes WHERE user = p_user;
END $$
DELIMITER ;
