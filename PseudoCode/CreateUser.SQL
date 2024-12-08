BEGIN UserCreate

    GET Username
    GET Password

    Password = HASH Password

    IF Username IN DATABASE THEN
        RETURN "Username already exists, sorry"
    ELSE
        ADD Username TO DATABASE
        ADD Password TO DATABASE
        RETURN "Account created, please log in"
    ENDIF

END UserCreate