instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS todo;',
    'DROP TABLE IF EXISTS user;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE userpython (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """
]