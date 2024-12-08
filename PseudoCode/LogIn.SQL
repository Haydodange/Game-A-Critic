BEGIN LogIn

    GET Username
    GET Password

    Password = HASH Password

    IF Username IN DATABASE THEN
        IF Password MATCH Username:Password THEN
            RETURN "You have successfully logged in!"
        ELSE
            RETURN "Username/Password is incorrect"
        END IF
    ELSE
        RETURN "Username/Password is incorrect"
    END IF

END LogIn